// kprsnt-email-bot: Cloudflare Email Worker
//
// Mail to interview@kprsnt.in / chat@kprsnt.in:
//   1. the question is sent to the site's bot API (/api/interview, /api/chat_agent),
//   2. the AI answer goes back to the sender as a threaded reply from the same address,
//   3. the owner gets a copy (their message + the AI answer, Reply-To = the sender).
// The Flask app itself still sends no email: all mail goes out through Cloudflare.
// Anything automated (bounces, lists, no-reply, our own domain) is only forwarded,
// never answered, so two auto-responders can't loop.
//
// It also has an HTTP route, POST /notify, which the Flask app calls after every
// chat-bot answer on the website (api/services/notify.py). It mails the owner the
// visitor's question + the AI answer from chat@kprsnt.in. Protected by NOTIFY_SECRET.
//
// Settings (dashboard → Worker → Settings, or wrangler.toml):
//   API_BASE     text var        https://kprsnt.in
//   OWNER_EMAIL  secret          your inbox, verified under Email Routing → Destination addresses
//   OWNER        send_email binding (no destination restriction needed)
//   NOTIFY_SECRET secret         same value as CHAT_NOTIFY_SECRET on Cloud Run

import { EmailMessage } from "cloudflare:email";

const ROUTES = {
  "interview@kprsnt.in": { path: "/api/interview", name: "Rash Agent (AI for Prashanth)" },
  "chat@kprsnt.in": { path: "/api/chat_agent", name: "RashBot (AI for Prashanth)" },
};

const FOOTER =
  "\n\n--\nThis reply was written by an AI assistant that answers on Prashanth Kumar Kadasi's behalf. " +
  "Prashanth gets a copy of this conversation and will follow up personally where needed.\n" +
  "Portfolio: https://kprsnt.in · Resume: https://kprsnt.in/resume";

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (request.method !== "POST" || url.pathname !== "/notify") {
      return new Response("Not found", { status: 404 });
    }
    if (!(await secretOk(request.headers.get("X-Notify-Secret"), env.NOTIFY_SECRET))) {
      return new Response("Forbidden", { status: 403 });
    }
    let data;
    try { data = await request.json(); } catch { return new Response("Bad JSON", { status: 400 }); }
    if (!data || typeof data !== "object" || Array.isArray(data)) return new Response("Bad JSON", { status: 400 });
    const question = String(data.message || "").slice(0, 4000).trim();
    if (!question) return new Response("Empty", { status: 400 });
    const answer = String(data.answer || "").slice(0, 8000);
    const source = String(data.source || "site chat").slice(0, 40);
    const now = new Date();
    await env.OWNER.send(new EmailMessage("chat@kprsnt.in", env.OWNER_EMAIL, buildMime({
      fromName: "RashBot (site chat)",
      fromAddr: "chat@kprsnt.in",
      to: env.OWNER_EMAIL,
      // One subject per day, so a day's questions thread together in Gmail.
      subject: `Site chat questions ${now.toISOString().slice(0, 10)}`,
      body: `Source: ${source}
Time: ${now.toUTCString()}

` +
            `----- Visitor asked -----
${question}

----- AI answered -----
${answer}
`,
    })));
    return new Response("ok");
  },

  async email(message, env, ctx) {
    const to = (message.to || "").toLowerCase();
    // message.from is the envelope sender (MAIL FROM). It can be a bounce/VERP address, so for display and
    // Reply-To use the person's address from the headers. reply() itself must go to the envelope sender.
    const sender = message.from || "";
    const person = headerAddress(message.headers.get("reply-to")) || headerAddress(message.headers.get("from")) || sender;
    const route = ROUTES[to];
    const subject = decodeMimeWords(message.headers.get("subject") || "(no subject)");
    const messageId = message.headers.get("message-id") || "";
    const references = message.headers.get("references") || "";

    if (!route || isAutomated(message, sender) || isAutomated(message, headerAddress(message.headers.get("from")))) {
      await message.forward(env.OWNER_EMAIL);
      return;
    }

    const raw = await new Response(message.raw).text();
    const { text, quoted } = splitReply(extractText(raw));
    const question = text.slice(0, 3700); // the API cuts at 4000 chars and botMessage adds a short note

    let answer = null;
    let status = "";
    if (!question) {
      status = "empty message, no AI reply sent";
    } else {
      try {
        answer = await askBot(env, route.path, botMessage(to, question, quoted));
        if (!answer) status = "AI unavailable, no reply sent";
      } catch (e) {
        status = "AI call failed: " + e.message;
      }
    }

    if (answer) {
      try {
        await message.reply(new EmailMessage(to, sender, buildMime({
          fromName: route.name,
          fromAddr: to,
          to: person,
          subject: reSubject(subject),
          body: answer + FOOTER,
          inReplyTo: messageId,
          references,
        })));
        status = "AI reply sent";
      } catch (e) {
        status = "reply failed: " + e.message;
      }
    }

    // The owner's copy: their message + what the AI said, Reply-To the sender.
    const copy =
      `From: ${person}${person !== sender ? ` (envelope ${sender})` : ""}\nTo: ${to}\nSubject: ${subject}\nStatus: ${status}\n\n` +
      `----- Their message -----\n${question || "(no text)"}\n\n` +
      `----- AI reply -----\n${answer || "(none)"}\n`;
    try {
      await env.OWNER.send(new EmailMessage(to, env.OWNER_EMAIL, buildMime({
        fromName: route.name,
        fromAddr: to,
        to: env.OWNER_EMAIL,
        replyTo: person,
        subject: `[${status === "AI reply sent" ? "AI replied" : "NEEDS YOU"}] ${subject}`,
        body: copy,
      })));
    } catch (e) {
      console.log("owner copy failed, forwarding original:", e.message);
      await message.forward(env.OWNER_EMAIL);
    }
    console.log(to, sender, status);
  },
};

