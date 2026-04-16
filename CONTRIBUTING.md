# Contributing to AI Projects Hub

Thank you for your interest in improving this project! This guide will help you contribute effectively.

## Code Quality Standards

All code contributions should meet these standards:

### 1. Type Hints Required
```python
# ❌ BAD - No type hints
def process_data(data, config):
    return data.transform(config)

# ✅ GOOD - Clear type hints
from typing import Dict, List

def process_data(data: List[Dict], config: Dict[str, any]) -> List[Dict]:
    """Process data according to configuration.
    
    Args:
        data: List of data dictionaries to process
        config: Configuration parameters
        
    Returns:
        Processed data list
    """
    return data.transform(config)
```

### 2. Code Formatting
All Python code must be formatted with `black`:

```bash
# Install black
pip install black

# Format your code before committing
black .
```

Configuration in `pyproject.toml`:
```toml
[tool.black]
line-length = 100
target-version = ['py310']
```

### 3. Linting
Code should pass `ruff` checks:

```bash
# Install ruff
pip install ruff

# Check for issues
ruff check .

# Auto-fix safe issues
ruff check --fix .
```

### 4. Error Handling

**Never** use exceptions to hide errors or return fake data:

```python
# ❌ BAD - Silent failure with fake data
try:
    import whisper
    result = whisper.transcribe(audio)
    return result["text"]
except ImportError:
    return "Fake transcript data..."  # NEVER DO THIS

# ✅ GOOD - Fail loudly with helpful message
try:
    import whisper
except ImportError as e:
    raise ImportError(
        "whisper not installed. Install with: pip install openai-whisper"
    ) from e

result = whisper.transcribe(audio)
return result["text"]
```

**Do** validate inputs and provide helpful errors:

```python
# ✅ GOOD
def get_stock_quote(symbol: str) -> Dict:
    """Get stock quote.
    
    Args:
        symbol: Stock symbol (e.g., "AAPL", "GOOGL")
        
    Raises:
        ValueError: If symbol format is invalid
    """
    if not symbol or not symbol.isalpha():
        raise ValueError(
            f"Invalid symbol: {symbol}. "
            "Symbol must be alphabetic (e.g., 'AAPL', 'GOOGL')"
        )
    
    # ... rest of function
```

### 5. Documentation

Every function needs a docstring:

```python
def extract_insights(transcript: str, date: str) -> Dict[str, any]:
    """Extract structured insights from journal transcript using Claude.
    
    Args:
        transcript: Journal entry text
        date: Entry date in format "YYYY-MM-DD HH:MM"
        
    Returns:
        Dictionary with keys: summary, mood, mood_score, key_events,
        wins, challenges, todos, themes, reflection, tomorrow_intention
        
    Raises:
        ValueError: If Claude returns invalid JSON
        anthropic.APIError: If API call fails
    """
    # ... implementation
```

Every project needs a comprehensive README:
- What it does (problem it solves)
- Prerequisites
- Installation steps
- Setup instructions
- Usage examples
- Expected output
- Troubleshooting section
- How it works (technical explanation)

See `README_TEMPLATE.md` for the full template.

## Git Workflow

### Branching Strategy

Create a feature branch for each contribution:

```bash
# Update main branch
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/your-feature-name
# OR
git checkout -b fix/bug-description
```

Branch naming conventions:
- `feature/add-xyz` - New features
- `fix/bug-name` - Bug fixes
- `docs/update-readme` - Documentation updates
- `refactor/improve-xyz` - Code improvements without behavior changes

### Commit Messages

