# Contributing to YourAIDetector

Thank you for your interest in contributing to YourAIDetector! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

By participating in this project, you agree to:
- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards other community members

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- A clear, descriptive title
- Steps to reproduce the bug
- Expected vs. actual behavior
- Your environment (OS, Python version, etc.)
- Sample text or file that causes the issue (if applicable)

### Suggesting Enhancements

Enhancement suggestions are welcome! Please include:
- A clear description of the enhancement
- Why it would be useful
- Example use cases
- Potential implementation approach (if you have one)

### Pull Requests

1. **Fork the repository**
   ```bash
   git clone https://github.com/bf20162/YourAIDetector.git
   cd YourAIDetector
   ```

2. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Write clear, readable code
   - Follow the existing code style
   - Add comments for complex logic
   - Update documentation as needed

4. **Test your changes**
   ```bash
   python examples/test_detector.py
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Brief description of changes"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Open a Pull Request**
   - Provide a clear title and description
   - Reference any related issues
   - Explain the changes and their benefits

## Development Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git

### Setting Up Development Environment

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/YourAIDetector.git
cd YourAIDetector

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
python examples/test_detector.py
```

## Code Style Guidelines

### Python Code Style

Follow PEP 8 guidelines with these specifics:

1. **Indentation**: 4 spaces (no tabs)
2. **Line Length**: Maximum 100 characters
3. **Imports**: Group in order: standard library, third-party, local
4. **Naming Conventions**:
   - Classes: `CamelCase`
   - Functions/methods: `snake_case`
   - Constants: `UPPER_CASE`
   - Private methods: `_leading_underscore`

### Documentation

- Add docstrings to all public functions, classes, and modules
- Use clear, descriptive variable names
- Comment complex logic

Example:
```python
def analyze_text(text: str, threshold: float = 0.5) -> Dict[str, Any]:
    """
    Analyze text for AI-generated content.
    
    Args:
        text: Text to analyze
        threshold: Detection threshold (0.0 to 1.0)
        
    Returns:
        Dictionary containing analysis results
        
    Raises:
        ValueError: If text is empty or threshold is invalid
    """
    # Implementation here
    pass
```

## Testing

### Running Tests

```bash
# Run the test suite
python examples/test_detector.py

# Test specific functionality
python -m aidetector examples/sample_ai_text.txt
python -m aidetector examples/sample_human_text.txt
```

### Adding Tests

When adding new features, include tests:

```python
def test_new_feature():
    """Test description."""
    # Setup
    detector = AIContentDetector()
    
    # Execute
    result = detector.new_feature()
    
    # Verify
    assert result is not None, "Result should not be None"
    print("✓ Test passed: new_feature works correctly")
```

## Project Structure

```
YourAIDetector/
├── aidetector/           # Main package
│   ├── __init__.py      # Package initialization
│   ├── __main__.py      # Module entry point
│   ├── cli.py           # Command-line interface
│   ├── detector.py      # AI detection engine
│   ├── parser.py        # Document parsing
│   └── highlighter.py   # Text highlighting
├── examples/            # Example files and tests
├── README.md           # Main documentation
├── USAGE_GUIDE.md      # Detailed usage guide
├── requirements.txt    # Python dependencies
└── setup.py           # Package setup
```

## Areas for Contribution

We welcome contributions in these areas:

### High Priority
- [ ] Support for additional file formats (RTF, Markdown, HTML)
- [ ] Improved accuracy with transformer-based models
- [ ] Performance optimizations for large documents
- [ ] Multilingual support

### Medium Priority
- [ ] Web-based interface
- [ ] Batch processing improvements
- [ ] API endpoint for integration
- [ ] Enhanced visualization of results

### Nice to Have
- [ ] Plugin system for custom detectors
- [ ] Export results in various formats (JSON, CSV)
- [ ] Integration with popular writing tools
- [ ] Real-time analysis for streaming text

## Questions?

If you have questions about contributing:
- Open an issue with the "question" label
- Check existing issues for similar questions
- Review the documentation

## Recognition

Contributors will be recognized in:
- The project README
- Release notes
- GitHub contributors page

Thank you for helping make YourAIDetector better!