/**
 * The text sent to the bot API. Neither endpoint keeps email threads, so earlier messages (the quoted part of
 * the email) go in as context; otherwise a follow-up like "and the second one?" gets a confused answer.
 * The note stops the bot's usual "email interview@kprsnt.in, he reads it himself" line: the person already did.
 */
export function botMessage(to, question, quoted = "") {
  const note = `[This message arrived by email at ${to}. Prashanth gets a copy and follows up personally where needed, ` +
    `so don't tell the sender to email him. Reply in plain text.]`;
  const context = stripFooter(quoted).trim();
  if (!context) return `${note}\n\n${question}`;
  const room = Math.max(0, 3900 - note.length - question.length - 80);
  const ctx = context.length > room ? "…" + context.slice(-room) : context;
  return ctx
    ? `${note}\n\nEarlier messages in this email thread, for context only:\n${ctx}\n\nThe sender's new message:\n${question}`
    : `${note}\n\n${question}`;
}

const stripFooter = (s) => {
  const i = s.indexOf("This reply was written by an AI assistant");
  return (i >= 0 ? s.slice(0, i) : s).replace(/\n-- ?\s*$/, "");
};

/** Plain text for e-mail: drop markdown the model may still produce. */
export function plainText(s) {
  return s
    .replace(/\*\*|__/g, "")
    .replace(/^#{1,6}\s+/gm, "")
    .replace(/^\s*[*•]\s+/gm, "- ")
    .replace(/\[([^\]]+)\]\((https?:[^)\s]+)\)/g, (_, t, u) => (t === u ? u : `${t} (${u})`))
    .replace(/`([^`\n]+)`/g, "$1")
    .replace(/\n{3,}/g, "\n\n")
    .trim();
}

// Texts the API returns instead of an answer when its model fails. They must never be mailed as a reply.
const FAILURE_TEXT = /temporarily unavailable|something went wrong\. please try again/i;

async function askBot(env, path, question) {
  const res = await fetch((env.API_BASE || "https://kprsnt.in").replace(/\/$/, "") + path, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "User-Agent": "kprsnt-email-bot",
      // tells the app not to send the owner a second notification for this
      "X-Kprsnt-Source": "email-worker",
    },
    body: JSON.stringify({ message: question }),
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const data = await res.json();
  const text = (data.response || data.answer || "").trim();
  if (!text || FAILURE_TEXT.test(text)) return null;
  return plainText(text);
}

/** "Name <a@b.c>" or "a@b.c" → "a@b.c" (lower-case), or "" when there is no address. */
export function headerAddress(v) {
  const s = String(v || "");
  const m = s.match(/<([^<>\s@]+@[^<>\s@]+)>/) || s.match(/([^\s<>",;:()]+@[^\s<>",;:()]+\.[a-z]{2,})/i);
  return m ? m[1].toLowerCase() : "";
}

async function secretOk(supplied, expected) {
  if (!supplied || !expected) return false;
  const a = new TextEncoder().encode(supplied);
  const b = new TextEncoder().encode(expected);
  if (a.byteLength !== b.byteLength) return false;
  return crypto.subtle.timingSafeEqual(a, b);
}

export function isAutomated(message, sender) {
  const from = sender.toLowerCase();
  const h = (name) => (message.headers.get(name) || "").toLowerCase();
  return (
    (h("auto-submitted") && h("auto-submitted") !== "no") ||
    !!h("list-id") || !!h("list-unsubscribe") ||
    /^(bulk|junk|list|auto_reply)$/.test(h("precedence")) ||
    /(^|[._-])(no-?reply|do-?not-?reply|mailer-daemon|postmaster|bounces?)([._+-]|@)/.test(from) ||
    from.endsWith("@kprsnt.in")
  );
}

// ---------- outgoing MIME ----------
function b64utf8(s) {
  let bin = "";
  for (const b of new TextEncoder().encode(s)) bin += String.fromCharCode(b);
  return btoa(bin);
}

function encodeHeader(s) {
  return /^[\x20-\x7e]*$/.test(s) ? s : `=?UTF-8?B?${b64utf8(s)}?=`;
}

export function reSubject(s) {
  return /^re:/i.test(s.trim()) ? s.trim() : "Re: " + s.trim();
}

/** Display name for From:. Unquoted "(…)" is a comment in RFC 5322, so "RashBot (AI for Prashanth)" showed as "RashBot". */
function displayName(s) {
  if (!/^[\x20-\x7e]*$/.test(s)) return encodeHeader(s);
  return /^[A-Za-z0-9 !#$%&'*+\-/=?^_`{|}~]*$/.test(s) ? s : `"${s.replace(/(["\\])/g, "\\$1")}"`;
}

