# YourAIDetector - Usage Guide

## Table of Contents
1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Command Line Usage](#command-line-usage)
4. [Python API](#python-api)
5. [Understanding Results](#understanding-results)
6. [Advanced Features](#advanced-features)
7. [Troubleshooting](#troubleshooting)

## Installation

### Basic Installation

```bash
# Clone the repository
git clone https://github.com/bf20162/YourAIDetector.git
cd YourAIDetector

# Install core dependencies
pip install numpy scipy

# Optional: Install all dependencies for full functionality
pip install -r requirements.txt
```

### For OCR Support (Images)

If you want to analyze images, install Tesseract OCR:

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr
```

**macOS:**
```bash
brew install tesseract
```

**Windows:**
Download from [Tesseract GitHub](https://github.com/UB-Mannheim/tesseract/wiki)

## Quick Start

### Analyze a text file
```bash
python -m aidetector examples/sample_ai_text.txt
```

### Analyze text directly
```bash
python -m aidetector --text "Your text here"
```

### Generate HTML report
```bash
python -m aidetector document.pdf --output report.html
```

## Command Line Usage

### Basic Syntax
```bash
python -m aidetector [OPTIONS] <file_or_text>
```

### Options

- `--file, -f PATH`: Analyze a file (auto-detected if path exists)
- `--text, -t TEXT`: Analyze text directly
- `--threshold FLOAT`: Detection threshold (0.0-1.0, default: 0.5)
- `--output, -o PATH`: Save HTML report to file
- `--no-color`: Disable colored terminal output
- `--verbose, -v`: Enable verbose logging
- `--help, -h`: Show help message

### Examples

#### Example 1: Analyze a PDF with custom threshold
```bash
python -m aidetector research_paper.pdf --threshold 0.7
```

#### Example 2: Generate HTML report
```bash
python -m aidetector essay.docx --output report.html
```

#### Example 3: Analyze text with verbose output
```bash
python -m aidetector --text "Your text here" --verbose
```

#### Example 4: Analyze an image (OCR)
```bash
python -m aidetector screenshot.png
```

## Python API

### Basic Usage

```python
from aidetector import AIContentDetector, DocumentParser, TextHighlighter

# Parse a document
parser = DocumentParser()
doc_data = parser.parse('document.pdf')
text = doc_data['text']

# Analyze for AI content
detector = AIContentDetector(threshold=0.5)
result = detector.analyze(text)

print(f"AI Score: {result['ai_score']}")
print(f"Is AI Generated: {result['is_ai_generated']}")
print(f"Confidence: {result['confidence']}")
```

### Advanced Usage

```python
from aidetector import AIContentDetector, TextHighlighter

# Analyze text
text = "Your text to analyze..."
detector = AIContentDetector(threshold=0.5)
result = detector.analyze(text)

# Create detailed summary
highlighter = TextHighlighter(use_colors=True)
summary = highlighter.create_summary(result)
print(summary)

# Generate HTML report
html_report = highlighter.generate_html_report(text, result)
with open('report.html', 'w', encoding='utf-8') as f:
    f.write(html_report)

# Highlight text in terminal
highlighted = highlighter.highlight_text(text, result['details']['suspicious_segments'])
print(highlighted)
```

### Supported Document Formats

```python
from aidetector import DocumentParser

parser = DocumentParser()

# Check if format is supported
parser.is_supported('document.pdf')  # True
parser.is_supported('image.png')     # True
parser.is_supported('text.xyz')      # False

# Parse different formats
pdf_data = parser.parse('document.pdf')
docx_data = parser.parse('essay.docx')
txt_data = parser.parse('notes.txt')
img_data = parser.parse('screenshot.png')  # Requires Tesseract OCR
```

## Understanding Results

### AI Score Interpretation

The AI score ranges from 0.0 to 1.0:

| Score Range | Interpretation |
|-------------|----------------|
| 0.0 - 0.3   | Likely human-written |
| 0.3 - 0.5   | Uncertain (borderline) |
| 0.5 - 0.7   | Possibly AI-generated |
| 0.7 - 1.0   | Likely AI-generated |

### Confidence Level

- **High Confidence (> 0.6)**: The result is reliable
- **Medium Confidence (0.3 - 0.6)**: Result is moderately reliable
- **Low Confidence (< 0.3)**: Result may be uncertain

### Analysis Metrics

1. **Perplexity Score**: Measures text complexity and predictability
   - Higher = More uniform/predictable (AI-like)
   - Lower = More varied/unpredictable (human-like)

2. **Burstiness Score**: Analyzes variation in sentence structure
   - Higher = Less variation (AI-like)
   - Lower = More variation (human-like)

3. **Pattern Score**: Detects common AI writing patterns
   - Higher = More AI patterns detected
   - Examples: "Furthermore", "Moreover", "In conclusion"

4. **Vocabulary Score**: Examines word choice and repetition
   - Higher = More repetitive/formal (AI-like)
   - Lower = More diverse/casual (human-like)

### Suspicious Segments

The tool identifies specific text segments that are likely AI-generated:

- **High Suspicion (70%+)**: Very likely AI-generated
- **Medium Suspicion (50-70%)**: Moderately suspicious
- **Low Suspicion (<50%)**: Slightly suspicious

Each segment includes:
- The suspicious text
- Suspicion score
- Reasons for flagging

## Advanced Features

### Adjusting Detection Sensitivity

```bash
# Strict detection (fewer false positives)
python -m aidetector document.pdf --threshold 0.7

# Lenient detection (catches more potential AI content)
python -m aidetector document.pdf --threshold 0.3
```

### Batch Processing

```python
import os
from aidetector import DocumentParser, AIContentDetector

detector = AIContentDetector()
parser = DocumentParser()

results = {}
for filename in os.listdir('documents/'):
    if filename.endswith(('.pdf', '.docx', '.txt')):
        filepath = os.path.join('documents/', filename)
        doc_data = parser.parse(filepath)
        result = detector.analyze(doc_data['text'])
        results[filename] = result

# Print summary
for filename, result in results.items():
    print(f"{filename}: AI Score = {result['ai_score']:.2f}")
```

### Custom Thresholds for Different Use Cases

```python
from aidetector import AIContentDetector

# Academic paper review (strict)
academic_detector = AIContentDetector(threshold=0.7)

# Social media content (lenient)
social_detector = AIContentDetector(threshold=0.3)

# General purpose (balanced)
general_detector = AIContentDetector(threshold=0.5)
```

## Troubleshooting

### Common Issues

#### 1. Import Error: Module not found

**Solution:**
```bash
pip install numpy scipy
```

#### 2. PDF parsing fails

**Solution:**
```bash
pip install pypdf
```

#### 3. DOCX parsing fails

**Solution:**
```bash
pip install python-docx
```

#### 4. Image OCR fails

**Solution:**
- Install Tesseract OCR (see Installation section)
- Install Python dependencies:
```bash
pip install pytesseract Pillow
```

#### 5. "Text too short for reliable analysis"

**Solution:**
The text needs at least 3 sentences for accurate analysis. Try combining multiple short texts or use longer samples.

#### 6. Low confidence results

**Solution:**
- Text may be genuinely borderline between human and AI
- Try analyzing more text from the same source
- Adjust threshold based on your use case

### Getting Help

If you encounter issues:
1. Check the error message and try the solutions above
2. Enable verbose mode: `python -m aidetector --verbose yourfile.txt`
3. Open an issue on GitHub with:
   - Error message
   - Command you ran
   - Python version and OS
   - Sample of the problematic text (if applicable)

## Best Practices

1. **Use adequate text samples**: At least 100 words recommended
2. **Consider the context**: Academic vs. casual writing have different patterns
3. **Don't rely solely on the tool**: Use human judgment alongside automated detection
4. **Adjust threshold based on needs**: Stricter for critical decisions, lenient for screening
5. **Review suspicious segments**: Understand why text was flagged

## Limitations

- Detection is probabilistic, not definitive
- Works best with English text
- May struggle with technical jargon or specialized vocabulary
- Short texts (< 50 words) may not be reliably analyzed
- Some human writing can resemble AI patterns and vice versa

## Contributing

We welcome contributions! Please see the main README for guidelines.

## License

This project is licensed under the GNU General Public License v3.0.
