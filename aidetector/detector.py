"""
AI Content Detector Module
===========================

Core detection engine for identifying AI-generated content using multiple methods.
"""

import re
import logging
from typing import List, Dict, Any, Tuple
import numpy as np

logger = logging.getLogger(__name__)


class AIContentDetector:
    """
    Detect AI-generated content using multiple analysis methods.
    
    This detector uses a combination of:
    1. Perplexity analysis (sentence complexity)
    2. Burstiness detection (variation in sentence structure)
    3. Pattern recognition (common AI writing patterns)
    4. Vocabulary analysis (word choice and repetition)
    """
    
    def __init__(self, threshold: float = 0.5):
        """
        Initialize the AI content detector.
        
        Args:
            threshold: Detection threshold (0.0 to 1.0). Higher values are more strict.
        """
        self.threshold = threshold
        self._initialize_patterns()
    
    def _initialize_patterns(self):
        """Initialize common AI writing patterns."""
        # Common phrases used by AI models
        self.ai_patterns = [
            r'\bin conclusion\b',
            r'\bin summary\b',
            r'\bit\'s worth noting\b',
            r'\bit is important to note\b',
            r'\boverall\b',
            r'\bin general\b',
            r'\bfurthermore\b',
            r'\bmoreover\b',
            r'\badditionally\b',
            r'\bhowever\b',
            r'\bnevertheless\b',
            r'\bconsequently\b',
            r'\btherefore\b',
            r'\bas a result\b',
            r'\bon the other hand\b',
            r'\bfrom this perspective\b',
        ]
        
        # Compile patterns for efficiency
        self.compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.ai_patterns]
    
    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Analyze text for AI-generated content.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary containing analysis results and AI score
        """
        if not text or not text.strip():
            return {
                'ai_score': 0.0,
                'is_ai_generated': False,
                'confidence': 0.0,
                'details': {'error': 'Empty text provided'}
            }
        
        logger.info("Starting AI content analysis")
        
        # Split text into sentences
        sentences = self._split_sentences(text)
        
        if len(sentences) < 3:
            return {
                'ai_score': 0.0,
                'is_ai_generated': False,
                'confidence': 0.0,
                'details': {'error': 'Text too short for reliable analysis'}
            }
        
        # Perform various analyses
        perplexity_score = self._analyze_perplexity(sentences)
        burstiness_score = self._analyze_burstiness(sentences)
        pattern_score = self._analyze_patterns(text)
        vocabulary_score = self._analyze_vocabulary(text)
        
        # Calculate weighted AI score
        ai_score = (
            perplexity_score * 0.3 +
            burstiness_score * 0.3 +
            pattern_score * 0.25 +
            vocabulary_score * 0.15
        )
        
        # Determine if text is AI-generated
        is_ai_generated = ai_score >= self.threshold
        confidence = min(abs(ai_score - 0.5) * 2, 1.0)
        
        # Find suspicious segments
        suspicious_segments = self._find_suspicious_segments(text, sentences)
        
        return {
            'ai_score': round(ai_score, 3),
            'is_ai_generated': is_ai_generated,
            'confidence': round(confidence, 3),
            'threshold': self.threshold,
            'details': {
                'perplexity_score': round(perplexity_score, 3),
                'burstiness_score': round(burstiness_score, 3),
                'pattern_score': round(pattern_score, 3),
                'vocabulary_score': round(vocabulary_score, 3),
                'total_sentences': len(sentences),
                'suspicious_segments': suspicious_segments
            }
        }
    
    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        # Simple sentence splitting (can be improved with NLTK)
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        return sentences
    
    def _analyze_perplexity(self, sentences: List[str]) -> float:
        """
        Analyze text perplexity (complexity).
        AI text tends to have lower perplexity (more predictable).
        
        Returns:
            Score from 0 to 1 (higher = more AI-like)
        """
        if not sentences:
            return 0.0
        
        # Calculate average sentence length
        avg_length = np.mean([len(s.split()) for s in sentences])
        
        # Calculate standard deviation of sentence length
        std_length = np.std([len(s.split()) for s in sentences])
        
        # AI text tends to have more uniform sentence length
        # Low std relative to avg suggests AI
        if avg_length == 0:
            return 0.0
        
        uniformity = 1 - min(std_length / avg_length, 1.0)
        
        # Also check vocabulary complexity
        words = ' '.join(sentences).lower().split()
        unique_words = len(set(words))
        total_words = len(words)
        
        if total_words == 0:
            return 0.0
        
        # AI text often has lower vocabulary diversity
        diversity = unique_words / total_words
        simplicity = 1 - diversity
        
        # Combine metrics
        perplexity_score = (uniformity * 0.6 + simplicity * 0.4)
        
        return min(max(perplexity_score, 0.0), 1.0)
    
    def _analyze_burstiness(self, sentences: List[str]) -> float:
        """
        Analyze burstiness (variation in sentence complexity).
        Human text is typically more "bursty" with varying complexity.
        
        Returns:
            Score from 0 to 1 (higher = more AI-like)
        """
        if len(sentences) < 3:
            return 0.0
        
        # Calculate complexity metrics for each sentence
        complexities = []
        for sentence in sentences:
            words = sentence.split()
            if not words:
                continue
            
            # Factors: word count, avg word length, punctuation
            word_count = len(words)
            avg_word_length = np.mean([len(w) for w in words])
            punct_count = len([c for c in sentence if c in ',.;:!?'])
            
            complexity = word_count * 0.5 + avg_word_length * 0.3 + punct_count * 0.2
            complexities.append(complexity)
        
        if not complexities:
            return 0.0
        
        # Calculate variation coefficient
        mean_complexity = np.mean(complexities)
        std_complexity = np.std(complexities)
        
        if mean_complexity == 0:
            return 0.0
        
        variation_coef = std_complexity / mean_complexity
        
        # Lower variation = more AI-like (less bursty)
        burstiness_score = 1 - min(variation_coef / 0.5, 1.0)
        
        return min(max(burstiness_score, 0.0), 1.0)
    
    def _analyze_patterns(self, text: str) -> float:
        """
        Analyze text for common AI writing patterns.
        
        Returns:
            Score from 0 to 1 (higher = more AI-like)
        """
        text_lower = text.lower()
        pattern_matches = 0
        
        for pattern in self.compiled_patterns:
            if pattern.search(text_lower):
                pattern_matches += 1
        
        # Calculate pattern density
        words = text.split()
        if len(words) < 50:
            # Not enough text for pattern analysis
            return 0.0
        
        # Normalize by text length (patterns per 100 words)
        pattern_density = (pattern_matches / len(words)) * 100
        
        # Scale to 0-1 range (5 patterns per 100 words = 1.0)
        pattern_score = min(pattern_density / 5.0, 1.0)
        
        return pattern_score
    
    def _analyze_vocabulary(self, text: str) -> float:
        """
        Analyze vocabulary characteristics.
        AI text often has specific vocabulary patterns.
        
        Returns:
            Score from 0 to 1 (higher = more AI-like)
        """
        words = text.lower().split()
        
        if len(words) < 20:
            return 0.0
        
        # Calculate word repetition rate
        word_counts = {}
        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1
        
        # AI text often has more repeated words
        repeated_words = sum(1 for count in word_counts.values() if count > 2)
        repetition_rate = repeated_words / len(word_counts)
        
        # Check for overly formal language (longer average word length)
        avg_word_length = np.mean([len(w) for w in words])
        formality = min(avg_word_length / 8.0, 1.0)
        
        vocabulary_score = (repetition_rate * 0.5 + formality * 0.5)
        
        return min(max(vocabulary_score, 0.0), 1.0)
    
    def _find_suspicious_segments(self, text: str, sentences: List[str]) -> List[Dict[str, Any]]:
        """
        Find specific text segments that are likely AI-generated.
        
        Returns:
            List of suspicious segments with their scores and positions
        """
        suspicious = []
        current_pos = 0
        
        for i, sentence in enumerate(sentences):
            # Calculate per-sentence AI likelihood
            sentence_score = 0.0
            reasons = []
            
            # Check for AI patterns
            for pattern in self.compiled_patterns:
                if pattern.search(sentence.lower()):
                    sentence_score += 0.2
                    reasons.append("Contains common AI phrase")
                    break
            
            # Check sentence structure uniformity
            words = sentence.split()
            if len(words) > 10:
                avg_word_len = np.mean([len(w) for w in words])
                if 5 <= avg_word_len <= 7:  # Suspiciously uniform
                    sentence_score += 0.15
                    reasons.append("Uniform word length")
            
            # Check for overly formal language
            formal_words = ['furthermore', 'moreover', 'additionally', 'consequently', 
                          'therefore', 'nevertheless', 'subsequently']
            if any(word in sentence.lower() for word in formal_words):
                sentence_score += 0.15
                reasons.append("Formal transition word")
            
            # If sentence is suspicious, add it
            if sentence_score >= 0.3:
                # Find position in original text
                pos = text.find(sentence)
                if pos != -1:
                    suspicious.append({
                        'text': sentence[:100] + '...' if len(sentence) > 100 else sentence,
                        'score': round(min(sentence_score, 1.0), 3),
                        'position': pos,
                        'length': len(sentence),
                        'reasons': reasons
                    })
        
        return suspicious[:10]  # Return top 10 most suspicious segments
