"""
Document Parser Module
======================

Handles parsing of various document formats including PDF, DOCX, TXT, and images with OCR.
"""

import os
from typing import Optional, Dict, Any
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class DocumentParser:
    """Parse documents from various formats and extract text."""
    
    def __init__(self):
        """Initialize the document parser."""
        self.supported_formats = ['.pdf', '.docx', '.doc', '.txt', '.png', '.jpg', '.jpeg', '.tiff', '.bmp']
    
    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        Parse a document and extract text.
        
        Args:
            file_path: Path to the document file
            
        Returns:
            Dictionary containing text and metadata
            
        Raises:
            ValueError: If file format is not supported
            FileNotFoundError: If file does not exist
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext not in self.supported_formats:
            raise ValueError(f"Unsupported file format: {file_ext}")
        
        logger.info(f"Parsing document: {file_path}")
        
        if file_ext == '.pdf':
            return self._parse_pdf(file_path)
        elif file_ext in ['.docx', '.doc']:
            return self._parse_docx(file_path)
        elif file_ext == '.txt':
            return self._parse_txt(file_path)
        elif file_ext in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp']:
            return self._parse_image(file_path)
        else:
            raise ValueError(f"Unsupported format: {file_ext}")
    
    def _parse_pdf(self, file_path: str) -> Dict[str, Any]:
        """Parse PDF file and extract text."""
        try:
            import PyPDF2
            
            text_content = []
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                num_pages = len(pdf_reader.pages)
                
                for page_num in range(num_pages):
                    page = pdf_reader.pages[page_num]
                    text_content.append(page.extract_text())
            
            full_text = '\n'.join(text_content)
            
            return {
                'text': full_text,
                'format': 'pdf',
                'pages': num_pages,
                'file_path': file_path
            }
        except ImportError:
            logger.error("PyPDF2 not installed. Install with: pip install PyPDF2")
            raise
        except Exception as e:
            logger.error(f"Error parsing PDF: {e}")
            raise
    
    def _parse_docx(self, file_path: str) -> Dict[str, Any]:
        """Parse DOCX file and extract text."""
        try:
            import docx
            
            doc = docx.Document(file_path)
            text_content = []
            
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    text_content.append(paragraph.text)
            
            full_text = '\n'.join(text_content)
            
            return {
                'text': full_text,
                'format': 'docx',
                'paragraphs': len(text_content),
                'file_path': file_path
            }
        except ImportError:
            logger.error("python-docx not installed. Install with: pip install python-docx")
            raise
        except Exception as e:
            logger.error(f"Error parsing DOCX: {e}")
            raise
    
    def _parse_txt(self, file_path: str) -> Dict[str, Any]:
        """Parse TXT file and extract text."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            
            return {
                'text': text,
                'format': 'txt',
                'file_path': file_path
            }
        except UnicodeDecodeError:
            # Try with different encoding
            with open(file_path, 'r', encoding='latin-1') as file:
                text = file.read()
            
            return {
                'text': text,
                'format': 'txt',
                'file_path': file_path
            }
        except Exception as e:
            logger.error(f"Error parsing TXT: {e}")
            raise
    
    def _parse_image(self, file_path: str) -> Dict[str, Any]:
        """Parse image file using OCR and extract text."""
        try:
            import pytesseract
            from PIL import Image
            
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image)
            
            return {
                'text': text,
                'format': 'image',
                'image_size': image.size,
                'file_path': file_path
            }
        except ImportError:
            logger.error("pytesseract or Pillow not installed. Install with: pip install pytesseract Pillow")
            raise
        except Exception as e:
            logger.error(f"Error parsing image: {e}")
            raise
    
    def is_supported(self, file_path: str) -> bool:
        """
        Check if a file format is supported.
        
        Args:
            file_path: Path to the file
            
        Returns:
            True if format is supported, False otherwise
        """
        file_ext = Path(file_path).suffix.lower()
        return file_ext in self.supported_formats