export function buildMime({ fromName, fromAddr, to, subject, body, inReplyTo, references, replyTo }) {
  const clean = (v) => String(v).replace(/[\r\n]+/g, " ").trim();
  const headers = [
    `From: ${displayName(clean(fromName))} <${fromAddr}>`,
    `To: ${clean(to)}`,
    `Subject: ${encodeHeader(clean(subject))}`,
    `Date: ${new Date().toUTCString()}`,
    `Message-ID: <${crypto.randomUUID()}@${fromAddr.split("@")[1]}>`,
    "MIME-Version: 1.0",
    "Content-Type: text/plain; charset=UTF-8",
    "Content-Transfer-Encoding: base64",
    "Auto-Submitted: auto-replied",
  ];
  if (inReplyTo) {
    // References = the original's References + its Message-ID, so every mail client threads the whole conversation.
    const refs = [...new Set(`${clean(references || "")} ${clean(inReplyTo)}`.match(/<[^<>\s]+>/g) || [clean(inReplyTo)])];
    headers.push(`In-Reply-To: ${clean(inReplyTo)}`, `References: ${refs.slice(-20).join(" ")}`);
  }
  if (replyTo) headers.push(`Reply-To: ${clean(replyTo)}`);
  return headers.join("\r\n") + "\r\n\r\n" + b64utf8(body).replace(/.{1,76}/g, "$&\r\n");
}

