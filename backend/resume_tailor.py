"""
Resume Tailor Module
Uses LLM (via OpenRouter) to intelligently tailor resume content to job description.
Preserves dates and structure while optimizing bullet points.
"""

import json
from typing import Dict, List, Tuple
from openai import OpenAI
import config


def get_openrouter_client() -> OpenAI:
    """
    Initialize OpenRouter client using OpenAI SDK.

    Returns:
        OpenAI client configured for OpenRouter
    """
    config.validate_config()

    client = OpenAI(
        base_url=config.OPENROUTER_BASE_URL,
        api_key=config.OPENROUTER_API_KEY,
    )

    return client


def get_account_balance() -> Dict:
    """
    Get OpenRouter account credit balance.

    Returns:
        Dictionary with balance information or error
    """
    import requests

    try:
        config.validate_config()

        headers = {
            "Authorization": f"Bearer {config.OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.get(
            "https://openrouter.ai/api/v1/auth/key",
            headers=headers,
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            # OpenRouter returns credit limit and usage
            return {
                'success': True,
                'limit': data.get('data', {}).get('limit'),
                'usage': data.get('data', {}).get('usage'),
                'label': data.get('data', {}).get('label', 'API Key'),
                'is_free_tier': data.get('data', {}).get('is_free_tier', False)
            }
        else:
            return {
                'success': False,
                'error': f"HTTP {response.status_code}"
            }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def create_tailoring_prompt(
    resume_text: str,
    jd_text: str,
    match_analysis: Dict,
    max_projects: int = 2
) -> str:
    """
    Create detailed prompt for LLM to tailor resume.

    Args:
        resume_text: Original resume text
        jd_text: Job description text
        match_analysis: Match analysis results from resume_analyzer
        max_projects: Maximum number of recent projects to tailor

    Returns:
        Formatted prompt string
    """
    missing_skills = ', '.join(list(match_analysis.get('missing_technical', set()))[:10])
    experience_reqs = match_analysis.get('experience_requirements', {})

    exp_req_text = ""
    if experience_reqs:
        exp_req_text = "\n".join([f"  - {skill}: {years} years" for skill, years in list(experience_reqs.items())[:5]])

    prompt = f"""You are an expert resume writer. Your task is to output a COMPLETE resume with ALL sections included.

**ORIGINAL RESUME:**
{resume_text}

**JOB DESCRIPTION:**
{jd_text}

**MATCH ANALYSIS:**
Current Match Score: {match_analysis.get('overall_score', 0):.1f}%
Missing Technical Skills: {missing_skills}

{f'**EXPERIENCE REQUIREMENTS:**{chr(10)}{exp_req_text}' if exp_req_text else ''}

**CRITICAL INSTRUCTION:**
You MUST output the ENTIRE resume with ALL content included. DO NOT use brackets, placeholders, or references like "[PRESERVED]" or "[AS WRITTEN]".

**YOUR TASK:**
Create a tailored resume by COPYING THE ENTIRE ORIGINAL RESUME and modifying ONLY the bullet points in the {max_projects} most recent Experience roles. Everything else must be COPIED WORD-FOR-WORD from the original.

**HOW TO DO THIS:**
1. Copy the name and contact information exactly
2. Copy the Professional Summary exactly (every single word, exact capitalization)
3. Copy the ENTIRE Technical Skills section (all categories: Cloud Technology, ETL Tools, RepoSystem, ML Frameworks, Dev tools, Schedulers, Languages, Databases - copy every single item)
4. For Experience section:
   - For the {max_projects} most recent roles: Copy company/title/dates exactly, then modify ONLY the bullet points
   - For all older roles: Copy EVERYTHING word-for-word (company, title, dates, ALL bullets, environment section)
5. Copy the Education section exactly (degree, university, year, GPA)
6. Copy any other sections exactly

**CRITICAL CONSTRAINTS:**

**ABSOLUTE RESTRICTIONS - NEVER VIOLATE:**
1. **NEVER INVENT COMPANIES/PROJECTS**: Keep all company names, project names, and roles exactly as written
2. **NEVER DELETE PROJECTS/ROLES**: All existing work history must remain intact
3. **NEVER REMOVE OR TRUNCATE SECTIONS**: All resume sections must remain in the final output
4. **PRESERVE ALL DATES**: Do not change any start dates, end dates, or date ranges
5. **NO TECHNOLOGY FABRICATION**: Only mention technologies/tools that already exist in the original resume
6. **NO EXPERIENCE INVENTION**: Do not add advanced methods (e.g., "LLM fine-tuning", "FSDP", "model serving at scale") unless they're already present

**SECTIONS THAT MUST REMAIN 100% UNCHANGED:**
1. **PROFESSIONAL SUMMARY** - Keep exactly as written, word-for-word
2. **TECHNICAL SKILLS** - Do not modify, add, or remove any skills
3. **EDUCATION** - Keep all degrees, schools, dates, GPA exactly as-is
4. **CONTACT INFORMATION** - Name, email, phone, location, LinkedIn - no changes
5. **CERTIFICATIONS** - If present, keep exactly as-is
6. **PUBLICATIONS** - If present, keep exactly as-is
7. **AWARDS** - If present, keep exactly as-is

**ONLY SECTION THAT CAN BE MODIFIED:**
- **EXPERIENCE SECTION** - And only the most recent {max_projects} roles/projects within it
- All other roles in Experience section must remain unchanged

**ALLOWED MODIFICATIONS (ONLY IN {max_projects} MOST RECENT ROLES IN EXPERIENCE SECTION):**
1. **REPHRASE BULLET POINTS**: Reuse original responsibility wording, adjust phrasing to highlight relevant skills
2. **EMPHASIZE EXISTING STRENGTHS**: If resume mentions Snowflake/Databricks/Azure/MLflow/PySpark, emphasize these more prominently
3. **ADJUST TERMINOLOGY**: Use job description's language (e.g., "MLOps pipeline" instead of "ML pipeline") if the concept already exists
4. **MAINTAIN BULLET COUNT**: Keep same number of bullets (max ±1)
5. **ADD CONTEXT**: Add brief context to existing achievements (e.g., "developed pipelines" → "developed enterprise-scale pipelines")
6. **PRESERVE ACTION VERBS**: If original says "Designed", keep "Designed" - do NOT change to "Architected"
7. **NO TITLE INFLATION**: If original doesn't say "Led" or "Architected", do NOT add leadership claims - use "Developed", "Implemented", "Built", "Created" instead

**EXAMPLES OF CORRECT TAILORING:**

Example 1 - Adding existing tech:
Original: "Developed data pipelines using Python and SQL"
JD requires: Snowflake, Databricks, PySpark
IF resume has these: "Developed data pipelines using Python, PySpark, and SQL with Snowflake and Databricks"
IF resume doesn't: "Developed scalable data pipelines using Python and SQL" (emphasize scale, don't add tech)

Example 2 - Preserving action verbs:
Original: "Designed and delivered BCAMS system processing 400M+ rows"
CORRECT: "Designed and delivered BCAMS system processing 400M+ rows using Snowflake and Snowpark"
WRONG: "Architected and scaled BCAMS system..." (changes "Designed" to "Architected" - NOT ALLOWED)

Example 3 - No leadership inflation:
Original: "Developed probabilistic matching engine in Python"
CORRECT: "Developed probabilistic matching engine in Python with automated training pipelines"
WRONG: "Led development of probabilistic matching engine..." (adds "Led" when not in original - NOT ALLOWED)

**CRITICAL: SECTIONS TO NEVER TOUCH:**
- Professional Summary / Objective (keep 100% as-is)
- Technical Skills / Skills (keep 100% as-is)
- Education (keep 100% as-is)
- Contact Info (keep 100% as-is)
- Certifications, Publications, Awards, Patents (keep 100% as-is)
- Older roles beyond the {max_projects} most recent (keep 100% as-is)

**OUTPUT FORMAT REQUIREMENTS:**

CRITICAL: Your output must be a clean, professional resume document ready for recruiters.

**DO NOT INCLUDE:**
- ❌ Any meta-text like "I'll help tailor this resume" or "Here's the tailored version"
- ❌ Any explanation of constraints or process
- ❌ Any preamble or introduction
- ❌ Any comments about what you're doing

**YOU MUST:**
- ✅ Start IMMEDIATELY with the resume content (name, contact info on first line)
- ✅ Include ALL sections: Professional Summary, Technical Skills, Education, Experience, etc.
- ✅ Make it look like a complete, professional resume
- ✅ End with "---TAILORING SUMMARY---" followed by the summary section
- ✅ **NEVER USE PLACEHOLDERS** - Output the complete actual content
- ✅ **PRESERVE EXACT FORMATTING** - Don't change capitalization or structure

**CRITICAL - NEVER DO THIS:**
❌ Do NOT write "[ORIGINAL TECHNICAL SKILLS SECTION PRESERVED EXACTLY AS WRITTEN]"
❌ Do NOT write "[Previous roles preserved exactly as written]"
❌ Do NOT write "[EDUCATION SECTION PRESERVED EXACTLY AS WRITTEN]"
❌ Do NOT use ANY placeholders or references

**INSTEAD - DO THIS:**
✅ Copy the COMPLETE Technical Skills section word-for-word with all categories
✅ Copy ALL Experience roles word-for-word (older roles unchanged, recent roles with modified bullets)
✅ Copy the COMPLETE Education section word-for-word
✅ Maintain EXACT formatting (if original is sentence case, keep it sentence case - don't change to ALL CAPS)

**STRUCTURE:**
1. Start with name and contact info (no preamble)
2. Professional Summary (copy exact wording AND exact formatting - preserve capitalization)
3. Technical Skills (copy COMPLETE list - all Cloud Technology, ETL Tools, RepoSystem, ML Frameworks, Dev tools, Schedulers, Languages, Databases)
4. Experience section:
   - Recent {max_projects} roles: Copy company/title/dates exact, modify ONLY bullets
   - Older roles: Copy EVERYTHING word-for-word including all bullets
5. Education (copy COMPLETE details - degree, university, year, GPA)
6. Any other sections (copy word-for-word)
7. Then add: "---TAILORING SUMMARY---"
8. Then add the summary content below

**TAILORING SUMMARY FORMAT:**
---TAILORING SUMMARY---

**Sections Preserved (100% unchanged):**
- Professional Summary
- Technical Skills
- Education
- Contact Information
- [Any other sections]

**Roles Modified:** [Number] (most recent only)
- [Role 1 at Company]: [Number] bullets modified
- [Role 2 at Company]: [Number] bullets modified

**Roles Preserved:** [Number]
- [Older roles list]: 100% unchanged

**Example Changes:**
- Original: "[Original bullet text]"
- Modified: "[Modified bullet text]"
- Reason: Emphasized existing [technology] to match JD requirement

**Technologies NOT Added:** [List JD requirements not in original resume]
**Factual Accuracy:** 100% - No fabricated experience

REMEMBER: Start your response directly with the name/contact info. NO introductory text.
"""

    return prompt


def parse_llm_response(response_text: str) -> Tuple[str, str]:
    """
    Parse LLM response to extract tailored resume and summary.

    Args:
        response_text: Raw LLM response

    Returns:
        Tuple of (tailored_resume, summary)
    """
    # Split on the summary marker
    parts = response_text.split('---TAILORING SUMMARY---')

    if len(parts) == 2:
        tailored_resume = parts[0].strip()
        summary = parts[1].strip()
    else:
        # If marker not found, try alternative splits
        if 'TAILORING SUMMARY' in response_text:
            parts = response_text.split('TAILORING SUMMARY')
            tailored_resume = parts[0].strip()
            summary = parts[1].strip() if len(parts) > 1 else "Summary not available"
        else:
            tailored_resume = response_text.strip()
            summary = "Summary not available"

    return tailored_resume, summary


def tailor_resume(
    resume_text: str,
    jd_text: str,
    match_analysis: Dict,
    model: str = None,
    max_projects: int = 2
) -> Dict:
    """
    Tailor resume to job description using LLM.

    Args:
        resume_text: Original resume text
        jd_text: Job description text
        match_analysis: Match analysis results
        model: LLM model to use (defaults to config.DEFAULT_MODEL)
        max_projects: Number of recent projects to tailor

    Returns:
        Dictionary with tailored resume and metadata
    """
    if model is None:
        model = config.DEFAULT_MODEL

    # Create client
    client = get_openrouter_client()

    # Create prompt
    prompt = create_tailoring_prompt(resume_text, jd_text, match_analysis, max_projects)

    try:
        # Call LLM
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert resume writer with deep knowledge of ATS systems and recruitment best practices. "
                               "CRITICAL: Output ONLY the clean, professional resume document starting with the candidate's name. "
                               "Do NOT include any meta-text, preambles, or explanations. Start directly with resume content. "
                               "NEVER use placeholders like '[PRESERVED]' or '[ORIGINAL SECTION]' - output the COMPLETE actual content. "
                               "Copy all preserved sections word-for-word including Technical Skills (all categories), Education (complete details), "
                               "and older Experience roles (all bullets). Maintain exact formatting and capitalization. "
                               "The output must be a COMPLETE resume ready to send to recruiters with no additional editing needed."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,  # Lower temperature for more deterministic, less "creative" output
            max_tokens=6000  # Higher token limit for complete resume with all sections
        )

        # Extract response
        response_text = response.choices[0].message.content

        # Parse response
        tailored_resume, summary = parse_llm_response(response_text)

        # Calculate detailed token usage and cost
        usage_info = {}
        if hasattr(response, 'usage'):
            usage_info = {
                'prompt_tokens': response.usage.prompt_tokens,
                'completion_tokens': response.usage.completion_tokens,
                'total_tokens': response.usage.total_tokens
            }

        return {
            'success': True,
            'tailored_resume': tailored_resume,
            'summary': summary,
            'model_used': model,
            'original_match_score': match_analysis.get('overall_score', 0),
            'tokens_used': response.usage.total_tokens if hasattr(response, 'usage') else None,
            'usage_info': usage_info
        }

    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'tailored_resume': resume_text,  # Return original on failure
            'summary': f"Error during tailoring: {str(e)}"
        }


