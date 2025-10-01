# AIResume Constraints Checklist ✅

## 📋 Quick Reference

**For detailed section-level preservation rules, see:** [SECTION_PRESERVATION.md](SECTION_PRESERVATION.md)

### Key Principle
✅ **ONLY Experience section bullets (in recent 1-2 roles) are modified**
❌ **Professional Summary, Technical Skills, Education, Contact Info - NEVER modified**

---

## Your Specific Requirements - Implementation Status

### ✅ **IMPLEMENTED: Section-Level Preservation (NEW!)**
- **Constraint:** Professional Summary, Technical Skills, Education, Contact Info NEVER modified
- **How:** AI prompt explicitly lists 7 sections that must remain 100% unchanged
- **Sections Preserved:**
  1. Professional Summary (word-for-word)
  2. Technical Skills (no additions/removals)
  3. Education (all details)
  4. Contact Information (all details)
  5. Certifications (if present)
  6. Publications (if present)
  7. Awards (if present)
- **Only Modifiable:** Experience section bullets in recent 1-2 roles ONLY
- **File:** `backend/resume_tailor.py:80-91`
- **Documentation:** See `SECTION_PRESERVATION.md` for detailed examples

### ✅ **IMPLEMENTED: Preserve All Projects and Roles**
- **Constraint:** Never delete or invent companies
- **How:** AI prompt explicitly states "NEVER INVENT COMPANIES/PROJECTS" and "NEVER DELETE PROJECTS/ROLES"
- **File:** `backend/resume_tailor.py:73-74`

### ✅ **IMPLEMENTED: Reuse Original Responsibilities**
- **Constraint:** Only adjust phrasing, don't fabricate
- **How:** Prompt instructs "REPHRASE BULLET POINTS: Reuse original responsibility wording, adjust phrasing to highlight relevant skills"
- **File:** `backend/resume_tailor.py:80`

### ✅ **IMPLEMENTED: No Technology Fabrication**
- **Constraint:** Do not add tech not present in original
- **How:** Prompt includes "NO TECHNOLOGY FABRICATION: Only mention technologies/tools that already exist in the original resume"
- **File:** `backend/resume_tailor.py:76`
- **Example:** If JD requires Kubernetes but you don't have it → **AI will NOT add it**

### ✅ **IMPLEMENTED: Preserve Dates**
- **Constraint:** Project start/end dates unchanged
- **How:** "PRESERVE ALL DATES: Do not change any start dates, end dates, or date ranges"
- **File:** `backend/resume_tailor.py:75`

### ✅ **IMPLEMENTED: Tailor Only Recent 1-2 Projects**
- **Constraint:** Limit scope to recent projects
- **How:** Prompt specifies "ONLY IN {max_projects} MOST RECENT PROJECTS" (default: 2)
- **File:** `backend/resume_tailor.py:79`, `config.py:22`
- **UI Control:** Adjustable via sidebar slider (1-3 projects)

### ✅ **IMPLEMENTED: Maintain Bullet Count**
- **Constraint:** Keep bullets consistent (±1)
- **How:** "MAINTAIN BULLET COUNT: Keep same number of bullets (max ±1)"
- **File:** `backend/resume_tailor.py:83`

### ✅ **IMPLEMENTED: Emphasize Existing Strengths**
- **Constraint:** Focus on Snowflake, Databricks, Azure, MLflow, PySpark
- **How:** "EMPHASIZE EXISTING STRENGTHS: If resume mentions Snowflake/Databricks/Azure/MLflow/PySpark, emphasize these more prominently"
- **File:** `backend/resume_tailor.py:81`

### ✅ **IMPLEMENTED: No Advanced AI/ML Fabrication**
- **Constraint:** Don't add "LLM fine-tuning", "FSDP", etc. unless present
- **How:** "NO EXPERIENCE INVENTION: Do not add advanced methods (e.g., 'LLM fine-tuning', 'FSDP', 'model serving at scale') unless they're already present"
- **File:** `backend/resume_tailor.py:77`

### ✅ **IMPLEMENTED: Detailed Change Log**
- **Constraint:** Show what was modified
- **How:** Output includes detailed TAILORING SUMMARY with before/after comparison
- **Format:**
  ```
  - Original bullet: "..."
  - Modified to: "..."
  - Reason: Emphasized existing X to match JD
  **Technologies NOT Added:** [honest about gaps]
  **Factual Accuracy:** 100%
  ```
- **File:** `backend/resume_tailor.py:103-117`

