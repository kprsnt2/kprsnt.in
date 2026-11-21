# Contributing to kprsnt.in

Thanks for your interest! This repository is the source of my personal
portfolio, [kprsnt.in](https://kprsnt.in). The code is open source under the
[MIT License](LICENSE); the written content is
[CC BY 4.0](LICENSE-CONTENT). Bug reports, fixes and ideas are welcome. You are also
welcome to fork it as a starting point for your own Flask + Cloud Run site.

By taking part you agree to follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## Ways to contribute

- **Report a bug.** Open an issue with the *Bug report* template. Say what you
  expected, what happened, and the URL or route.
- **Suggest an improvement.** Open an issue with the *Feature request*
  template before starting large changes, so we can agree on the approach.
- **Fix something.** Small fixes (typos, broken links, failing tests,
  accessibility) can go straight to a pull request.
- **Security issues.** Please do **not** open a public issue. See
  [SECURITY.md](SECURITY.md).

Content that is personal to me (resume data, blog posts, case studies, job
data) is not open for edits through pull requests, apart from fixing obvious
typos or broken links.

## Development setup

Requires Python 3.12 (the same version as the Docker image).

```bash
git clone https://github.com/kprsnt2/kprsnt.in.git
cd kprsnt.in
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements-dev.txt

cp .env.example .env              # every key is optional for local work
python api/index.py               # http://127.0.0.1:5000
```

The app runs without any API keys: pages render, and the AI endpoints return
a "not configured" response.

To run the production container exactly as Cloud Run does:

```bash
docker build -t kprsnt .
docker run -p 8080:8080 --env-file .env kprsnt   # http://localhost:8080
```

## Before you open a pull request

```bash
pytest -q
ruff check api scripts tests --select E9,F63,F7,F82,F
```

CI runs both, and also builds and boots the Docker image.

## Guidelines

- **Keep it simple.** Prefer the smallest change that fully solves the
  problem. Use the standard library or an existing dependency before adding a
  new one (see `.github/copilot-instructions.md`).
- **Fix root causes.** Fix a bug where it starts rather than working around it
  in each caller.
- **Add a test** for any bug fix or new route, under `tests/`.
- **No secrets in code.** Configuration comes from environment variables;
  document new ones in `.env.example` and the README.
- **Data directories are runtime inputs.** If you add a directory the app
  reads, keep it out of `.dockerignore`.
- **Static assets:** link them with `url_for('static', filename=...)`. A
  content hash is added automatically, so never hand-add `?v=N`.

## Commit messages and pull requests

- Use short, imperative commit subjects, optionally with a
  [Conventional Commits](https://www.conventionalcommits.org/) prefix
  (`fix:`, `feat:`, `docs:`, `chore:`).
- Keep each pull request focused on one change and fill in the template.
- Add a line under **Unreleased** in [CHANGELOG.md](CHANGELOG.md) for
  user-visible changes.

## License

By contributing, you agree that code contributions are licensed under the
[MIT License](LICENSE), and contributions to content (posts, resume and
case-study text, data, images) under [CC BY 4.0](LICENSE-CONTENT).