def tailor_resume_iterative(
    resume_text: str,
    jd_text: str,
    match_analysis: Dict,
    target_score: float = 85.0,
    max_iterations: int = 2,
    model: str = None
) -> Dict:
    """
    Iteratively tailor resume to achieve target match score.

    Args:
        resume_text: Original resume text
        jd_text: Job description text
        match_analysis: Initial match analysis
        target_score: Target match score percentage
        max_iterations: Maximum tailoring iterations
        model: LLM model to use

    Returns:
        Dictionary with final tailored resume and metadata
    """
    current_resume = resume_text
    current_score = match_analysis.get('overall_score', 0)
    iteration_history = []

    for i in range(max_iterations):
        if current_score >= target_score:
            break

        # Tailor resume
        result = tailor_resume(
            current_resume,
            jd_text,
            match_analysis,
            model=model,
            max_projects=min(2, i + 1)  # Tailor more projects in later iterations
        )

        if not result['success']:
            break

        current_resume = result['tailored_resume']

        # Re-analyze match score
        from .resume_analyzer import calculate_match_score
        new_analysis = calculate_match_score(current_resume, jd_text)
        new_score = new_analysis.get('overall_score', 0)

        iteration_history.append({
            'iteration': i + 1,
            'score': new_score,
            'summary': result['summary']
        })

        # Update for next iteration
        current_score = new_score
        match_analysis = new_analysis

    return {
        'success': True,
        'tailored_resume': current_resume,
        'final_score': current_score,
        'iterations': len(iteration_history),
        'iteration_history': iteration_history,
        'improvement': current_score - match_analysis.get('overall_score', 0)
    }


