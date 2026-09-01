# Contributing Guidelines

## Getting Started

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Code Style

Follow PEP 8:
- Maximum line length: 100 characters
- Use type hints
- Use descriptive names

### Code Quality Tools

```bash
black . --line-length=100
isort .
flake8 . --max-line-length=100
pylint bot/ database/ github_api/
```

## Commit Messages

```
<type>(<scope>): <subject>

<body>

<footer>
```

## Pull Request Checklist

- Code follows style guidelines
- Self-review completed
- Comments added for complex logic
- Documentation updated
- Tests passing

## Areas for Contribution

- New features
- Bug fixes
- Documentation
- Tests
- Performance improvements
- Security fixes

---

**Thank you for contributing!**
