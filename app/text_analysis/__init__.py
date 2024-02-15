# app/text_analysis/__init__.py
from .nlp_processing import analyze_text
from .sentiment_analysis import get_sentiment
from .emotion_analysis import analyze_emotion

__all__ = ['analyze_text', 'get_sentiment', 'analyze_emotion']
