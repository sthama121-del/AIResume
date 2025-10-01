"""
Resume Analyzer Module
Calculates match score between resume and job description.
Uses keyword extraction and similarity analysis.
"""

import re
from typing import Dict, List, Set, Tuple
from collections import Counter
import string


def clean_text(text: str) -> str:
    """
    Clean and normalize text for analysis.

    Args:
        text: Raw text

    Returns:
        Cleaned text
    """
    # Convert to lowercase
    text = text.lower()
    # Remove special characters but keep alphanumeric and spaces
    text = re.sub(r'[^a-z0-9\s\-\+\#]', ' ', text)
    # Remove extra whitespace
    text = ' '.join(text.split())
    return text


def extract_technical_keywords(text: str) -> Set[str]:
    """
    Extract technical keywords and skills from text.

    Args:
        text: Input text

    Returns:
        Set of technical keywords
    """
    # Common technical skills, tools, and technologies
    technical_patterns = [
        # Programming languages
        r'\b(python|java|javascript|typescript|c\+\+|c#|ruby|go|rust|swift|kotlin|scala|r|matlab|sql|nosql)\b',
        # Frameworks & Libraries
        r'\b(react|angular|vue|django|flask|fastapi|spring|express|node\.?js|tensorflow|pytorch|keras|pandas|numpy|scikit-learn)\b',
        # Cloud & DevOps
        r'\b(aws|azure|gcp|docker|kubernetes|jenkins|gitlab|github|terraform|ansible|circleci)\b',
        # Databases
        r'\b(postgresql|mysql|mongodb|redis|cassandra|dynamodb|snowflake|bigquery|redshift|databricks)\b',
        # AI/ML/Data
        r'\b(machine learning|deep learning|nlp|computer vision|genai|generative ai|llm|transformer|bert|gpt|mlops|data science|analytics)\b',
        # Tools & Technologies
        r'\b(git|jira|confluence|slack|agile|scrum|ci/cd|rest api|graphql|microservices|kafka|spark|hadoop|airflow)\b',
        # Certifications & Methodologies
        r'\b(aws certified|azure certified|pmp|scrum master|agile|devops|tdd|bdd)\b',
    ]

    keywords = set()
    text_clean = clean_text(text)

    for pattern in technical_patterns:
        matches = re.findall(pattern, text_clean, re.IGNORECASE)
        keywords.update(matches)

    # Extract multi-word technical terms
    multi_word_terms = [
        'machine learning', 'deep learning', 'natural language processing',
        'computer vision', 'data science', 'data engineering', 'software engineering',
        'full stack', 'backend', 'frontend', 'devops', 'mlops', 'generative ai',
        'artificial intelligence', 'big data', 'cloud computing', 'web development',
        'mobile development', 'rest api', 'graphql', 'microservices', 'ci/cd',
        'agile methodology', 'scrum', 'test driven development'
    ]

    for term in multi_word_terms:
        if term in text_clean:
            keywords.add(term.replace(' ', '_'))

    return keywords


def extract_experience_requirements(jd_text: str) -> Dict[str, int]:
    """
    Extract years of experience requirements from job description.

    Args:
        jd_text: Job description text

    Returns:
        Dictionary mapping skills to required years
    """
    requirements = {}
    text_clean = clean_text(jd_text)

    # Pattern to match "X years of Y" or "X+ years Y"
    patterns = [
        r'(\d+)\+?\s*(?:years?|yrs?)\s+(?:of\s+)?(?:experience\s+(?:in\s+|with\s+)?)?([a-z\s\-]+)',
        r'([a-z\s\-]+)[\s\-:]+(\d+)\+?\s*(?:years?|yrs?)',
    ]

    for pattern in patterns:
        matches = re.findall(pattern, text_clean)
        for match in matches:
            if pattern.startswith(r'(\d+)'):
                years, skill = match
            else:
                skill, years = match

            skill = skill.strip()
            # Filter out common words
            if skill and len(skill) > 2 and skill not in ['the', 'and', 'or', 'with', 'in']:
                try:
                    requirements[skill] = int(years)
                except ValueError:
                    pass

    return requirements


