#!/usr/bin/env python3
"""
Simple test script for YourAIDetector
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aidetector import AIContentDetector, DocumentParser, TextHighlighter


def test_ai_text():
    """Test with AI-like text."""
    print("\n" + "=" * 60)
    print("TEST 1: AI-Generated Text")
    print("=" * 60)
    
    ai_text = """
    The advancement of technology has significantly transformed modern society. 
    Furthermore, artificial intelligence has emerged as a pivotal force in this 
    transformation. Moreover, the integration of AI systems into various sectors 
    demonstrates remarkable potential. In conclusion, it is important to note that 
    these developments will continue to shape our future. Additionally, machine 
    learning algorithms have shown unprecedented capabilities. Therefore, the 
    impact on our daily lives will be profound and far-reaching.
    """
    
    detector = AIContentDetector(threshold=0.5)
    result = detector.analyze(ai_text)
    
    highlighter = TextHighlighter(use_colors=True)
    summary = highlighter.create_summary(result)
    print(summary)
    
    assert result['ai_score'] > 0.5, "AI text should have high score"
    print("✓ Test passed: AI text correctly detected")


def test_human_text():
    """Test with human-like text."""
    print("\n" + "=" * 60)
    print("TEST 2: Human-Written Text")
    print("=" * 60)
    
    human_text = """
    I went to the store today. Needed milk and eggs. The line was crazy long! 
    Waited like 20 minutes. Guy in front of me bought SO many things. I was 
    getting impatient. Finally got home. Made breakfast. Eggs were perfect. 
    Now I'm just chilling watching TV. Life's good.
    """
    
    detector = AIContentDetector(threshold=0.5)
    result = detector.analyze(human_text)
    
    highlighter = TextHighlighter(use_colors=True)
    summary = highlighter.create_summary(result)
    print(summary)
    
    assert result['ai_score'] < 0.6, "Human text should have lower score"
    print("✓ Test passed: Human text correctly identified")


def test_document_parser():
    """Test document parser."""
    print("\n" + "=" * 60)
    print("TEST 3: Document Parser")
    print("=" * 60)
    
    parser = DocumentParser()
    
    # Test TXT file
    test_file = os.path.join(os.path.dirname(__file__), 'sample_ai_text.txt')
    if os.path.exists(test_file):
        doc_data = parser.parse(test_file)
        print(f"✓ Successfully parsed TXT file")
        print(f"  Format: {doc_data['format']}")
        print(f"  Text length: {len(doc_data['text'])} characters")
    else:
        print("⚠ Sample file not found, skipping parser test")
    
    # Test supported formats
    assert parser.is_supported('test.pdf'), "Should support PDF"
    assert parser.is_supported('test.docx'), "Should support DOCX"
    assert parser.is_supported('test.txt'), "Should support TXT"
    assert parser.is_supported('test.png'), "Should support PNG"
    assert not parser.is_supported('test.xyz'), "Should not support XYZ"
    
    print("✓ Test passed: Document parser working correctly")


def test_highlighter():
    """Test text highlighter."""
    print("\n" + "=" * 60)
    print("TEST 4: Text Highlighter")
    print("=" * 60)
    
    text = "This is a test sentence. Furthermore, this is another sentence."
    
    detector = AIContentDetector()
    result = detector.analyze(text)
    
    highlighter = TextHighlighter(use_colors=False)
    
    # Test summary creation
    summary = highlighter.create_summary(result)
    assert len(summary) > 0, "Summary should not be empty"
    print("✓ Summary generated successfully")
    
    # Test HTML report
    html_report = highlighter.generate_html_report(text, result)
    assert '<html>' in html_report.lower(), "Should generate valid HTML"
    assert 'AI Score' in html_report, "Should contain score"
    print("✓ HTML report generated successfully")
    
    print("✓ Test passed: Text highlighter working correctly")


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("YourAIDetector - Test Suite")
    print("=" * 60)
    
    try:
        test_ai_text()
        test_human_text()
        test_document_parser()
        test_highlighter()
        
        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED")
        print("=" * 60 + "\n")
        
        return 0
    
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}\n")
        return 1
    
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