### ✅ **IMPLEMENTED: Match Score Comparison**
- **Constraint:** Show before vs after scores
- **How:** UI displays initial score, then final score with improvement delta
- **File:** `app.py:217-235`
- **Display:** Side-by-side metrics with +X% improvement

### ✅ **IMPLEMENTED: Example-Driven Prompt**
- **Constraint:** AI needs clear examples
- **How:** Prompt includes explicit example of correct tailoring:
  ```
  Original: "Developed data pipelines using Python and SQL"
  IF resume has Snowflake: "... with Snowflake and Databricks"
  IF resume doesn't have them: "Developed scalable data pipelines..." (no tech added)
  ```
- **File:** `backend/resume_tailor.py:86-90`

## 🔍 Verification Steps

### Before Using
1. ✅ Read `SAFETY_FEATURES.md` - Understand constraints
2. ✅ Ensure your original resume is accurate
3. ✅ List all technologies you've actually used

### During Tailoring
1. ✅ Upload accurate resume
2. ✅ Review initial match score
3. ✅ Wait 30-60 seconds for AI processing

### After Tailoring
1. ✅ Read the TAILORING SUMMARY carefully
2. ✅ Check "Technologies NOT Added" section
3. ✅ Verify every modified bullet
4. ✅ Ensure you can defend all claims in interview
5. ✅ Download and review final resume

## 📊 Expected Behavior Examples

### Scenario 1: You Have the Tech
- **Resume:** "Used Python and Snowflake"
- **JD Requires:** Snowflake, Databricks
- **Result:** Emphasizes Snowflake, does NOT add Databricks (you don't have it)
- **Change Log:** "Technologies NOT Added: Databricks"

### Scenario 2: Phrasing Adjustment
- **Resume:** "Built ML models"
- **JD Language:** "MLOps pipelines"
- **Result:** "Built MLOps-driven ML models" (same concept, JD terminology)
- **Reason:** You did ML, just using their language

### Scenario 3: Adding Context
- **Resume:** "Led Python development"
- **JD Requires:** "7+ years Python"
- **Result:** "Led Python development (7+ years experience)" (if you have it)
- **Reason:** Adding duration context, not fabricating

### Scenario 4: NOT Adding Missing Tech
- **Resume:** No mention of "Kubernetes"
- **JD Requires:** "Kubernetes experience"
- **Result:** NO change, does NOT add Kubernetes
- **Change Log:** "Technologies NOT Added: Kubernetes (not in original)"

## 🎯 Match Score Reality Check

### Realistic Expectations
- **Before:** 60-75% (typical starting point)
- **After (honest tailoring):** 77-86%
- **Best case (you have most requirements):** 87-95%

### Warning Signs
- ❌ 100% match: Likely fabricated, suspicious to recruiters
- ❌ +30% improvement: Probably added fake experience
- ✅ 82-86% match: Perfect - shows fit without red flags

## 🛠️ Configuration Options

### Adjust Tailoring Aggressiveness
**File:** `config.py`

```python
MAX_PROJECTS_TO_TAILOR = 2        # Modify 1-3 recent projects
BULLET_VARIATION_ALLOWED = 1      # Allow ±1 bullet
TARGET_MATCH_SCORE_MIN = 77       # Realistic minimum
TARGET_MATCH_SCORE_MAX = 95       # Realistic maximum
```

### Choose AI Model
**UI:** Sidebar dropdown

- **Claude 3.5 Sonnet** (recommended - most conservative)
- **GPT-4 Turbo** (good, slightly more creative)
- **GPT-3.5 Turbo** (faster, less conservative)
- **LLaMA 3.1 70B** (experimental)

**Recommendation:** Use Claude 3.5 Sonnet for most accurate, conservative tailoring

## 📚 Documentation Files

1. **README.md** - Installation and usage
2. **QUICKSTART.md** - 3-minute setup guide
3. **SAFETY_FEATURES.md** - Detailed safety explanation (read this!)
4. **CONSTRAINTS_CHECKLIST.md** - This file

## ✅ Final Checklist Before Using

- [ ] I've read `SAFETY_FEATURES.md`
- [ ] My original resume is 100% accurate
- [ ] I understand the AI will NOT add technologies I don't have
- [ ] I'll review the change log after tailoring
- [ ] I can defend every claim in the tailored resume
- [ ] I'm okay with realistic match scores (77-86%), not 100%

## 🚀 Ready to Use

The app is running at: **http://localhost:8501**

Your resume will be tailored **conservatively and honestly** to emphasize your real strengths without fabrication.

---

**Remember:** The goal is to **optimize what you have**, not invent what you don't. 🎯
