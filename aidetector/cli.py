"""
Command Line Interface for YourAIDetector
==========================================

Main CLI entry point for the AI content detection tool.
"""

import sys
import os
import logging
from pathlib import Path
from typing import Optional

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aidetector.parser import DocumentParser
from aidetector.detector import AIContentDetector
from aidetector.highlighter import TextHighlighter


def setup_logging(verbose: bool = False):
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def print_banner():
    """Print application banner."""
    banner = """
    ╔═══════════════════════════════════════════════════════╗
    ║                                                       ║
    ║           🔍  YourAIDetector v1.0.0  🔍              ║
    ║                                                       ║
    ║       Comprehensive AI Content Detection Tool        ║
    ║                                                       ║
    ╚═══════════════════════════════════════════════════════╝
    """
    print(banner)


def print_help():
    """Print help information."""
    help_text = """
Usage: python -m aidetector.cli [OPTIONS] <file_path_or_text>

Detect AI-generated content in documents or text.

Arguments:
  <file_path_or_text>    Path to document file or text to analyze

Options:
  --file, -f             Analyze a file (default if path exists)
  --text, -t             Analyze text directly
  --threshold FLOAT      Detection threshold (0.0-1.0, default: 0.5)
  --output, -o PATH      Output HTML report to file
  --no-color             Disable colored output
  --verbose, -v          Enable verbose logging
  --help, -h             Show this help message

Supported File Formats:
  - PDF (.pdf)
  - Word Documents (.docx, .doc)
  - Text Files (.txt)
  - Images with OCR (.png, .jpg, .jpeg, .tiff, .bmp)

Examples:
  # Analyze a PDF file
  python -m aidetector.cli document.pdf

  # Analyze text directly
  python -m aidetector.cli --text "Your text here..."

  # Generate HTML report
  python -m aidetector.cli document.pdf --output report.html

  # Adjust detection threshold
  python -m aidetector.cli document.pdf --threshold 0.7

  # Disable colors
  python -m aidetector.cli document.pdf --no-color
"""
    print(help_text)


def analyze_file(file_path: str, threshold: float = 0.5, 
                output_path: Optional[str] = None, use_colors: bool = True):
    """
    Analyze a document file for AI-generated content.
    
    Args:
        file_path: Path to the document file
        threshold: Detection threshold
        output_path: Optional path to save HTML report
        use_colors: Whether to use colored output
    """
    print(f"\n📄 Analyzing file: {file_path}\n")
    
    # Parse document
    parser = DocumentParser()
    
    try:
        doc_data = parser.parse(file_path)
        text = doc_data['text']
        
        print(f"✓ Document parsed successfully")
        print(f"  Format: {doc_data['format']}")
        print(f"  Text length: {len(text)} characters")
        
        if 'pages' in doc_data:
            print(f"  Pages: {doc_data['pages']}")
        elif 'paragraphs' in doc_data:
            print(f"  Paragraphs: {doc_data['paragraphs']}")
        
        print()
        
    except Exception as e:
        print(f"❌ Error parsing file: {e}")
        return 1
    
    # Analyze content
    return analyze_text(text, threshold, output_path, use_colors)


def analyze_text(text: str, threshold: float = 0.5,
                output_path: Optional[str] = None, use_colors: bool = True):
    """
    Analyze text for AI-generated content.
    
    Args:
        text: Text to analyze
        threshold: Detection threshold
        output_path: Optional path to save HTML report
        use_colors: Whether to use colored output
    """
    print("🔍 Running AI detection analysis...")
    
    # Detect AI content
    detector = AIContentDetector(threshold=threshold)
    
    try:
        result = analyzer = detector.analyze(text)
        print("✓ Analysis complete\n")
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        return 1
    
    # Create highlighter
    highlighter = TextHighlighter(use_colors=use_colors)
    
    # Print summary
    summary = highlighter.create_summary(result)
    print(summary)
    
    # Print highlighted text
    if result.get('details', {}).get('suspicious_segments'):
        print("\n📝 Text with highlighted suspicious segments:\n")
        print("-" * 80)
        highlighted = highlighter.highlight_text(text, result['details']['suspicious_segments'])
        print(highlighted)
        print("-" * 80)
    
    # Generate HTML report if requested
    if output_path:
        try:
            html_report = highlighter.generate_html_report(text, result)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_report)
            
            print(f"\n✓ HTML report saved to: {output_path}")
        except Exception as e:
            print(f"\n❌ Error saving HTML report: {e}")
            return 1
    
    return 0


def main():
    """Main CLI entry point."""
    args = sys.argv[1:]
    
    # Parse arguments manually (simple argument parsing)
    if not args or '--help' in args or '-h' in args:
        print_banner()
        print_help()
        return 0
    
    # Default values
    threshold = 0.5
    output_path = None
    use_colors = True
    verbose = False
    is_file = True
    input_data = None
    
    # Parse arguments
    i = 0
    while i < len(args):
        arg = args[i]
        
        if arg in ['--threshold']:
            i += 1
            if i < len(args):
                try:
                    threshold = float(args[i])
                    if not 0.0 <= threshold <= 1.0:
                        print("❌ Error: Threshold must be between 0.0 and 1.0")
                        return 1
                except ValueError:
                    print("❌ Error: Invalid threshold value")
                    return 1
        
        elif arg in ['--output', '-o']:
            i += 1
            if i < len(args):
                output_path = args[i]
        
        elif arg in ['--text', '-t']:
            is_file = False
            i += 1
            if i < len(args):
                input_data = args[i]
        
        elif arg == '--no-color':
            use_colors = False
        
        elif arg in ['--verbose', '-v']:
            verbose = True
        
        elif arg in ['--file', '-f']:
            is_file = True
            i += 1
            if i < len(args):
                input_data = args[i]
        
        elif not arg.startswith('--') and not arg.startswith('-'):
            # Assume it's the input data
            if input_data is None:
                # Auto-detect if it's a file or text
                if os.path.exists(arg):
                    is_file = True
                    input_data = arg
                else:
                    is_file = False
                    input_data = arg
        
        i += 1
    
    # Setup logging
    setup_logging(verbose)
    
    # Print banner
    print_banner()
    
    # Validate input
    if input_data is None:
        print("❌ Error: No input provided")
        print("Use --help for usage information")
        return 1
    
    # Process input
    try:
        if is_file:
            return analyze_file(input_data, threshold, output_path, use_colors)
        else:
            return analyze_text(input_data, threshold, output_path, use_colors)
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Analysis interrupted by user")
        return 130
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        if verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