// ---------- incoming MIME (no npm needed) ----------
function bytesToText(bytes, charset) {
  try { return new TextDecoder(charset).decode(bytes); }
  catch { return new TextDecoder().decode(bytes); }
}

function qpBytes(s, underscoreIsSpace = false) {
  s = s.replace(/=\r?\n/g, "");
  const out = [];
  for (let i = 0; i < s.length; i++) {
    const hex = s.substr(i + 1, 2);
    if (s[i] === "=" && /^[0-9A-Fa-f]{2}$/.test(hex)) { out.push(parseInt(hex, 16)); i += 2; }
    else if (underscoreIsSpace && s[i] === "_") out.push(32);
    else if (s.charCodeAt(i) < 0x80) out.push(s.charCodeAt(i));
    else out.push(...new TextEncoder().encode(s[i])); // raw UTF-8 left unencoded by a sloppy sender
  }
  return new Uint8Array(out);
}

function b64Bytes(s) {
  return Uint8Array.from(atob(s.replace(/[^A-Za-z0-9+/=]/g, "")), (c) => c.charCodeAt(0));
}

export function decodeMimeWords(s) {
  return s.replace(/=\?([^?]+)\?([BbQq])\?([^?]*)\?=(\s+(?==\?))?/g, (_, cs, enc, txt) =>
    bytesToText(enc.toUpperCase() === "B" ? b64Bytes(txt) : qpBytes(txt, true), cs));
}

function parseHeaders(block) {
  const h = {};
  block.replace(/\r?\n[ \t]+/g, " ").split(/\r?\n/).forEach((line) => {
    const i = line.indexOf(":");
    if (i > 0) h[line.slice(0, i).trim().toLowerCase()] = line.slice(i + 1).trim();
  });
  return h;
}

function splitEntity(raw) {
  const m = raw.match(/\r?\n\r?\n/);
  if (!m) return { headers: parseHeaders(raw), body: "" };
  return { headers: parseHeaders(raw.slice(0, m.index)), body: raw.slice(m.index + m[0].length) };
}

function decodePart(headers, body) {
  const ctype = (headers["content-type"] || "text/plain").toLowerCase();
  const charset = (ctype.match(/charset="?([^";\s]+)"?/) || [])[1] || "utf-8";
  const enc = (headers["content-transfer-encoding"] || "").toLowerCase();
  if (enc === "base64") return bytesToText(b64Bytes(body), charset);
  if (enc === "quoted-printable") return bytesToText(qpBytes(body), charset);
  return body;
}

function findText(raw, depth = 0) {
  const { headers, body } = splitEntity(raw);
  const ctypeRaw = headers["content-type"] || "text/plain";
  const ctype = ctypeRaw.toLowerCase();
  if (ctype.startsWith("multipart/") && depth < 6) {
    const b = (ctypeRaw.match(/boundary="?([^";]+)"?/i) || [])[1];
    if (!b) return null;
    let html = null;
    for (const p of body.split("--" + b).slice(1)) {
      if (p.startsWith("--")) break;
      const r = findText(p.replace(/^\r?\n/, ""), depth + 1);
      if (r && r.type === "plain") return r;
      if (r && !html) html = r;
    }
    return html;
  }
  if (ctype.startsWith("text/plain")) return { type: "plain", text: decodePart(headers, body) };
  if (ctype.startsWith("text/html")) return { type: "html", text: decodePart(headers, body) };
  return null;
}

const QUOTE_MARK = "⁣QUOTED⁣"; // invisible marker line where an HTML quote block starts