def calculate_estimated_cost(model: str, usage_info: Dict) -> Dict:
    """
    Calculate estimated cost based on token usage.

    Args:
        model: Model ID used
        usage_info: Dictionary with prompt_tokens, completion_tokens, total_tokens

    Returns:
        Dictionary with cost information
    """
    # Approximate pricing (in USD per 1M tokens)
    pricing = {
        'openai/gpt-3.5-turbo': {'input': 0.50, 'output': 1.50},
        'openai/gpt-4o': {'input': 2.50, 'output': 10.00},
        'openai/gpt-4-turbo': {'input': 10.00, 'output': 30.00},
        'anthropic/claude-3.5-sonnet': {'input': 3.00, 'output': 15.00},
        'meta-llama/llama-3.1-70b-instruct': {'input': 0.35, 'output': 0.40}
    }

    if model not in pricing or not usage_info:
        return {'estimated_cost': None, 'currency': 'USD'}

    prompt_tokens = usage_info.get('prompt_tokens', 0)
    completion_tokens = usage_info.get('completion_tokens', 0)

    input_cost = (prompt_tokens / 1_000_000) * pricing[model]['input']
    output_cost = (completion_tokens / 1_000_000) * pricing[model]['output']
    total_cost = input_cost + output_cost

    return {
        'estimated_cost': round(total_cost, 4),
        'input_cost': round(input_cost, 4),
        'output_cost': round(output_cost, 4),
        'currency': 'USD'
    }


