# Contributing to DocMemory

First off, **thank you** for considering contributing to DocMemory! 🙌

We take and we give hands — that's the spirit of this project. Whether you're fixing a typo, reporting a bug, or proposing a major feature, your contribution is valued.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Guidelines](#coding-guidelines)
- [Commit Messages](#commit-messages)
- [Pull Request Process](#pull-request-process)
- [Areas Needing Help](#areas-needing-help)

---

## Code of Conduct

### Our Pledge

We are committed to making participation in this project a harassment-free experience for everyone, regardless of:
- Age, body size, disability, ethnicity
- Gender identity and expression
- Level of experience
- Nationality, personal appearance, race, religion
- Sexual identity and orientation

### Our Standards

**Positive behaviors:**
- ✅ Using welcoming and inclusive language
- ✅ Being respectful of differing viewpoints
- ✅ Gracefully accepting constructive criticism
- ✅ Focusing on what's best for the community
- ✅ Showing empathy towards others

**Unacceptable behaviors:**
- ❌ Trolling, insulting/derogatory comments
- ❌ Public or private harassment
- ❌ Publishing others' private information
- ❌ Other conduct which could reasonably be considered inappropriate

---

## How Can I Contribute?

### 🐛 Reporting Bugs

Before creating a bug report:
1. **Check existing issues** — someone may have already reported it
2. **Verify it's actually a bug** — expected behavior vs actual behavior
3. **Collect details** — version, OS, Python version, error messages

**Good bug report includes:**
```markdown
**Description:** Clear description of the bug

**Steps to Reproduce:**
1. Initialize system with...
2. Add document with...
3. Search for...
4. See error

**Expected Behavior:** What should happen

**Actual Behavior:** What actually happens

**Environment:**
- DocMemory version: 1.0.0
- Python version: 3.9.5
- OS: Ubuntu 22.04

**Error Message/Stack Trace:**
```
[paste full error here]
```

**Additional Context:** Screenshots, logs, etc.
```

### 💡 Suggesting Enhancements

Have an idea? Great! Here's how to propose it:

1. **Check roadmap** — might already be planned
2. **Search existing suggestions** — avoid duplicates
3. **Explain the use case** — why is this needed?
4. **Provide examples** — mock code, screenshots, workflows

**Enhancement template:**
```markdown
**Feature Request:** [concise title]

**Problem:** What problem does this solve?

**Proposed Solution:** How should it work?

**Alternatives Considered:** Other approaches you thought about

**Implementation Ideas:** (Optional) Technical approach
```

### 📝 Improving Documentation

Documentation improvements are **always welcome**:
- Fixing typos or unclear explanations
- Adding examples or tutorials
- Translating documentation
- Improving docstrings in code

**No contribution is too small!**

### 🔧 Code Contributions

Ready to write code? Here's the workflow:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Make your changes**
4. **Test your changes**
5. **Commit with clear message**
6. **Push to your fork**
7. **Open a Pull Request**

---

## Development Setup

### Prerequisites

```bash
# Python 3.8 or higher
python --version

# Git
git --version
```

### Local Setup

```bash
# 1. Fork and clone
git clone https://github.com/DocSynapse/Synapse-DocMemory.git
cd Synapse-DocMemory

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install in development mode
pip install -e .

# 4. Install development dependencies
pip install -r requirements-dev.txt

# 5. Run tests (once test suite exists)
pytest tests/

# 6. Verify installation
python -c "from main import DocMemorySystem; print('Success!')"
```

### Project Structure

```
docmemory/
├── src/                     # Core library
│   ├── docmemory_core.py
│   ├── search_engine.py
│   ├── document_processor.py
│   └── auto_save_load.py
├── backend/                 # FastAPI backend
├── frontend/                # Next.js frontend
├── tests/                   # Test suite
├── docs/                    # Documentation
├── main.py                  # Main entry point
├── requirements.txt
├── pyproject.toml
└── README.md
```

---

## Coding Guidelines

### Python Style

We follow [PEP 8](https://peps.python.org/pep-0008/) with some flexibility:

**Key rules:**
- ✅ 4 spaces for indentation (no tabs)
- ✅ Line length: aim for 88 chars (Black default), max 100
- ✅ Use descriptive variable names
- ✅ Add docstrings to functions and classes
- ✅ Type hints where they add clarity

**Tools we use:**
- `black` — code formatting
- `isort` — import sorting
- `flake8` — linting
- `mypy` — type checking (optional)

```bash
# Format your code before committing
black src/ backend/
isort src/ backend/
flake8 src/ backend/
```

### Docstring Format

We use Google-style docstrings:

```python
def search_documents(query: str, limit: int = 10) -> List[Dict]:
    """Search documents using hybrid semantic and keyword search.
    
    Args:
        query: Search query string
        limit: Maximum number of results to return (default: 10)
    
    Returns:
        List of dictionaries containing document metadata and scores
    
    Raises:
        ValueError: If query is empty or limit is negative
    
    Example:
        >>> results = search_documents("machine learning", limit=5)
        >>> for result in results:
        ...     print(result['title'])
    """
```

### Testing

**Writing tests:**
```python
import pytest
from main import DocMemorySystem

def test_document_ingestion():
    """Test basic document ingestion and retrieval"""
    system = DocMemorySystem(storage_path="./test_storage/")
    
    # Add test document
    doc_ids = system.add_document_from_file(
        "test_data/sample.txt",
        title="Test Doc"
    )
    
    assert len(doc_ids) > 0
    
    # Verify retrieval
    doc = system.get_document(doc_ids[0])
    assert doc.title == "Test Doc"
    
    # Cleanup
    system.close()
```

---

## Commit Messages

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

**Good commits:**
```
feat(search): add BM25 ranking algorithm

Implements BM25 relevance scoring for keyword search to improve 
result quality over simple term frequency.

Closes #42
```

```
fix(processor): handle Unicode encoding errors in PDF extraction

Adds fallback encoding detection for PDFs with non-UTF-8 text.

Fixes #38
```

```
docs(readme): add installation troubleshooting section

Added common installation issues and solutions based on user feedback.
```

**Bad commits:**
```
Update stuff
Fixed bug
Changes
```

---

## Pull Request Process

### Before Submitting

- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated if needed
- [ ] Tests added/updated (when test suite exists)
- [ ] All tests pass locally
- [ ] No new warnings introduced

### PR Description Template

```markdown
## Description
[Clear explanation of what this PR does]

## Type of Change
- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New feature (non-breaking change adding functionality)
- [ ] Breaking change (fix or feature causing existing functionality to break)
- [ ] Documentation update

## How Has This Been Tested?
[Describe testing performed]

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added where needed
- [ ] Documentation updated
- [ ] No new warnings

## Related Issues
Closes #[issue number]
```

### Review Process

1. **Maintainer reviews** within 3-7 days
2. **Feedback provided** — may request changes
3. **Discussion** — collaborate on best approach
4. **Approval and merge** — once changes approved

**Be patient and respectful during review!**

---

## Areas Needing Help

### High Priority

- [ ] **Testing Suite** — comprehensive unit and integration tests
- [ ] **Error Handling** — robust error messages and recovery
- [ ] **Performance Benchmarks** — formal performance testing
- [ ] **Documentation** — more examples and tutorials

### Medium Priority

- [ ] **CLI Tool** — command-line interface for quick operations
- [ ] **More File Formats** — Markdown, LaTeX, EPUB support
- [ ] **Docker Support** — containerized deployment
- [ ] **Configuration System** — YAML/JSON config files

### Low Priority (But Still Valuable!)

- [ ] **Web UI** — simple web interface for document exploration
- [ ] **API Endpoints** — REST API for remote access
- [ ] **Graph Visualization** — visual relationship explorer
- [ ] **Multi-language Support** — internationalization

---

## Questions?

**Not sure where to start?**
- Check [Good First Issues](https://github.com/DocSynapse/Synapse-DocMemory/labels/good%20first%20issue)
- Ask in [Discussions](https://github.com/DocSynapse/Synapse-DocMemory/discussions)
- Reach out via email: your.email@example.com

**Need clarification?**
- Don't hesitate to ask questions in your issue/PR
- We're here to help you contribute successfully!

---

## Attribution

Contributors are recognized in:
- Git commit history
- GitHub contributors page
- Release notes
- Special mentions for significant contributions

---

## Thank You!

Your contribution, no matter how small, makes DocMemory better for everyone. 

**We take and we give hands.** 🤝

Let's build something great together!

---

*This contribution guide is inspired by successful open source projects and adapted for our community-first philosophy.*
