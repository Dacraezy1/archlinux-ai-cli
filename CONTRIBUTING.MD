# Contributing to Arch Linux AI CLI

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## 🎯 How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- **Clear title**: Describe the issue in one sentence
- **Steps to reproduce**: List exact steps to reproduce the behavior
- **Expected behavior**: What you expected to happen
- **Actual behavior**: What actually happened
- **Environment**:
  - Arch Linux version: `uname -r`
  - Python version: `python --version`
  - Package versions: `pip list | grep -E "google-generativeai|requests"`
- **Logs/Error messages**: Include relevant error output

### Suggesting Features

Feature suggestions are welcome! Please:

1. Check if the feature has already been suggested
2. Provide a clear use case
3. Explain how it benefits Arch Linux users
4. Consider implementation complexity

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the code style (PEP 8 for Python)
   - Add comments for complex logic
   - Update documentation if needed

4. **Test your changes**
   - Test on a real Arch Linux system
   - Try multiple use cases
   - Check edge cases

5. **Commit your changes**
   ```bash
   git commit -m "Add: brief description of changes"
   ```
   
   Use conventional commit messages:
   - `Add:` for new features
   - `Fix:` for bug fixes
   - `Update:` for updates to existing features
   - `Docs:` for documentation changes
   - `Refactor:` for code refactoring

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Open a Pull Request**
   - Describe what your PR does
   - Reference any related issues
   - Include testing steps

## 📝 Code Style Guidelines

### Python Code

- Follow PEP 8 style guide
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions focused and small
- Use type hints where appropriate

Example:
```python
def search_wiki(query: str, limit: int = 5) -> Optional[dict]:
    """
    Search the Arch Wiki for relevant pages.
    
    Args:
        query: Search term to look for
        limit: Maximum number of results to return
        
    Returns:
        Dictionary with search results or None if failed
    """
    # Implementation here
```

### Documentation

- Keep README.md up to date
- Use clear, concise language
- Include examples for new features
- Update help text in argparse if adding options

## 🔍 Testing Guidelines

Before submitting a PR, test:

1. **Basic functionality**
   - Single query mode works
   - Interactive mode works
   - History feature works

2. **Edge cases**
   - Empty queries
   - Very long queries
   - Network failures
   - Invalid API keys

3. **Safety features**
   - Dangerous commands get warnings
   - System stability advice is sound

## 🚫 What NOT to Do

- Don't suggest commands that could harm Arch systems without clear warnings
- Don't bypass safety features
- Don't include hardcoded API keys
- Don't add unnecessary dependencies
- Don't submit untested code
- Don't copy code without proper attribution

## 💡 Ideas for Contributions

### Good First Issues

- Improve error messages
- Add more examples to README
- Enhance Wiki search results parsing
- Add colored output support
- Improve command explanations

### Advanced Contributions

- Add caching for Wiki searches
- Implement offline mode with cached data
- Add support for other AI models
- Create a man page
- Add bash/zsh completion scripts
- Implement logging system
- Add configuration file support

## 🏗️ Architecture Guidelines

### Keep It Simple

- This is a CLI tool - keep it lightweight
- Minimize dependencies
- Avoid over-engineering
- Prioritize user experience

### Safety First

- Always validate user input
- Warn before dangerous operations
- Provide accurate information
- Reference official documentation

### Arch Linux Focus

- Stay true to Arch principles (KISS, user-centric)
- Reference Arch Wiki as primary source
- Use Arch-specific tools and conventions
- Support the Arch way of doing things

## 📋 PR Checklist

Before submitting, ensure:

- [ ] Code follows PEP 8 style guidelines
- [ ] All functions have docstrings
- [ ] Changes are tested on Arch Linux
- [ ] Documentation is updated
- [ ] No hardcoded credentials
- [ ] Commit messages are clear
- [ ] PR description explains the changes
- [ ] No breaking changes (or clearly documented)

## 🤔 Questions?

If you have questions about contributing:

1. Check existing issues and PRs
2. Open a discussion on GitHub
3. Reach out in the issue tracker

## 📜 Code of Conduct

- Be respectful and constructive
- Welcome newcomers
- Focus on the code, not the person
- Help maintain a positive community

## 🙏 Recognition

All contributors will be recognized in the project. Significant contributions may be highlighted in release notes.

---

Thank you for contributing to Arch Linux AI CLI! 🚀
