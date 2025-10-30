"""
YourAIDetector - Comprehensive AI Content Detection Tool
=========================================================

A powerful tool for detecting AI-generated content in documents.
Supports PDF, DOCX, TXT, and image files with OCR.
"""

__version__ = "1.0.0"
__author__ = "YourAIDetector Team"

from .detector import AIContentDetector
from .parser import DocumentParser
from .highlighter import TextHighlighter

__all__ = ['AIContentDetector', 'DocumentParser', 'TextHighlighter']
