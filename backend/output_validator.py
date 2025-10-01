"""
Output Validator Module
Validates that LLM output contains all required sections without placeholders.
"""

from typing import Dict, List, Tuple
import re


def detect_placeholders(text: str) -> List[str]:
    """
    Detect placeholder text in LLM output.

    Args:
        text: LLM output text

    Returns:
        List of placeholder patterns found
    """
    placeholders = []

    # Common placeholder patterns
    patterns = [
        r'\[.*?PRESERVED.*?\]',
        r'\[.*?AS WRITTEN.*?\]',
        r'\[.*?EXACTLY.*?\]',
        r'\[.*?UNCHANGED.*?\]',
        r'\[Previous roles.*?\]',
        r'\[Environment section.*?\]',
        r'\[EDUCATION.*?\]',
        r'\[TECHNICAL SKILLS.*?\]',
        r'\[All previous.*?\]',
        r'\[Earlier roles.*?\]',
    ]

    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            placeholders.extend(matches)

    return placeholders


def validate_resume_sections(tailored_text: str, original_text: str) -> Dict:
    """
    Validate that tailored resume contains all required sections.

    Args:
        tailored_text: AI-generated tailored resume
        original_text: Original resume text

    Returns:
        Dictionary with validation results
    """
    issues = []

    # Check for placeholders
    placeholders = detect_placeholders(tailored_text)
    if placeholders:
        issues.append({
            'type': 'placeholders',
            'severity': 'critical',
            'message': f'Found {len(placeholders)} placeholder(s): {placeholders[:3]}'
        })

    # Check for ALL CAPS Professional Summary (wrong formatting)
    if 'SENIOR DATA ENGINEER WITH 20+ YEARS' in tailored_text:
        if 'Senior Data Engineer with 20+ years' in original_text:
            issues.append({
                'type': 'formatting',
                'severity': 'high',
                'message': 'Professional Summary changed to ALL CAPS (should preserve original formatting)'
            })

    # Check for specific company names from original
    original_companies = extract_company_names(original_text)
    for company in original_companies:
        if company not in tailored_text and company not in ['AT&T', 'Cognizant']:
            # Older companies should be present
            issues.append({
                'type': 'missing_company',
                'severity': 'critical',
                'message': f'Missing company: {company}'
            })

    # Check for Technical Skills section completeness
    if 'Cloud Technology' in original_text:
        if 'Cloud Technology' not in tailored_text:
            issues.append({
                'type': 'missing_section',
                'severity': 'critical',
                'message': 'Technical Skills section incomplete or missing'
            })

    # Check for Education section
    if 'Master of Computer Applications' in original_text:
        if 'Master of Computer Applications' not in tailored_text:
            issues.append({
                'type': 'missing_education',
                'severity': 'critical',
                'message': 'Education section missing or incomplete'
            })

    # Check for forbidden words
    forbidden_patterns = [
        (r'\bArchitected\b', 'Uses "Architected" (should preserve original action verbs)'),
        (r'\bLed\s+(?:development|implementation)', 'Adds "Led" (leadership inflation)'),
    ]

    original_lower = original_text.lower()
    for pattern, message in forbidden_patterns:
        if re.search(pattern, tailored_text, re.IGNORECASE):
            # Check if it was in original
            if not re.search(pattern, original_text, re.IGNORECASE):
                issues.append({
                    'type': 'verb_inflation',
                    'severity': 'high',
                    'message': message
                })

    return {
        'valid': len(issues) == 0,
        'issues': issues,
        'placeholder_count': len(placeholders)
    }


def extract_company_names(text: str) -> List[str]:
    """Extract company names from resume text."""
    companies = []

    # Common patterns for company names in experience section
    patterns = [
        r'([A-Z][A-Za-z\s&]+(?:Corporation|Technology Solutions|Bank|Syntel))',
        r'(Xoriant\s+Corporation)',
        r'(Atos\s+Syntel)',
        r'(ANZ\s+Bank)',
    ]

    for pattern in patterns:
        matches = re.findall(pattern, text)
        companies.extend(matches)

    return list(set(companies))


def suggest_fixes(validation_result: Dict) -> List[str]:
    """
    Suggest fixes based on validation issues.

    Args:
        validation_result: Result from validate_resume_sections

    Returns:
        List of suggested fixes
    """
    suggestions = []

    for issue in validation_result['issues']:
        if issue['type'] == 'placeholders':
            suggestions.append('CRITICAL: Remove all placeholders and output complete content')
        elif issue['type'] == 'missing_company':
            suggestions.append(f"Add missing company: {issue['message']}")
        elif issue['type'] == 'formatting':
            suggestions.append('Fix Professional Summary: Use sentence case, not ALL CAPS')
        elif issue['type'] == 'verb_inflation':
            suggestions.append(f"Fix action verbs: {issue['message']}")
        elif issue['type'] == 'missing_section':
            suggestions.append(f"Add missing section: {issue['message']}")

    return suggestions