Use [Conventional Commits](https://www.conventionalcommits.org/) format:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

**Examples:**

```bash
# Good commits
git commit -m "feat(pdf-chat): add support for image PDFs with OCR"
git commit -m "fix(stock-agent): handle network timeout errors gracefully"
git commit -m "docs(voice-journal): add troubleshooting section for Windows users"
git commit -m "refactor(resume-analyzer): extract PDF parsing into separate function"

# Bad commits (too vague)
git commit -m "update"
git commit -m "fix bug"
git commit -m "changes"
```

### Commit Frequency

Make **atomic commits** - one logical change per commit:

```bash
# ❌ BAD - All changes in one commit
git add .
git commit -m "feat: add 5 new projects"

# ✅ GOOD - Separate commits for each logical unit
git add 15-project-name/
git commit -m "feat(project-15): add agentic data analyst with pandas tools"

git add 16-project-name/
git commit -m "feat(project-16): add real-time news analyst with RSS feeds"

# Even better - break down a single project into logical commits
git add pdf-chat/requirements.txt pdf-chat/README.md
git commit -m "feat(pdf-chat): initialize project structure and dependencies"

git add pdf-chat/extractor.py
git commit -m "feat(pdf-chat): add PDF text extraction with page markers"

git add pdf-chat/app.py
git commit -m "feat(pdf-chat): add Streamlit chat interface with Claude integration"

git add pdf-chat/app.py
git commit -m "feat(pdf-chat): add conversation history support"
```

### Pull Request Process

1. **Before Opening PR:**
   ```bash
   # Format code
   black .
   
   # Check linting
   ruff check .
   
   # Run any tests (if they exist)
   pytest
   
   # Make sure your branch is up to date
   git checkout main
   git pull origin main
   git checkout your-feature-branch
   git rebase main
   ```

2. **PR Description Template:**
   ```markdown
   ## What This PR Does
   [Brief description of changes]
   
   ## Why This Change
   [Explanation of the problem this solves]
   
   ## Changes Made
   - [ ] Added/Modified X
   - [ ] Updated documentation
   - [ ] Added tests (if applicable)
   
   ## Testing
   [How you tested these changes]
   
   ## Screenshots/Examples
   [If UI changes, include before/after screenshots]
   
   ## Checklist
   - [ ] Code formatted with `black`
   - [ ] Passes `ruff` checks
   - [ ] Added type hints
   - [ ] Updated README if needed
   - [ ] Tested on Python 3.10+
   ```

3. **Review Process:**
   - Address all review comments
   - Push new commits to the same branch
   - Don't force-push unless necessary
   - Be patient and respectful

## Adding New Projects

When adding a new project to the hub:

### 1. Project Structure
```
XX-project-name/
├── README.md              # Use README_TEMPLATE.md
├── requirements.txt       # Pinned versions
├── main_script.py         # Main application
├── .env.example          # Example environment variables
└── tests/ (optional)      # Tests if applicable
```

### 2. Checklist

Before submitting a new project:

- [ ] **Code Quality**
  - [ ] All functions have type hints
  - [ ] Code formatted with `black`
  - [ ] Passes `ruff` linting
  - [ ] No silent failures or fake error responses
  - [ ] Clear error messages with actionable fixes
  
- [ ] **Documentation**
  - [ ] README follows template structure
  - [ ] Installation steps tested on fresh environment
  - [ ] Usage examples provided
  - [ ] Expected output shown
  - [ ] Troubleshooting section included
  - [ ] "How It Works" section explains concepts
  
- [ ] **Dependencies**
  - [ ] `requirements.txt` has pinned versions (`package==1.2.3`)
  - [ ] All dependencies actually used
  - [ ] No unnecessary packages
  
- [ ] **Testing**
  - [ ] Tested on Python 3.10+
  - [ ] Tested with fresh virtual environment
  - [ ] Tested all code paths (success and error cases)
  - [ ] Screenshots/examples updated if UI changed
  
- [ ] **API Keys**
  - [ ] No hardcoded API keys in code
  - [ ] Environment variable validation at startup
  - [ ] Clear error message if key missing
  - [ ] `.env.example` provided

### 3. Project Difficulty Levels

Label your project appropriately:

**Beginner:**
- Single file, < 200 lines
- Uses one external API (e.g., just Claude)
- Minimal error handling needed
- Example: PDF text summarizer

**Intermediate:**
- Multiple files or 200-500 lines
- Uses 2-3 external services
- Requires understanding of async, APIs, or data processing
- Example: Stock market agent with tools

**Advanced:**
- Complex architecture, 500+ lines
- Multiple integrations, streaming, or real-time processing
- Requires system setup (Docker, databases, etc.)
- Example: Multi-agent research system

## Testing Guidelines

### Manual Testing Required

Before submitting:

1. **Fresh Environment Test:**
   ```bash
   # Create new virtual environment
   python -m venv test_env
   source test_env/bin/activate  # or test_env\Scripts\activate on Windows
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Run your project
   python main.py
   ```

2. **Error Path Testing:**
   - Try running without API key
   - Try with invalid inputs
   - Try with network disconnected (if applicable)
   - Make sure error messages are helpful

3. **Cross-Platform Testing** (if possible):
   - Test on both Unix-like systems (macOS/Linux) and Windows
   - Check file paths use `pathlib.Path` not string concatenation
   - Verify line endings are handled correctly

### Automated Tests (Optional but Welcome)

If adding tests:

```python
# tests/test_main.py
import pytest
from main import extract_insights

def test_extract_insights_valid_input():
    """Test that extract_insights returns expected structure."""
    result = extract_insights("I had a good day", "2026-04-16")
    
    assert "summary" in result
    assert "mood" in result
    assert "mood_score" in result
    assert isinstance(result["mood_score"], int)
    assert 1 <= result["mood_score"] <= 10

def test_extract_insights_empty_input():
    """Test that empty input raises appropriate error."""
    with pytest.raises(ValueError):
        extract_insights("", "2026-04-16")
```

## API Key Security

### Never Commit API Keys

Add to `.gitignore`:
```
.env
*.key
secrets/
```

### Use Environment Variables

```python
import os
import sys

# ✅ GOOD - Environment variable
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    print("❌ Error: ANTHROPIC_API_KEY not set")
    print("Get your key at: https://console.anthropic.com")
    sys.exit(1)

# ❌ BAD - Hardcoded key
api_key = "sk-ant-api03-xxx"  # NEVER DO THIS
```

### Provide .env.example

```bash
# .env.example
ANTHROPIC_API_KEY=sk-ant-your-key-here
# Add other required environment variables
```

## Common Mistakes to Avoid

### 1. Silent Failures
```python
# ❌ BAD
try:
    result = api_call()
except:
    result = None  # Hides the error!

# ✅ GOOD
try:
    result = api_call()
except APIError as e:
    print(f"❌ API call failed: {e}")
    sys.exit(1)
```

### 2. Bare Exception Handlers
```python
# ❌ BAD - Catches everything, even KeyboardInterrupt
try:
    risky_operation()
except:
    pass

# ✅ GOOD - Specific exceptions
try:
    risky_operation()
except (ValueError, KeyError) as e:
    logger.error(f"Operation failed: {e}")
    raise
```

### 3. Missing Input Validation
```python
# ❌ BAD - No validation
def process(data):
    return data.upper()

# ✅ GOOD
def process(data: str) -> str:
    if not isinstance(data, str):
        raise TypeError(f"Expected str, got {type(data)}")
    if not data:
        raise ValueError("Empty string not allowed")
    return data.upper()
```

### 4. Unclear Error Messages
```python
# ❌ BAD
raise ValueError("Invalid input")

# ✅ GOOD
raise ValueError(
    f"Invalid symbol: {symbol}. "
    f"Expected format: SYMBOL.NS (NSE) or SYMBOL.BO (BSE). "
    f"Example: RELIANCE.NS"
)
```

## Getting Help

- **Questions:** Open a [Discussion](https://github.com/mahak867/ai-projects-hub/discussions)
- **Bugs:** Open an [Issue](https://github.com/mahak867/ai-projects-hub/issues)
- **Features:** Open an [Issue](https://github.com/mahak867/ai-projects-hub/issues) with "feature request" label

## Code of Conduct

- Be respectful and constructive
- Welcome newcomers
- Focus on the code, not the person
- Assume good intentions
- Help others learn

---

Thank you for contributing! 🎉
