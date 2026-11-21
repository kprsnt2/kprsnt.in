# Changelog

Notable changes to kprsnt.in. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/). The site deploys
continuously from `main`, so changes are grouped by date rather than version.
Automated content updates (swarm memory, daily views, job data) are not listed.

## [Unreleased]

### Added
- Content license: posts, resume and case-study text, data and images are
  CC BY 4.0 (`LICENSE-CONTENT`); code stays MIT. Shown in the site footer.
- security@kprsnt.in as the private contact for security and Code of Conduct
  reports.
- Standard open-source project files: contributing guide, Code of Conduct,
  security policy, issue and pull request templates, CODEOWNERS, Dependabot
  and EditorConfig.
- `/favicon.ico` and a 192px PWA icon.
- CI job that builds and boots the Docker image.
- Health check after each Cloud Run deploy; deploys now run the tests first.

### Removed
- The AI email auto-reply: the inbound-email webhook, the bots' "send resume"
  email tool, reply emails and owner notifications, along with the Resend
  dependency and the `RESEND_API_KEY`, `OWNER_NOTIFY_EMAIL`,
  `INTERVIEW_FROM_EMAIL` and `EMAIL_WEBHOOK_SECRET` settings. Mail to
  interview@, chat@ and security@kprsnt.in now goes to a person through
  Cloudflare Email Routing.

### Changed
- `/api/interview` and `/api/chat_agent` return only the answer
  (`email_sent` and `from` are gone; `from_email` / `send_email` are ignored).
  The bots point people to interview@kprsnt.in and the resume page.
- Static assets get a content-hash URL and a one-year cache. Previously they
  were served `no-cache`.
- `www.kprsnt.in` and direct `*.run.app` requests redirect to `https://kprsnt.in`.
- The OpenAI SDK loads on first use, which cuts cold-start import time from
  ~0.7s to ~0.2s.
- CI uses Python 3.12 to match the Docker image.

### Fixed
- The 512px PWA icon had its mark in the corner instead of centered.
