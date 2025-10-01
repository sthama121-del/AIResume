"""
AIResume Backend Package
Contains modules for resume parsing, analysis, tailoring, and generation.
"""

from .file_parser import extract_text_from_file
from .resume_analyzer import calculate_match_score, extract_keywords
from .resume_tailor import tailor_resume
from .document_generator import generate_resume_document

__all__ = [
    'extract_text_from_file',
    'calculate_match_score',
    'extract_keywords',
    'tailor_resume',
    'generate_resume_document'
]
