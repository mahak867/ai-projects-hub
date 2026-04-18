# ============================================================
# AI Projects Hub — Makefile
# Usage: make <target>
# ============================================================

.PHONY: help setup lint check test clean

# Default target
help:
	@echo ""
	@echo "AI Projects Hub — Available commands:"
	@echo ""
	@echo "  make setup    Validate your environment (Python, API key, connectivity)"
	@echo "  make lint     Check all Python files for syntax errors"
	@echo "  make check    Full CI check (syntax + structure)"
	@echo "  make clean    Remove __pycache__ and temp files"
	@echo ""

# Validate environment
setup:
	@bash setup.sh

# Syntax check all Python files and run ruff for deeper analysis
lint:
	@echo "Checking Python syntax..."
	@find . -name "*.py" -not -path "./.git/*" -not -path "*/__pycache__/*" | \
		while read f; do python3 -m py_compile "$$f" && echo "  ✓ $$f" || exit 1; done
	@echo "All files OK ✓"
	@echo "Running ruff..."
	@command -v ruff >/dev/null 2>&1 \
		&& ruff check --select F821,F811,E9 . && echo "Ruff OK ✓" \
		|| echo "  (ruff not installed; skipping — run: pip install ruff)"

# Full structure + syntax check (mirrors CI)
check: lint
	@echo "Checking project structure..."
	@FAILED=0; \
	for dir in [0-9][0-9]-*/; do \
		[ -f "$$dir/README.md" ]        || { echo "  Missing README.md in $$dir"; FAILED=1; }; \
		[ -f "$$dir/requirements.txt" ] || { echo "  Missing requirements.txt in $$dir"; FAILED=1; }; \
		[ -f "$$dir/.env.example" ]     || { echo "  Missing .env.example in $$dir"; FAILED=1; }; \
	done; \
	[ $$FAILED -eq 0 ] && echo "Structure OK ✓" || exit 1

# Remove Python cache
clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -name "*.pyc" -delete 2>/dev/null || true
	@find . -name "*.pyo" -delete 2>/dev/null || true
	@find . -name ".DS_Store" -delete 2>/dev/null || true
	@echo "Cleaned ✓"