const ENTITIES = { nbsp: " ", lt: "<", gt: ">", amp: "&", quot: '"', apos: "'", ndash: "–", mdash: "—", hellip: "…",
  lsquo: "‘", rsquo: "’", ldquo: "“", rdquo: "”", pound: "£", euro: "€", rupee: "₹", copy: "©", middot: "·", bull: "•" };

function decodeEntities(s) {
  return s.replace(/&(#x[0-9a-f]+|#\d+|[a-z]+);/gi, (m, e) => {
    if (e[0] === "#") {
      const n = e[1].toLowerCase() === "x" ? parseInt(e.slice(2), 16) : parseInt(e.slice(1), 10);
      try { return String.fromCodePoint(n); } catch { return m; }
    }
    return ENTITIES[e.toLowerCase()] ?? m;
  });
}

export function extractText(raw) {
  const r = findText(raw);
  if (!r) return "";
  if (r.type === "plain") return r.text;
  const text = r.text
    .replace(/<(style|script|head)[\s\S]*?<\/\1>/gi, "")
    // Quoted earlier mail in HTML (Gmail, Outlook, Apple Mail) has no ">" prefixes: mark where it starts.
    .replace(/<(blockquote|div)\b[^>]*\b(class|id)="[^"]*(gmail_quote|yahoo_quoted|divRplyFwdMsg|appendonsend|moz-cite-prefix)[^"]*"[^>]*>/gi, `\n${QUOTE_MARK}\n$&`)
    .replace(/<blockquote\b[^>]*>/gi, `\n${QUOTE_MARK}\n`)
    .replace(/<br\s*\/?>|<\/p>|<\/div>|<\/li>|<\/tr>|<\/h[1-6]>/gi, "\n")
    .replace(/<li\b[^>]*>/gi, "- ")
    .replace(/<[^>]+>/g, "");
  return decodeEntities(text).replace(/[ \t ]+\n/g, "\n").replace(/[ \t ]{2,}/g, " ");
}

/**
 * Split an e-mail body into the sender's new text and the quoted earlier messages.
 * Handles Gmail/Apple "On … wrote:" (also when wrapped over two lines), Outlook's "From: … Sent:" header block
 * and "-----Original Message-----", underscore separators, "> " quoting, HTML quote blocks and "-- " signatures.
 */
export function splitReply(t) {
  const lines = String(t || "").replace(/\r\n?/g, "\n").split("\n");
  const out = [];
  let cut = -1;
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i], trimmed = line.trim();
    const next = (lines[i + 1] || "").trim();
    const headerBlock = /^\*?(From|Von|De|Da):\*?\s/i.test(trimmed) &&
      lines.slice(i + 1, i + 5).some((l) => /^\*?(Sent|Date|To|Subject|Gesendet|Envoyé|Enviado):\*?\s/i.test(l.trim()));
    if (trimmed === QUOTE_MARK || /^On\s.+wrote:$/i.test(trimmed) || (/^On\s.+/i.test(trimmed) && /wrote:$/i.test(next) && next.length < 120) ||
        /^-{2,}\s*Original Message\s*-*$/i.test(trimmed) || /^-{2,}\s*Forwarded message\s*-*$/i.test(trimmed) ||
        /^_{5,}$/.test(trimmed) || headerBlock || trimmed === "--" || /^Sent from my \w+/i.test(trimmed) ||
        /^Get Outlook for /i.test(trimmed)) {
      cut = i;
      break;
    }
    if (trimmed.startsWith(">")) continue;
    out.push(line);
  }
  const quoted = cut < 0 ? lines.filter((l) => l.trim().startsWith(">")).join("\n")
    : lines.slice(cut).filter((l) => l.trim() !== QUOTE_MARK).join("\n");
  const tidy = (s) => s.replace(/^>+ ?/gm, "").replace(/\n{3,}/g, "\n\n").trim();
  return { text: tidy(out.join("\n")), quoted: tidy(quoted) };
}

// Keep only the new text: drop quoted replies and signatures.
export const cleanBody = (t) => splitReply(t).text;
