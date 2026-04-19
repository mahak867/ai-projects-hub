# 🖥️ Claude Computer Use Demo

Practical examples of Claude's computer use capability — Claude can see your screen, run commands, and edit files.

![Demo](https://img.shields.io/badge/difficulty-intermediate-orange?style=flat-square)

## What Claude can do
- 📸 Take and analyze screenshots
- 💻 Run bash commands
- 📝 Read and edit files
- 🖱️ Click, type, and interact with GUIs

## Setup

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
```

## Usage

```bash
# Run the example demos
python demo.py

# Give Claude a specific task
python demo.py "Find all TODO comments in Python files and list them"
python demo.py "Check if port 8080 is in use"
python demo.py "Create a requirements.txt from the imports in main.py"
```

## How it works
The computer use API runs a tool loop:
1. Claude requests a screenshot or bash command
2. Your code executes it and returns the result
3. Claude decides what to do next
4. Repeats until task is complete

## Safety notes
- The bash tool here only allows whitelisted commands
- In production, run in a Docker container or VM
- Never give computer use access to sensitive systems

## Key concept: Tool loops
Computer use is just an extended tool-use loop where Claude has perception (screenshot) and action (keyboard/mouse/bash) tools. The same pattern applies to any agent that needs to take actions in the world.

## ⚠️ Known Limitations
- **Beta API**: Computer use is in public beta and the API interface may change without notice
- **Display required**: Screenshot capture requires a running graphical display; headless Linux servers need a virtual display (e.g., Xvfb)
- **Bash whitelist**: Only whitelisted commands are allowed by default; unwhitelisted commands will be rejected even if Claude requests them
- **No undo**: Claude's actions (file edits, command execution) are irreversible — always run in a sandbox or Docker container for untrusted tasks

## 🧪 Testing & Linting

```bash
# Install linter
pip install ruff

# Check for style and correctness issues
ruff check .

# Verify all dependencies install correctly
pip install -r requirements.txt

# Smoke test — confirm imports load without error
python -c "import anthropic; print('All dependencies OK')"
```