def quick_tailor(resume_text: str, jd_text: str, model: str = None) -> Dict:
    """
    Quick one-shot resume tailoring (main function for UI).

    Args:
        resume_text: Original resume text
        jd_text: Job description text
        model: LLM model to use

    Returns:
        Complete tailoring results with before/after scores
    """
    # Import here to avoid circular dependency
    from .resume_analyzer import calculate_match_score

    # Calculate initial match score
    initial_analysis = calculate_match_score(resume_text, jd_text)
    initial_score = initial_analysis.get('overall_score', 0)

    # Tailor resume
    tailor_result = tailor_resume(
        resume_text,
        jd_text,
        initial_analysis,
        model=model,
        max_projects=config.MAX_PROJECTS_TO_TAILOR
    )

    if not tailor_result['success']:
        return {
            'success': False,
            'error': tailor_result.get('error', 'Unknown error'),
            'initial_score': initial_score
        }

    # Calculate new match score
    final_analysis = calculate_match_score(tailor_result['tailored_resume'], jd_text)
    final_score = final_analysis.get('overall_score', 0)

    # Calculate cost
    usage_info = tailor_result.get('usage_info', {})
    cost_info = calculate_estimated_cost(tailor_result.get('model_used'), usage_info)

    return {
        'success': True,
        'original_resume': resume_text,
        'tailored_resume': tailor_result['tailored_resume'],
        'summary': tailor_result['summary'],
        'initial_score': initial_score,
        'final_score': final_score,
        'improvement': final_score - initial_score,
        'initial_analysis': initial_analysis,
        'final_analysis': final_analysis,
        'model_used': tailor_result.get('model_used'),
        'tokens_used': tailor_result.get('tokens_used'),
        'usage_info': usage_info,
        'cost_info': cost_info
    }
