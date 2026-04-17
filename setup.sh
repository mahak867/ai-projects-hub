#!/usr/bin/env bash
# ============================================================
# ai-projects-hub setup validator
# Run this before trying any project: bash setup.sh
# ============================================================
set -e

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'

ok()   { echo -e "${GREEN}✓${NC} $1"; }
warn() { echo -e "${YELLOW}⚠${NC}  $1"; }
fail() { echo -e "${RED}✗${NC} $1"; FAILED=1; }

FAILED=0

echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  AI Projects Hub — Environment Check${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

# 1. Python version
echo "[ 1/5 ] Checking Python version..."
if command -v python3 &>/dev/null; then
    PY_VER=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    PY_MAJOR=$(echo $PY_VER | cut -d. -f1)
    PY_MINOR=$(echo $PY_VER | cut -d. -f2)
    if [ "$PY_MAJOR" -ge 3 ] && [ "$PY_MINOR" -ge 10 ]; then
        ok "Python $PY_VER"
    else
        fail "Python $PY_VER found — need 3.10+. Download: https://python.org/downloads"
    fi
else
    fail "Python 3 not found. Download: https://python.org/downloads"
fi

# 2. pip
echo "[ 2/5 ] Checking pip..."
if command -v pip3 &>/dev/null || command -v pip &>/dev/null; then
    ok "pip available"
else
    fail "pip not found — run: python3 -m ensurepip"
fi

# 3. API key
echo "[ 3/5 ] Checking ANTHROPIC_API_KEY..."
if [ -n "${ANTHROPIC_API_KEY}" ]; then
    KEY_PREVIEW="${ANTHROPIC_API_KEY:0:10}..."
    ok "ANTHROPIC_API_KEY set ($KEY_PREVIEW)"
else
    # Check .env files
    if find . -name ".env" | head -1 | grep -q ".env"; then
        warn "ANTHROPIC_API_KEY not exported but .env files found."
        warn "Run: export ANTHROPIC_API_KEY=\$(grep ANTHROPIC_API_KEY .env | cut -d= -f2)"
    else
        fail "ANTHROPIC_API_KEY not set. Get a free key: https://console.anthropic.com"
        echo "       Set it: export ANTHROPIC_API_KEY='sk-ant-...'"
    fi
fi

# 4. Git
echo "[ 4/5 ] Checking git..."
if command -v git &>/dev/null; then
    GIT_VER=$(git --version | awk '{print $3}')
    ok "git $GIT_VER"
else
    warn "git not found — needed only if you plan to contribute"
fi

# 5. Quick API connectivity test
echo "[ 5/5 ] Testing Anthropic API connectivity..."
if [ -n "${ANTHROPIC_API_KEY}" ] && command -v python3 &>/dev/null; then
    RESULT=$(python3 -c "
import urllib.request, json, os, sys
req = urllib.request.Request(
    'https://api.anthropic.com/v1/messages',
    data=json.dumps({'model':'claude-haiku-4-5-20251001','max_tokens':10,'messages':[{'role':'user','content':'hi'}]}).encode(),
    headers={'x-api-key': os.environ['ANTHROPIC_API_KEY'], 'anthropic-version': '2023-06-01', 'content-type': 'application/json'},
    method='POST'
)
try:
    resp = urllib.request.urlopen(req, timeout=10)
    print('ok')
except urllib.error.HTTPError as e:
    body = e.read().decode()
    if 'authentication' in body.lower() or 'invalid' in body.lower():
        print('bad_key')
    else:
        print('ok')
except Exception:
    print('network_error')
" 2>/dev/null)
    case $RESULT in
        ok)           ok "Anthropic API reachable and key valid" ;;
        bad_key)      fail "API key is invalid. Get a new one: https://console.anthropic.com" ;;
        network_error) warn "Could not reach api.anthropic.com — check your internet connection" ;;
    esac
else
    warn "Skipping API test (key not set)"
fi

# Summary
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}  All checks passed! Pick a project and start building.${NC}"
    echo ""
    echo "  Quick start (beginner):"
    echo "    cd 01-pdf-chat-claude"
    echo "    pip install -r requirements.txt"
    echo "    streamlit run app.py"
else
    echo -e "${RED}  Some checks failed. Fix the issues above and re-run: bash setup.sh${NC}"
fi
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"
exit $FAILED
