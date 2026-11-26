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
    const sender = message.from || "";
    const route = ROUTES[to];
    const subject = decodeMimeWords(message.headers.get("subject") || "(no subject)");
    const messageId = message.headers.get("message-id") || "";

    if (!route || isAutomated(message, sender)) {
      await message.forward(env.OWNER_EMAIL);
      return;
    }

    const raw = await new Response(message.raw).text();
    const question = cleanBody(extractText(raw)).slice(0, 4000);

    let answer = null;
    let status = "";
    if (!question) {
      status = "empty message, no AI reply sent";
    } else {
      try {
        answer = await askBot(env, route.path, question);
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
          to: sender,
          subject: reSubject(subject),
          body: answer + FOOTER,
          inReplyTo: messageId,
        })));
        status = "AI reply sent";
      } catch (e) {
        status = "reply failed: " + e.message;
      }
    }

    // The owner's copy: their message + what the AI said, Reply-To the sender.
    const copy =
      `From: ${sender}\nTo: ${to}\nSubject: ${subject}\nStatus: ${status}\n\n` +
      `----- Their message -----\n${question || "(no text)"}\n\n` +
      `----- AI reply -----\n${answer || "(none)"}\n`;
    try {
      await env.OWNER.send(new EmailMessage(to, env.OWNER_EMAIL, buildMime({
        fromName: route.name,
        fromAddr: to,
        to: env.OWNER_EMAIL,
        replyTo: sender,
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
  if (!text || /temporarily unavailable/i.test(text)) return null;
  return text.replace(/\*\*/g, "");
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

export function buildMime({ fromName, fromAddr, to, subject, body, inReplyTo, replyTo }) {
  const clean = (v) => String(v).replace(/[\r\n]+/g, " ");
  const headers = [
    `From: ${encodeHeader(clean(fromName))} <${fromAddr}>`,
    `To: ${clean(to)}`,
    `Subject: ${encodeHeader(clean(subject))}`,
    `Date: ${new Date().toUTCString()}`,
    `Message-ID: <${crypto.randomUUID()}@${fromAddr.split("@")[1]}>`,
    "MIME-Version: 1.0",
    "Content-Type: text/plain; charset=UTF-8",
    "Content-Transfer-Encoding: base64",
    "Auto-Submitted: auto-replied",
  ];
  if (inReplyTo) headers.push(`In-Reply-To: ${clean(inReplyTo)}`, `References: ${clean(inReplyTo)}`);
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
    else out.push(s.charCodeAt(i) & 0xff);
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

export function extractText(raw) {
  const r = findText(raw);
  if (!r) return "";
  if (r.type === "plain") return r.text;
  return r.text
    .replace(/<(style|script)[\s\S]*?<\/\1>/gi, "")
    .replace(/<br\s*\/?>|<\/p>|<\/div>/gi, "\n")
    .replace(/<[^>]+>/g, "")
    .replace(/&nbsp;/g, " ").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&amp;/g, "&");
}

// Keep only the new text: drop quoted replies and signatures.
export function cleanBody(t) {
  const out = [];
  for (const line of t.replace(/\r\n/g, "\n").split("\n")) {
    if (/^On .+wrote:\s*$/.test(line) || /^-{2,}\s*Original Message/i.test(line) ||
        /^_{5,}/.test(line) || line.trim() === "--") break;
    if (line.startsWith(">")) continue;
    out.push(line);
  }
  return out.join("\n").replace(/\n{3,}/g, "\n\n").trim();
}
