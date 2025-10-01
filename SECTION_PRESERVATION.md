# Resume Section Preservation Rules

## 🛡️ **Critical: What Gets Modified vs Preserved**

AIResume follows **strict section-level rules** to ensure your resume integrity.

---

## ✅ **Sections That Are 100% PRESERVED (Never Modified)**

### 1. **Professional Summary / Objective**
- **Preserved:** 100% - Word-for-word
- **Rationale:** This is your elevator pitch and should remain your voice
- **AI will:** Keep exactly as written
- **AI will NOT:** Rephrase, add keywords, or modify in any way

### 2. **Technical Skills Section**
- **Preserved:** 100% - No additions, removals, or modifications
- **Rationale:** This is your definitive skill list
- **AI will:** Keep all skills exactly as listed
- **AI will NOT:** Add JD-required skills not in your list
- **Note:** Even if JD requires "Kubernetes" and you don't have it, AI will NOT add it here

### 3. **Education**
- **Preserved:** 100% - All details unchanged
- **What's preserved:**
  - Degree names
  - University/College names
  - Graduation dates
  - GPA (if present)
  - Honors/Awards (if present)
- **AI will NOT:** Modify anything in this section

### 4. **Contact Information**
- **Preserved:** 100% - Exact details
- **What's preserved:**
  - Full name
  - Email address
  - Phone number
  - Location/Address
  - LinkedIn profile
  - GitHub profile
  - Portfolio links

### 5. **Certifications**
- **Preserved:** 100% - If present
- **AI will NOT:** Add, remove, or modify certifications

### 6. **Publications**
- **Preserved:** 100% - If present
- **AI will NOT:** Modify titles, dates, or co-authors

### 7. **Awards / Honors**
- **Preserved:** 100% - If present
- **AI will NOT:** Add or modify awards

### 8. **Patents**
- **Preserved:** 100% - If present
- **AI will NOT:** Modify patent details

---

## 🔧 **Section That CAN Be Modified**

### **EXPERIENCE SECTION ONLY**

**What can be modified:**
- Only the **most recent 1-2 roles** (configurable)
- Only the **bullet points** under those roles

**What stays unchanged even in Experience:**
- ✅ Company names
- ✅ Job titles
- ✅ Start dates
- ✅ End dates
- ✅ Location
- ✅ All older roles (beyond recent 1-2)

---

## 📊 **Visual Breakdown**

### Your Resume Structure

```
┌─────────────────────────────────────────┐
│ [NAME] - NEVER MODIFIED                 │
│ [Contact Info] - NEVER MODIFIED         │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ PROFESSIONAL SUMMARY                    │
│ [Your summary text]                     │
│ ❌ NEVER MODIFIED                       │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ TECHNICAL SKILLS                        │
│ • Python, Snowflake, Databricks...      │
│ ❌ NEVER MODIFIED                       │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ EXPERIENCE                              │
│                                         │
│ [Company 1] - [Title] (2022-Present)    │
│ ✅ CAN MODIFY BULLETS (most recent)    │
│ • Bullet 1 ← Can be rephrased          │
│ • Bullet 2 ← Can be rephrased          │
│                                         │
│ [Company 2] - [Title] (2020-2022)      │
│ ✅ CAN MODIFY BULLETS (if within top 2)│
│ • Bullet 1 ← Can be rephrased          │
│ • Bullet 2 ← Can be rephrased          │
│                                         │
│ [Company 3] - [Title] (2018-2020)      │
│ ❌ NEVER MODIFIED (older role)         │
│ • Bullet 1 ← Stays exactly as-is       │
│ • Bullet 2 ← Stays exactly as-is       │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ EDUCATION                               │
│ [Degree, University, Date]              │
│ ❌ NEVER MODIFIED                       │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ CERTIFICATIONS (if present)             │
│ [Your certifications]                   │
│ ❌ NEVER MODIFIED                       │
└─────────────────────────────────────────┘
```

