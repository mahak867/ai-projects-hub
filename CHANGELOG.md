# Changelog

All notable changes to this project are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased]

### Planned
- Streamlit Cloud one-click deploy buttons for projects 01, 05, 14, 15, 19
- Docker support for all CLI projects
- Unit tests for core functions in each project

---

## [1.2.0] — 2025-04

### Added
- GitHub Actions CI: syntax check + structure check on every push
- Context Engineering Cookbook: all 10 patterns now have runnable code
  - Pattern 2: Chain-of-thought investment analysis
  - Pattern 3: Role + constraints for safe financial advice
  - Pattern 4: Few-shot news sentiment classification
  - Pattern 5: Constitutional constraints for market commentary
  - Pattern 6: Multi-source context with priority ordering
  - Pattern 8: Naive vs optimized RAG chunk formatting
  - Pattern 9: Strict output templates for zero-parse-failure production
  - Pattern 10: Uncertainty quantification with confidence scores
- `SECURITY.md`, `CHANGELOG.md`, `ROADMAP.md`
- GitHub issue templates (bug report, feature request)
- Pull request template
- `setup.sh` — one-command environment validator
- `Makefile` — `make lint`, `make check`, `make setup`

### Fixed
- Project 20 missing `requirements.txt` (was causing CI failure)
- Stale model reference in project 10 (`claude-3-5-sonnet` → `claude-sonnet-4-5`)
- Missing docstrings in 21 public functions across projects 06, 08, 09, 13, 16, 18
- Missing `-> None` return type annotations on `send_telegram`, `send_email`, `ingest_pdf`

---

## [1.1.0] — 2025-04

### Added
- `.env.example` files for all 20 projects
- Type hints and docstrings across all major files
- API key validation with helpful error messages at startup in all projects
- Project 17: `screener.py` source code (was missing — only README existed)
- `.gitignore` at repo root

### Fixed
- Project 12: Removed fake response inside `ImportError` handler (critical bug)
- Project 17: Dead link to non-existent source code in README
- Project 03: Added Twilio credential validation and transparent README
- Project 07: Added API key check, type hints, docstrings to MCP server
- JSON parse error handling in projects 05, 11, 13, 16, 18, 19
- Removed accidentally nested `ai-projects-hub/` subfolder

### Changed
- WhatsApp bot README now clearly explains Twilio dependency upfront

---

## [1.0.0] — 2025-03

### Added
- Initial release: 20 AI projects using Claude API
- Projects 01–20 covering RAG, agents, automation, and India-first finance tools
- `CONTRIBUTING.md`, `LICENSE` (MIT)
