# Security Policy

## Supported versions

Only the current `main` branch, which is what runs on
[kprsnt.in](https://kprsnt.in), receives security fixes.

## Reporting a vulnerability

Please **do not open a public issue** for security problems.

Report them privately, either:

- through GitHub: **[Security → Report a vulnerability](https://github.com/kprsnt2/kprsnt.in/security/advisories/new)**, or
- by email to **[security@kprsnt.in](mailto:security@kprsnt.in)**.

Please include:

- the affected URL, route or file;
- steps to reproduce, or a proof of concept;
- the impact you think it has.

You can expect an acknowledgement within 7 days. Once a fix ships, I'm happy
to credit you in the advisory unless you would rather stay anonymous.

## Scope

In scope: the code in this repository and the site it serves at
`kprsnt.in`. That includes the REST API, the MCP server, the OAuth endpoints
and the chat and interview bots.

Out of scope:

- denial-of-service or load testing against the live site;
- reports from automated scanners without a demonstrated impact;
- third-party services the site uses (Cloudflare, Google Cloud, LLM
  providers), which should be reported to those vendors.