---

## 🎯 **Detailed Example**

### Original Resume

```
JOHN DOE
john@email.com | 555-1234 | San Francisco, CA

PROFESSIONAL SUMMARY
Data Engineer with 7 years of experience in building scalable data pipelines.

TECHNICAL SKILLS
Python, SQL, Snowflake, Databricks, Azure, PySpark, Airflow

EXPERIENCE

Senior Data Engineer | AT&T | 2022-Present
• Developed ETL pipelines using Python and SQL
• Built ML models for customer churn prediction
• Managed cloud infrastructure on Azure

Data Engineer | Cognizant | 2020-2022
• Created data warehouses with Snowflake
• Implemented real-time data processing

Junior Developer | TCS | 2018-2020
• Wrote Python scripts for automation
• Maintained legacy databases

EDUCATION
B.S. Computer Science | MIT | 2018
GPA: 3.8/4.0
```

### Job Description Requires
- 5 years Python ✅ (you have 7)
- Snowflake experience ✅ (you have it)
- GenAI/LLM experience ❌ (you don't have it)
- Kubernetes ❌ (you don't have it)

### After Tailoring (Setting: Modify 2 most recent roles)

```
JOHN DOE
john@email.com | 555-1234 | San Francisco, CA
← NO CHANGES (Contact preserved)

PROFESSIONAL SUMMARY
Data Engineer with 7 years of experience in building scalable data pipelines.
← NO CHANGES (Summary preserved 100%)

TECHNICAL SKILLS
Python, SQL, Snowflake, Databricks, Azure, PySpark, Airflow
← NO CHANGES (Skills list preserved 100%, Kubernetes NOT added)

EXPERIENCE

Senior Data Engineer | AT&T | 2022-Present
← Company, title, dates UNCHANGED
• Developed enterprise-scale ETL pipelines using Python (7+ years) and SQL
  ← MODIFIED: Added "enterprise-scale" and "7+ years" context
• Built MLOps-driven ML models for customer churn prediction with Azure ML
  ← MODIFIED: Used "MLOps-driven" terminology, emphasized Azure
• Managed scalable cloud infrastructure on Azure with focus on data engineering
  ← MODIFIED: Added "scalable" and "data engineering" emphasis

Data Engineer | Cognizant | 2020-2022
← Company, title, dates UNCHANGED
• Created enterprise data warehouses with Snowflake for high-volume analytics
  ← MODIFIED: Added "enterprise" and "high-volume analytics"
• Implemented real-time data processing pipelines using PySpark
  ← MODIFIED: Added "pipelines" and "PySpark" (already in skills)

Junior Developer | TCS | 2018-2020
← Company, title, dates UNCHANGED
• Wrote Python scripts for automation
  ← NO CHANGES (older role, preserved)
• Maintained legacy databases
  ← NO CHANGES (older role, preserved)

EDUCATION
B.S. Computer Science | MIT | 2018
GPA: 3.8/4.0
← NO CHANGES (Education preserved 100%)
```

### Change Log Would Show

```
TAILORING SUMMARY

Sections Preserved (100% unchanged):
✓ Professional Summary
✓ Technical Skills (GenAI, Kubernetes NOT added despite JD requirement)
✓ Education
✓ Contact Information

Roles Modified: 2 (most recent only)
- AT&T - Senior Data Engineer (2022-Present): 3 bullets modified
- Cognizant - Data Engineer (2020-2022): 2 bullets modified

Roles Preserved:
- TCS - Junior Developer (2018-2020): 100% unchanged (older role)

Technologies NOT Added:
- GenAI/LLM (not in original resume)
- Kubernetes (not in original resume)

Factual Accuracy: 100%
```

---

## ❌ **What AI Will NEVER Do**

### To Professional Summary
- ❌ Add keywords
- ❌ Rephrase sentences
- ❌ Add experience claims
- ❌ Modify tone or style

### To Technical Skills
- ❌ Add skills from JD
- ❌ Remove skills
- ❌ Reorder skills
- ❌ Add proficiency levels

### To Education
- ❌ Change degree names
- ❌ Modify GPA
- ❌ Add coursework
- ❌ Change dates

### To Experience Section (Older Roles)
- ❌ Modify bullets in roles beyond recent 1-2
- ❌ Add or remove roles
- ❌ Change company names or titles

---

## ⚙️ **Configuration**

### Control How Many Recent Roles to Modify

**In App (Sidebar):**
- Slider: "Projects to Tailor" (1-3)
- Default: 2 roles

**In Code (config.py):**
```python
MAX_PROJECTS_TO_TAILOR = 2  # Modify only 2 most recent roles
```

### Example Scenarios

**Setting: 1 role**
- Modifies: Only most recent position
- Preserves: All other positions unchanged

**Setting: 2 roles** (default)
- Modifies: 2 most recent positions
- Preserves: All older positions unchanged

**Setting: 3 roles**
- Modifies: 3 most recent positions
- Preserves: All older positions unchanged

---

## 🔍 **Verification Checklist**

After tailoring, verify:

### ✅ Unchanged Sections
- [ ] Professional Summary is word-for-word identical
- [ ] Technical Skills list is identical (no additions)
- [ ] Education section is identical
- [ ] Contact info is identical
- [ ] Certifications (if present) are identical

### ✅ Modified Sections
- [ ] Only recent 1-2 roles have modified bullets
- [ ] Company names unchanged
- [ ] Job titles unchanged
- [ ] Dates unchanged
- [ ] Older roles completely unchanged

### ✅ Factual Accuracy
- [ ] No technologies added that weren't in original
- [ ] No fabricated experience claims
- [ ] Change log lists "Technologies NOT Added"

---

## 💡 **Why This Structure?**

### Professional Summary
**Reason for preservation:** This is your personal brand statement, carefully crafted in your voice. Modifying it risks losing authenticity.

### Technical Skills
**Reason for preservation:** This is your authoritative skill inventory. Adding skills you don't have creates interview problems.

**Better approach:** If you need to add a skill for a job, learn it first, then update your resume.

### Education
**Reason for preservation:** Factual records that can be verified. Never modified.

### Experience - Older Roles
**Reason for preservation:** Recent roles are most relevant to current job search. Older roles provide history but shouldn't be tailored (less relevant).

### Experience - Recent Roles Only
**Reason for modification allowed:** Most recent 1-2 roles are most relevant to target job. Rephrasing bullets to emphasize existing relevant experience improves ATS matching without fabrication.

---

## 🎓 **Best Practices**

1. **Before uploading:**
   - Ensure your Professional Summary is strong
   - Verify your Technical Skills list is complete and accurate
   - Update your resume with any new skills you've actually learned

2. **When tailoring:**
   - Set "Projects to Tailor" to 1-2 (not 3) for most conservative approach
   - Review change log carefully
   - Verify all sections outside Experience are preserved

3. **After tailoring:**
   - Compare Professional Summary word-for-word (should be identical)
   - Check Technical Skills (should be identical, no additions)
   - Verify older roles in Experience are unchanged

---

## ✅ **Summary**

| Section | Modification Status |
|---------|-------------------|
| Contact Info | ❌ Never modified |
| Professional Summary | ❌ Never modified |
| Technical Skills | ❌ Never modified |
| **Experience (Recent 1-2 roles)** | ✅ **Bullets can be rephrased** |
| Experience (Older roles) | ❌ Never modified |
| Education | ❌ Never modified |
| Certifications | ❌ Never modified |
| Publications | ❌ Never modified |
| Awards | ❌ Never modified |

**Only the bullet points in your most recent 1-2 roles are modified. Everything else stays exactly as you wrote it.**
