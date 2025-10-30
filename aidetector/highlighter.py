"""
Text Highlighter Module
========================

Highlights suspicious AI-generated text segments in the output.
"""

from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class TextHighlighter:
    """Highlight AI-generated text segments."""
    
    # ANSI color codes for terminal output
    COLORS = {
        'RED': '\033[91m',
        'YELLOW': '\033[93m',
        'GREEN': '\033[92m',
        'CYAN': '\033[96m',
        'MAGENTA': '\033[95m',
        'BOLD': '\033[1m',
        'UNDERLINE': '\033[4m',
        'END': '\033[0m'
    }
    
    # HTML color codes for report generation
    HTML_COLORS = {
        'HIGH': '#ff6b6b',     # Red for high suspicion
        'MEDIUM': '#ffd93d',   # Yellow for medium suspicion
        'LOW': '#6bcf7f',      # Green for low suspicion
        'STATUS_AI': '#ff6b6b',      # Red for AI-generated status
        'STATUS_HUMAN': '#6bcf7f'    # Green for human-written status
    }
    
    def __init__(self, use_colors: bool = True):
        """
        Initialize the text highlighter.
        
        Args:
            use_colors: Whether to use ANSI colors in output
        """
        self.use_colors = use_colors
    
    def highlight_text(self, text: str, suspicious_segments: List[Dict[str, Any]]) -> str:
        """
        Highlight suspicious segments in the text.
        
        Args:
            text: Original text
            suspicious_segments: List of suspicious segments from detector
            
        Returns:
            Text with highlighted segments
        """
        if not suspicious_segments:
            return text
        
        # Sort segments by position (reverse order to maintain positions)
        sorted_segments = sorted(suspicious_segments, key=lambda x: x['position'], reverse=True)
        
        highlighted_text = text
        
        for segment in sorted_segments:
            pos = segment['position']
            length = segment['length']
            score = segment['score']
            
            # Determine highlight color based on score
            if score >= 0.7:
                color = 'RED'
            elif score >= 0.5:
                color = 'YELLOW'
            else:
                color = 'CYAN'
            
            # Extract the segment
            original_segment = text[pos:pos + length]
            
            # Create highlighted version
            if self.use_colors:
                highlighted_segment = (
                    f"{self.COLORS[color]}{self.COLORS['BOLD']}"
                    f"{original_segment}"
                    f"{self.COLORS['END']}"
                )
            else:
                highlighted_segment = f"[SUSPICIOUS: {score}]{original_segment}[/SUSPICIOUS]"
            
            # Replace in text
            highlighted_text = (
                highlighted_text[:pos] + 
                highlighted_segment + 
                highlighted_text[pos + length:]
            )
        
        return highlighted_text
    
    def generate_html_report(self, text: str, analysis_result: Dict[str, Any]) -> str:
        """
        Generate an HTML report with highlighted text.
        
        Args:
            text: Original text
            analysis_result: Analysis result from detector
            
        Returns:
            HTML string with highlighted text and analysis
        """
        suspicious_segments = analysis_result.get('details', {}).get('suspicious_segments', [])
        ai_score = analysis_result.get('ai_score', 0.0)
        is_ai = analysis_result.get('is_ai_generated', False)
        
        # Sort segments by position
        sorted_segments = sorted(suspicious_segments, key=lambda x: x['position'], reverse=True)
        
        html_text = text
        
        # Highlight segments in HTML
        for segment in sorted_segments:
            pos = segment['position']
            length = segment['length']
            score = segment['score']
            reasons = segment.get('reasons', [])
            
            # Determine color based on score
            if score >= 0.7:
                color = self.HTML_COLORS['HIGH']
                intensity = 'high'
            elif score >= 0.5:
                color = self.HTML_COLORS['MEDIUM']
                intensity = 'medium'
            else:
                color = self.HTML_COLORS['LOW']
                intensity = 'low'
            
            original_segment = text[pos:pos + length]
            
            # Create HTML highlighted version with tooltip
            highlighted_segment = (
                f'<span class="highlight-{intensity}" '
                f'style="background-color: {color}; padding: 2px 4px; '
                f'border-radius: 3px; cursor: help;" '
                f'title="AI Score: {score}\nReasons: {", ".join(reasons)}">'
                f'{original_segment}'
                f'</span>'
            )
            
            html_text = (
                html_text[:pos] + 
                highlighted_segment + 
                html_text[pos + length:]
            )
        
        # Generate full HTML report
        status_color = self.HTML_COLORS['STATUS_AI'] if is_ai else self.HTML_COLORS['STATUS_HUMAN']
        status_text = 'LIKELY AI-GENERATED' if is_ai else 'LIKELY HUMAN-WRITTEN'
        
        html_report = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>AI Detection Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}
        .title {{
            font-size: 28px;
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
        }}
        .status {{
            font-size: 20px;
            font-weight: bold;
            color: {status_color};
            margin: 15px 0;
        }}
        .score-container {{
            display: flex;
            gap: 20px;
            margin: 20px 0;
        }}
        .score-box {{
            background-color: #f9f9f9;
            padding: 15px;
            border-radius: 5px;
            flex: 1;
        }}
        .score-label {{
            font-size: 12px;
            color: #666;
            text-transform: uppercase;
        }}
        .score-value {{
            font-size: 24px;
            font-weight: bold;
            color: #333;
            margin-top: 5px;
        }}
        .content {{
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            line-height: 1.8;
            white-space: pre-wrap;
            word-wrap: break-word;
        }}
        .legend {{
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}
        .legend-item {{
            display: inline-block;
            margin-right: 20px;
            margin-bottom: 10px;
        }}
        .legend-color {{
            display: inline-block;
            width: 20px;
            height: 20px;
            border-radius: 3px;
            margin-right: 5px;
            vertical-align: middle;
        }}
        .highlight-high {{
            background-color: #ff6b6b;
        }}
        .highlight-medium {{
            background-color: #ffd93d;
        }}
        .highlight-low {{
            background-color: #6bcf7f;
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="title">🔍 AI Content Detection Report</div>
        <div class="status">{status_text}</div>
        
        <div class="score-container">
            <div class="score-box">
                <div class="score-label">AI Score</div>
                <div class="score-value">{ai_score * 100:.1f}%</div>
            </div>
            <div class="score-box">
                <div class="score-label">Confidence</div>
                <div class="score-value">{analysis_result.get('confidence', 0) * 100:.1f}%</div>
            </div>
            <div class="score-box">
                <div class="score-label">Suspicious Segments</div>
                <div class="score-value">{len(suspicious_segments)}</div>
            </div>
        </div>
    </div>
    
    <div class="legend">
        <strong>Legend:</strong>
        <div class="legend-item">
            <span class="legend-color highlight-high"></span>
            <span>High Suspicion (70%+)</span>
        </div>
        <div class="legend-item">
            <span class="legend-color highlight-medium"></span>
            <span>Medium Suspicion (50-70%)</span>
        </div>
        <div class="legend-item">
            <span class="legend-color highlight-low"></span>
            <span>Low Suspicion (&lt;50%)</span>
        </div>
    </div>
    
    <div class="content">
{html_text}
    </div>
</body>
</html>
"""
        
        return html_report
    
    def create_summary(self, analysis_result: Dict[str, Any]) -> str:
        """
        Create a text summary of the analysis.
        
        Args:
            analysis_result: Analysis result from detector
            
        Returns:
            Formatted summary string
        """
        ai_score = analysis_result.get('ai_score', 0.0)
        is_ai = analysis_result.get('is_ai_generated', False)
        confidence = analysis_result.get('confidence', 0.0)
        details = analysis_result.get('details', {})
        
        summary_lines = []
        
        if self.use_colors:
            summary_lines.append(f"\n{self.COLORS['BOLD']}=== AI DETECTION RESULTS ==={self.COLORS['END']}\n")
        else:
            summary_lines.append("\n=== AI DETECTION RESULTS ===\n")
        
        # Status
        status = "LIKELY AI-GENERATED" if is_ai else "LIKELY HUMAN-WRITTEN"
        color = 'RED' if is_ai else 'GREEN'
        
        if self.use_colors:
            summary_lines.append(f"Status: {self.COLORS[color]}{self.COLORS['BOLD']}{status}{self.COLORS['END']}")
        else:
            summary_lines.append(f"Status: {status}")
        
        # Scores
        summary_lines.append(f"\nAI Score: {ai_score * 100:.1f}%")
        summary_lines.append(f"Confidence: {confidence * 100:.1f}%")
        summary_lines.append(f"Threshold: {analysis_result.get('threshold', 0.5) * 100:.1f}%")
        
        # Detailed metrics
        summary_lines.append("\n--- Detailed Metrics ---")
        summary_lines.append(f"Perplexity Score: {details.get('perplexity_score', 0) * 100:.1f}%")
        summary_lines.append(f"Burstiness Score: {details.get('burstiness_score', 0) * 100:.1f}%")
        summary_lines.append(f"Pattern Score: {details.get('pattern_score', 0) * 100:.1f}%")
        summary_lines.append(f"Vocabulary Score: {details.get('vocabulary_score', 0) * 100:.1f}%")
        
        # Suspicious segments
        suspicious_segments = details.get('suspicious_segments', [])
        if suspicious_segments:
            summary_lines.append(f"\n--- Top Suspicious Segments ({len(suspicious_segments)}) ---")
            for i, segment in enumerate(suspicious_segments[:5], 1):
                summary_lines.append(f"\n{i}. Score: {segment['score'] * 100:.1f}%")
                summary_lines.append(f"   Text: {segment['text']}")
                summary_lines.append(f"   Reasons: {', '.join(segment['reasons'])}")
        
        summary_lines.append("\n" + "=" * 50 + "\n")
        
        return '\n'.join(summary_lines)
