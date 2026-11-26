// Tests for the email worker. Run:  node --test cloudflare/email-worker/
// Node has no "cloudflare:email" module, so the worker is loaded with that import swapped for a stub.
import assert from "node:assert/strict";
import { readFileSync, writeFileSync, mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { test } from "node:test";
import { pathToFileURL } from "node:url";

const src = readFileSync(new URL("./worker.js", import.meta.url), "utf8").replace(
  'import { EmailMessage } from "cloudflare:email";',
  "class EmailMessage { constructor(from, to, raw) { Object.assign(this, { from, to, raw }); } }");
const file = join(mkdtempSync(join(tmpdir(), "email-worker-")), "worker.mjs");
writeFileSync(file, src);
// Workers-only API, not in Node.
crypto.subtle.timingSafeEqual ??= (a, b) => a.byteLength === b.byteLength && a.every((x, i) => x === b[i]);
const W = await import(pathToFileURL(file).href);

const b64 = (s) => Buffer.from(s, "utf8").toString("base64");
const decodeBody = (mime) => Buffer.from(mime.split("\r\n\r\n")[1].replace(/\r\n/g, ""), "base64").toString("utf8");
const header = (mime, name) => (mime.match(new RegExp(`^${name}: (.*)$`, "mi")) || [])[1];

function incoming({ from = "Jane Doe <jane@example.com>", envelope = "srs0=ab12=jane@forwarder.example.net", to = "interview@kprsnt.in",
  subject = "Question", body, html, extra = {} } = {}) {
  const headers = new Map(Object.entries({ from, subject, "message-id": "<orig-2@example.com>",
    references: "<orig-1@example.com>", ...extra }).map(([k, v]) => [k.toLowerCase(), v]));
  const raw = html
    ? `From: ${from}\r\nSubject: ${subject}\r\nContent-Type: multipart/alternative; boundary="B1"\r\n\r\n--B1\r\n` +
      `Content-Type: text/html; charset=UTF-8\r\nContent-Transfer-Encoding: base64\r\n\r\n${b64(html)}\r\n--B1--\r\n`
    : `From: ${from}\r\nSubject: ${subject}\r\nContent-Type: text/plain; charset=UTF-8\r\n\r\n${body}`;
  const sent = { replies: [], forwards: [] };
  return { sent, message: { to, from: envelope, headers: { get: (k) => headers.get(k.toLowerCase()) ?? null },
    raw: new Response(raw).body, reply: async (m) => sent.replies.push(m), forward: async (a) => sent.forwards.push(a) } };
}

function envWith(answer, calls = []) {
  const owner = [];
  globalThis.fetch = async (url, init) => { calls.push({ url, body: JSON.parse(init.body) }); return new Response(JSON.stringify({ response: answer })); };
  return { env: { OWNER_EMAIL: "owner@example.org", API_BASE: "https://kprsnt.in", OWNER: { send: async (m) => owner.push(m) } }, owner, calls };
}

test("From display name with parentheses is quoted", () => {
  const mime = W.buildMime({ fromName: "Rash Agent (AI for Prashanth)", fromAddr: "interview@kprsnt.in", to: "a@b.c", subject: "s", body: "x" });
  assert.equal(header(mime, "From"), '"Rash Agent (AI for Prashanth)" <interview@kprsnt.in>');
  const plain = W.buildMime({ fromName: "RashBot", fromAddr: "chat@kprsnt.in", to: "a@b.c", subject: "s", body: "x" });
  assert.equal(header(plain, "From"), "RashBot <chat@kprsnt.in>");
});

test("References keeps the whole thread", () => {
  const mime = W.buildMime({ fromName: "x", fromAddr: "a@kprsnt.in", to: "b@c.d", subject: "s", body: "x",
    inReplyTo: "<m2@x>", references: "<m0@x> <m1@x>" });
  assert.equal(header(mime, "References"), "<m0@x> <m1@x> <m2@x>");
});

test("Outlook reply: quoted header block is not part of the question", () => {
  const t = "Thanks! And what about the second project?\n\nFrom: Rash Agent <interview@kprsnt.in>\nSent: Monday, 1 December 2026 10:00\n" +
    "To: Jane <jane@example.com>\nSubject: RE: Question\n\nHe built three projects...";
  const r = W.splitReply(t);
  assert.equal(r.text, "Thanks! And what about the second project?");
  assert.match(r.quoted, /He built three projects/);
});

test("Gmail 'On … wrote:' wrapped over two lines, '>' quotes and signatures", () => {
  const t = "Which one used Kafka?\n\nOn Mon, 1 Dec 2026 at 10:00, Rash Agent (AI for Prashanth) <\ninterview@kprsnt.in> wrote:\n> Project A, B and C.";
  assert.deepEqual(W.splitReply(t), { text: "Which one used Kafka?", quoted: "On Mon, 1 Dec 2026 at 10:00, Rash Agent (AI for Prashanth) <\ninterview@kprsnt.in> wrote:\nProject A, B and C." });
  assert.equal(W.cleanBody("Hi\n-- \nJane Doe\nCTO"), "Hi");
  assert.equal(W.cleanBody("Quick one\n\nSent from my iPhone"), "Quick one");
  assert.equal(W.cleanBody("-----Original Message-----"), "");
});

test("HTML-only mail: entities decoded, Gmail quote block removed", async () => {
  const html = `<div dir="ltr">It&#39;s great &amp; I&rsquo;d like &quot;more&quot; info&nbsp;please</div>` +
    `<div class="gmail_quote"><div class="gmail_attr">On Mon, X wrote:<br></div><blockquote>old text</blockquote></div>`;
  const raw = `Content-Type: text/html; charset=UTF-8\r\nContent-Transfer-Encoding: base64\r\n\r\n${b64(html)}`;
  const r = W.splitReply(W.extractText(raw));
  assert.equal(r.text, "It's great & I’d like \"more\" info please");
  assert.match(r.quoted, /old text/);
});

test("quoted-printable with raw UTF-8 is not mangled", () => {
  const raw = "Content-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: quoted-printable\r\n\r\nCaf=C3=A9 and café ₹";
  assert.equal(W.extractText(raw), "Café and café ₹");
});

test("follow-up email sends the thread as context and tells the bot it is email", async () => {
  const { env, calls, owner } = envWith("**Project B** used Kafka. See [repo](https://github.com/x/b).");
  const { message, sent } = incoming({ body: "Which one used Kafka?\n\nOn Mon, 1 Dec 2026, Rash Agent <interview@kprsnt.in> wrote:\n> Projects A, B and C.\n> --\n> This reply was written by an AI assistant that answers on ..." });
  await W.default.email(message, env, {});
  const sentMsg = calls[0].body.message;
  assert.match(sentMsg, /arrived by email at interview@kprsnt\.in/);
  assert.match(sentMsg, /Projects A, B and C\./);
  assert.doesNotMatch(sentMsg, /This reply was written by an AI/);
  assert.match(sentMsg, /The sender's new message:\nWhich one used Kafka\?$/);

  assert.equal(sent.replies.length, 1);
  const reply = sent.replies[0];
  assert.equal(reply.to, "srs0=ab12=jane@forwarder.example.net");          // reply() must go to the envelope sender
  assert.equal(header(reply.raw, "To"), "jane@example.com");         // but the header shows the person
  assert.equal(header(reply.raw, "References"), "<orig-1@example.com> <orig-2@example.com>");
  assert.match(decodeBody(reply.raw), /^Project B used Kafka\. See repo \(https:\/\/github\.com\/x\/b\)\./);

  assert.equal(owner.length, 1);
  assert.equal(header(owner[0].raw, "Reply-To"), "jane@example.com");
  assert.match(decodeBody(owner[0].raw), /----- Their message -----\nWhich one used Kafka\?\n/);
});

test("API failure text is never mailed as an answer", async () => {
  for (const failure of ["I'm sorry, something went wrong. Please try again later.",
    "I'm sorry, my AI service is temporarily unavailable. Please try again later."]) {
    const { env, owner } = envWith(failure);
    const { message, sent } = incoming({ body: "Hello?" });
    await W.default.email(message, env, {});
    assert.equal(sent.replies.length, 0, failure);
    assert.match(header(owner[0].raw, "Subject"), /^\[NEEDS YOU\]/);
  }
});

test("automated or own-domain mail is only forwarded", async () => {
  const { env, calls } = envWith("x");
  const { message, sent } = incoming({ from: "Rash Agent <interview@kprsnt.in>", envelope: "x@sender.com", body: "loop?" });
  await W.default.email(message, env, {});
  assert.deepEqual(sent.forwards, ["owner@example.org"]);
  assert.equal(calls.length, 0);
});

test("/notify rejects null or non-object JSON with 400", async () => {
  const { env } = envWith("x");
  env.NOTIFY_SECRET = "s3cret";
  for (const body of ["null", "[]", "7"]) {
    const res = await W.default.fetch(new Request("https://w/notify", { method: "POST", headers: { "X-Notify-Secret": "s3cret" }, body }), env);
    assert.equal(res.status, 400, body);
  }
});
