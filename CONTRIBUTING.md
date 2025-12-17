# Contributing to AWS EC2 Cost Analyzer

Thank you for your interest in contributing to the AWS EC2 Cost Analyzer! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Issues

1. **Search existing issues** first to avoid duplicates
2. **Use the issue template** when creating new issues
3. **Provide detailed information**:
   - Operating system and version
   - Python version
   - AWS region
   - Error messages (full stack trace)
   - Steps to reproduce

### Suggesting Features

1. **Check existing feature requests** to avoid duplicates
2. **Describe the use case** and why it would be valuable
3. **Provide examples** of how the feature would work
4. **Consider implementation complexity** and maintenance burden

### Code Contributions

#### Development Setup

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/aws-ec2-cost-analyzer.git
   cd aws-ec2-cost-analyzer
   ```

2. **Set up development environment**
   ```cmd
   setup.bat
   ```

3. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

#### Code Standards

- **Python Style**: Follow PEP 8 guidelines
- **Documentation**: Add docstrings for all functions and classes
- **Comments**: Use clear, concise comments for complex logic
- **Error Handling**: Include appropriate exception handling
- **Testing**: Test your changes thoroughly

#### Batch Script Guidelines

- **Encoding**: Use UTF-8 without BOM to avoid character issues
- **Error Handling**: Include proper error checking and user feedback
- **Comments**: Use REM for comments, keep them clear and helpful
- **Compatibility**: Ensure compatibility with Windows 10/11

#### Pull Request Process

1. **Update documentation** if needed
2. **Test thoroughly** on Windows environment
3. **Update CHANGELOG.md** with your changes
4. **Create pull request** with:
   - Clear title and description
   - Reference to related issues
   - Screenshots if UI changes
   - Testing information

## 🧪 Testing

### Manual Testing

1. **Test all batch scripts** in clean environment
2. **Verify AWS integration** with different regions
3. **Test error scenarios**:
   - Invalid credentials
   - Network issues
   - Missing permissions
   - Invalid parameters

### Test Cases to Cover

- [ ] Fresh installation on clean Windows system
- [ ] Python auto-detection with various Python installations
- [ ] AWS authentication methods (CLI, environment variables, IAM roles)
- [ ] Different AWS regions
- [ ] Various instance types and sizes
- [ ] Edge cases (no instances, all stopped instances, etc.)

## 📝 Documentation

### Code Documentation

- **Docstrings**: Use Google-style docstrings
- **Type hints**: Include type hints for function parameters and returns
- **Comments**: Explain complex business logic and AWS-specific concepts

### User Documentation

- **README updates**: Keep README.md current with new features
- **Examples**: Provide clear, working examples
- **Troubleshooting**: Add common issues and solutions

## 🐛 Bug Reports

### Information to Include

1. **Environment details**:
   - Windows version
   - Python version (`python --version`)
   - AWS CLI version (`aws --version`)

2. **Steps to reproduce**:
   - Exact commands run
   - Configuration used
   - Expected vs actual behavior

3. **Error information**:
   - Full error messages
   - Log files if available
   - Screenshots if helpful

## 💡 Feature Requests

### Good Feature Requests Include

- **Clear problem statement**: What problem does this solve?
- **Use cases**: Who would benefit and how?
- **Proposed solution**: How should it work?
- **Alternatives considered**: What other approaches were considered?

### Feature Categories

- **Analysis improvements**: Better cost calculations, new metrics
- **Reporting enhancements**: New output formats, visualizations
- **Usability improvements**: Better error messages, setup automation
- **Platform support**: Support for other operating systems
- **Integration features**: API endpoints, webhook notifications

## 🔄 Release Process

### Version Numbering

We use [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes
- **MINOR**: New features, backwards compatible
- **PATCH**: Bug fixes, backwards compatible

### Changelog

All notable changes are documented in CHANGELOG.md following [Keep a Changelog](https://keepachangelog.com/) format.

## 📞 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **Discussions**: For questions and general discussion
- **Email**: For security issues or private matters

## 🏆 Recognition

Contributors will be recognized in:
- README.md acknowledgments section
- CHANGELOG.md for significant contributions
- GitHub contributors page

## 📋 Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/). By participating, you agree to uphold this code.

### Our Standards

- **Be respectful** and inclusive
- **Be constructive** in feedback
- **Focus on the project** goals
- **Help others** learn and contribute

Thank you for contributing to AWS EC2 Cost Analyzer! 🎉