def calculate_keyword_match(resume_keywords: Set[str], jd_keywords: Set[str]) -> float:
    """
    Calculate keyword match percentage.

    Args:
        resume_keywords: Set of keywords from resume
        jd_keywords: Set of keywords from job description

    Returns:
        Match percentage (0-100)
    """
    if not jd_keywords:
        return 0.0

    matched_keywords = resume_keywords.intersection(jd_keywords)
    match_percentage = (len(matched_keywords) / len(jd_keywords)) * 100

    return min(match_percentage, 100.0)


def extract_keywords(text: str) -> Set[str]:
    """
    Extract all relevant keywords from text.

    Args:
        text: Input text

    Returns:
        Set of keywords
    """
    # Get technical keywords
    keywords = extract_technical_keywords(text)

    # Add additional important words (nouns, verbs, domain terms)
    text_clean = clean_text(text)
    words = text_clean.split()

    # Filter for meaningful words (length > 3, not common words)
    common_words = {
        'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
        'a', 'an', 'is', 'was', 'are', 'were', 'been', 'be', 'have', 'has', 'had',
        'do', 'does', 'did', 'will', 'would', 'should', 'could', 'may', 'might',
        'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it',
        'we', 'they', 'what', 'which', 'who', 'when', 'where', 'why', 'how'
    }

    for word in words:
        if len(word) > 3 and word not in common_words:
            keywords.add(word)

    return keywords


def calculate_match_score(resume_text: str, jd_text: str) -> Dict:
    """
    Calculate comprehensive match score between resume and job description.

    Args:
        resume_text: Resume text
        jd_text: Job description text

    Returns:
        Dictionary containing match score and details
    """
    # Extract keywords
    resume_keywords = extract_keywords(resume_text)
    jd_keywords = extract_keywords(jd_text)

    # Calculate keyword match
    keyword_match = calculate_keyword_match(resume_keywords, jd_keywords)

    # Extract technical keywords specifically
    resume_tech = extract_technical_keywords(resume_text)
    jd_tech = extract_technical_keywords(jd_text)

    # Calculate technical skills match
    if jd_tech:
        tech_match = (len(resume_tech.intersection(jd_tech)) / len(jd_tech)) * 100
    else:
        tech_match = 0.0

    # Overall match score (weighted average)
    # Technical skills are weighted more heavily (60%) vs general keywords (40%)
    overall_score = (tech_match * 0.6) + (keyword_match * 0.4)

    # Extract experience requirements
    experience_reqs = extract_experience_requirements(jd_text)

    # Matched and missing keywords
    matched_keywords = resume_keywords.intersection(jd_keywords)
    missing_keywords = jd_keywords - resume_keywords

    matched_tech = resume_tech.intersection(jd_tech)
    missing_tech = jd_tech - resume_tech

    return {
        'overall_score': round(overall_score, 2),
        'keyword_match': round(keyword_match, 2),
        'technical_match': round(tech_match, 2),
        'matched_keywords': matched_keywords,
        'missing_keywords': missing_keywords,
        'matched_technical': matched_tech,
        'missing_technical': missing_tech,
        'experience_requirements': experience_reqs,
        'total_jd_keywords': len(jd_keywords),
        'total_resume_keywords': len(resume_keywords),
        'total_jd_technical': len(jd_tech),
        'total_resume_technical': len(resume_tech)
    }


def get_match_summary(match_results: Dict) -> str:
    """
    Generate human-readable summary of match results.

    Args:
        match_results: Results from calculate_match_score

    Returns:
        Summary text
    """
    summary = []

    summary.append(f"Overall Match Score: {match_results['overall_score']:.1f}%")
    summary.append(f"Technical Skills Match: {match_results['technical_match']:.1f}%")
    summary.append(f"Keyword Match: {match_results['keyword_match']:.1f}%")

    if match_results['missing_technical']:
        missing_tech_list = ', '.join(sorted(list(match_results['missing_technical']))[:10])
        summary.append(f"\nMissing Technical Skills: {missing_tech_list}")

    if match_results['experience_requirements']:
        summary.append("\nExperience Requirements Found:")
        for skill, years in list(match_results['experience_requirements'].items())[:5]:
            summary.append(f"  • {skill}: {years} years")

    return '\n'.join(summary)
