# 🔍 YourAIDetector

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

A comprehensive AI content detection tool that analyzes text from various file formats and provides accurate AI-generation scoring with text highlighting capabilities.

## ✨ Features

- **📄 Multi-Format Support**: Read and analyze content from:
  - PDF files (`.pdf`)
  - Word documents (`.docx`, `.doc`)
  - Text files (`.txt`)
  - Images with OCR (`.png`, `.jpg`, `.jpeg`, `.tiff`, `.bmp`)

- **🎯 Accurate Detection**: Uses multiple analysis methods:
  - Perplexity analysis (sentence complexity)
  - Burstiness detection (variation in sentence structure)
  - Pattern recognition (common AI writing patterns)
  - Vocabulary analysis (word choice and repetition)

- **🎨 Text Highlighting**: Visually identifies suspicious AI-generated segments with:
  - Color-coded terminal output
  - HTML report generation with interactive highlights
  - Detailed reasoning for each suspicious segment

- **⚙️ Configurable**: Adjust detection sensitivity with customizable thresholds

- **🚀 Easy to Use**: Simple CLI interface and Python API

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Install from source

```bash
# Clone the repository
git clone https://github.com/bf20162/YourAIDetector.git
cd YourAIDetector

# Install dependencies
pip install -r requirements.txt

# Optional: Install package
pip install -e .
```

### For OCR support (images)

If you want to analyze images, you also need to install Tesseract OCR:

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr
```

**macOS:**
```bash
brew install tesseract
```

**Windows:**
Download and install from [Tesseract GitHub](https://github.com/UB-Mannheim/tesseract/wiki)

## 🚀 Quick Start

### Command Line Interface

#### Analyze a file:
```bash
python -m aidetector document.pdf
```

#### Analyze text directly:
```bash
python -m aidetector --text "Your text here to analyze for AI generation..."
```

#### Generate HTML report:
```bash
python -m aidetector document.pdf --output report.html
```

#### Adjust detection threshold:
```bash
python -m aidetector document.pdf --threshold 0.7
```

#### View all options:
```bash
python -m aidetector --help
```

### Python API

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

# Highlight suspicious segments
highlighter = TextHighlighter()
summary = highlighter.create_summary(result)
print(summary)

# Generate HTML report
html_report = highlighter.generate_html_report(text, result)
with open('report.html', 'w') as f:
    f.write(html_report)
```

## 📊 Understanding Results

### AI Score
A value between 0.0 and 1.0 indicating the likelihood of AI generation:
- **0.0 - 0.3**: Likely human-written
- **0.3 - 0.5**: Uncertain
- **0.5 - 0.7**: Possibly AI-generated
- **0.7 - 1.0**: Likely AI-generated

### Detection Metrics

The tool analyzes four key metrics:

1. **Perplexity Score**: Measures text complexity and predictability. AI text tends to have lower perplexity.

2. **Burstiness Score**: Analyzes variation in sentence structure. Human writing is typically more "bursty" with varying complexity.

3. **Pattern Score**: Detects common AI writing patterns like formal transitions ("furthermore", "moreover", etc.).

4. **Vocabulary Score**: Examines word choice, repetition, and formality patterns typical of AI models.

### Confidence Level
Indicates how confident the tool is in its assessment (0.0 - 1.0). Higher confidence means the result is more reliable.

## 🎨 Highlighted Output

Suspicious segments are highlighted in different colors based on their AI likelihood:

- 🔴 **Red**: High suspicion (70%+)
- 🟡 **Yellow**: Medium suspicion (50-70%)
- 🟢 **Cyan**: Low suspicion (<50%)

## 📁 Examples

The `examples/` directory contains sample files to test the tool:

- `sample_ai_text.txt`: Example of AI-generated text
- `sample_human_text.txt`: Example of human-written text

Test them:
```bash
python -m aidetector examples/sample_ai_text.txt
python -m aidetector examples/sample_human_text.txt
```

## 🔧 Configuration

### Adjusting Threshold

The detection threshold determines how strict the classification is:

```bash
# More lenient (fewer false positives)
python -m aidetector document.pdf --threshold 0.7

# More strict (catches more potential AI content)
python -m aidetector document.pdf --threshold 0.3
```

Default threshold is 0.5, which provides a good balance.

## 🏗️ Architecture

```
YourAIDetector/
├── aidetector/
│   ├── __init__.py          # Package initialization
│   ├── __main__.py          # Module entry point
│   ├── cli.py               # Command-line interface
│   ├── detector.py          # AI detection engine
│   ├── parser.py            # Document parsing
│   └── highlighter.py       # Text highlighting and reporting
├── examples/                # Example files
├── requirements.txt         # Python dependencies
├── setup.py                 # Package setup
└── README.md               # Documentation
```

## 🧪 How It Works

YourAIDetector uses a multi-faceted approach to detect AI-generated content:

1. **Document Parsing**: Extracts text from various file formats using specialized parsers.

2. **Text Analysis**: Breaks down text into sentences and analyzes:
   - Sentence length uniformity
   - Vocabulary diversity
   - Complexity patterns
   - Common AI phrases and transitions

3. **Scoring**: Combines multiple metrics with weighted scoring:
   - Perplexity: 30%
   - Burstiness: 30%
   - Patterns: 25%
   - Vocabulary: 15%

4. **Highlighting**: Identifies and marks suspicious segments with detailed reasoning.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool provides probabilistic analysis and should not be used as the sole basis for important decisions. AI detection is an evolving field, and no tool is 100% accurate. Always use human judgment in conjunction with automated tools.

## 🔮 Future Enhancements

- [ ] Support for more file formats (RTF, Markdown, HTML)
- [ ] Integration with transformer-based models for improved accuracy
- [ ] Batch processing of multiple files
- [ ] Web-based interface
- [ ] Language detection and multilingual support
- [ ] API endpoint for integration with other tools

## 📧 Contact

For questions, issues, or suggestions, please open an issue on GitHub.

---

Made with ❤️ for the open-source community
