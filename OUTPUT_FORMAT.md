# Resume Output Format Requirements

## ✅ **Critical: Clean, Professional Output Only**

The AI must output a **complete, recruiter-ready resume** with no meta-commentary.

---

## ❌ **INCORRECT Output Examples**

### Example 1: Meta-Text Preamble (WRONG)
```
I'll help tailor this resume for you. Here are the changes I'll make:
- Emphasize Snowflake experience
- Highlight MLOps skills
- Adjust terminology to match job description

JOHN DOE
john@email.com | 555-1234
...
```
**Problem:** Starts with explanation. Resume should start immediately with name.

### Example 2: Constraint Explanation (WRONG)
```
Based on your constraints, I will preserve the Professional Summary and Technical Skills sections while only modifying the Experience section bullets.

JOHN DOE
john@email.com | 555-1234
...
```
**Problem:** Includes meta-commentary about constraints.

### Example 3: Missing Sections (WRONG)
```
JOHN DOE
john@email.com | 555-1234

EXPERIENCE

Senior Data Engineer | AT&T | 2022-Present
• Developed enterprise-scale ETL pipelines...

[Education section missing]
[Professional Summary missing]
[Technical Skills missing]
```
**Problem:** Incomplete resume. All sections must be included.

---

## ✅ **CORRECT Output Format**

### The AI Should Output:

```
JOHN DOE
john@email.com | 555-1234 | San Francisco, CA | linkedin.com/in/johndoe

PROFESSIONAL SUMMARY
Data Engineer with 7+ years of experience building scalable data pipelines and cloud-based analytics solutions. Proven expertise in Python, SQL, Snowflake, and Azure.

TECHNICAL SKILLS
Languages: Python, SQL, R, Java
Cloud: Azure, AWS
Data Platforms: Snowflake, Databricks, Azure Synapse
Tools: PySpark, Airflow, MLflow, Docker, Git
ML/AI: Scikit-learn, TensorFlow, Azure ML

EXPERIENCE

Senior Data Engineer | AT&T | San Francisco, CA | Jan 2022 – Present
• Developed enterprise-scale ETL pipelines using Python (7+ years) and SQL, processing 10TB+ daily data volumes
• Built MLOps-driven machine learning models for customer churn prediction with Azure ML, improving retention by 15%
• Managed scalable cloud infrastructure on Azure, optimizing data engineering workflows and reducing costs by 20%
• Led cross-functional team of 5 engineers in implementing real-time data processing using PySpark and Kafka

Data Engineer | Cognizant | Chicago, IL | Mar 2020 – Dec 2021
• Created enterprise data warehouses with Snowflake for high-volume analytics, supporting 100+ business users
• Implemented real-time data processing pipelines using PySpark, reducing latency from hours to minutes
• Designed and deployed Azure Data Factory workflows for automated ETL processes
• Optimized SQL queries and database performance, improving query response time by 40%

Junior Developer | TCS | Mumbai, India | Jul 2018 – Feb 2020
• Wrote Python scripts for automation of data validation and reporting tasks
• Maintained legacy databases and performed routine database administration
• Collaborated with senior developers on data migration projects

EDUCATION
Bachelor of Science in Computer Science
Massachusetts Institute of Technology (MIT) | Cambridge, MA | 2018
GPA: 3.8/4.0
Relevant Coursework: Machine Learning, Database Systems, Algorithms

CERTIFICATIONS
- Azure Data Engineer Associate (Microsoft)
- Snowflake SnowPro Core Certification

---TAILORING SUMMARY---

**Sections Preserved (100% unchanged):**
- Professional Summary (word-for-word identical to original)
- Technical Skills (no additions - GenAI, Kubernetes NOT added despite JD requirement)
- Education (all details unchanged)
- Contact Information (all details unchanged)
- Certifications (unchanged)

**Roles Modified:** 2 (most recent only)
- AT&T - Senior Data Engineer: 4 bullets modified
- Cognizant - Data Engineer: 4 bullets modified

**Roles Preserved:** 1
- TCS - Junior Developer: 100% unchanged (older role outside top 2)

**Example Changes:**
- Original: "Developed ETL pipelines using Python and SQL"
- Modified: "Developed enterprise-scale ETL pipelines using Python (7+ years) and SQL, processing 10TB+ daily data volumes"
- Reason: Added "enterprise-scale" emphasis, highlighted years of experience, added quantifiable metric

- Original: "Built ML models for customer churn"
- Modified: "Built MLOps-driven machine learning models for customer churn prediction with Azure ML, improving retention by 15%"
- Reason: Used JD terminology "MLOps", emphasized Azure ML (already in skills), added impact metric

**Technologies NOT Added:**
- GenAI / Generative AI (required by JD but not in original resume)
- Kubernetes (required by JD but not in original resume)
- LLM fine-tuning (not in original resume)

**Factual Accuracy:** 100% - No fabricated experience. All technologies mentioned (Python, Snowflake, Azure, PySpark, MLflow) were already in the original Technical Skills section.
```

---

## 📋 **Output Structure Checklist**

The AI output must include, in this order:

### 1. **Contact Information** (First Line)
- Start immediately with name
- Include email, phone, location, LinkedIn

### 2. **Professional Summary**
- Exact same as original (word-for-word)
- No modifications

### 3. **Technical Skills**
- Exact same list as original
- No additions (even if JD requires them)
- No removals
- No reordering

### 4. **Experience Section**
- All roles included
- Company names, titles, dates unchanged
- Recent 1-2 roles: Bullets modified
- Older roles: Bullets 100% unchanged

### 5. **Education**
- Exact same as original
- All degrees, schools, dates, GPA unchanged

### 6. **Other Sections** (if present)
- Certifications: Unchanged
- Publications: Unchanged
- Awards: Unchanged
- Patents: Unchanged

### 7. **Tailoring Summary** (at end)
- Separated by "---TAILORING SUMMARY---"
- Lists what was preserved
- Lists what was modified
- Lists technologies NOT added
- Confirms factual accuracy

---

## 🎯 **What Makes Output "Recruiter-Ready"**

### ✅ Ready to Send
- Starts with name and contact info
- All sections present and complete
- Professional formatting
- No meta-commentary
- No explanation of changes (those are in summary section at end)

### ❌ Not Ready to Send
- Starts with "I'll help you..."
- Missing sections (Summary, Skills, Education)
- Includes constraint explanations in body
- Truncated or incomplete

---

## 💡 **Why This Matters**

### User Experience
- Users can **copy-paste directly** from output
- No need to remove meta-text
- Download buttons create clean PDF/DOCX

### Professional Quality
- Looks like a human-written resume
- Ready for ATS systems
- Ready for recruiter review

### Time Savings
- No manual cleanup required
- No section removal needed
- Immediate usability

---

## 🔍 **Verification**

After running the application, the tailored resume should:

1. [ ] Start with name on first line
2. [ ] Include Professional Summary (unchanged)
3. [ ] Include Technical Skills (unchanged)
4. [ ] Include all Experience roles
5. [ ] Include Education (unchanged)
6. [ ] Include all original sections
7. [ ] End with "---TAILORING SUMMARY---"
8. [ ] Summary explains what was changed
9. [ ] Lists technologies NOT added

**No meta-text, no preambles, no constraint explanations in the resume body.**

---

## 🛠️ **Implementation**

### System Message
```
"You are an expert resume writer with deep knowledge of ATS systems and recruitment best practices.
CRITICAL: Output ONLY the clean, professional resume document starting with the candidate's name.
Do NOT include any meta-text, preambles, or explanations. Start directly with resume content.
The output must be ready to send to recruiters with no additional editing needed."
```

### Prompt Instructions
```
**DO NOT INCLUDE:**
- ❌ Any meta-text like "I'll help tailor this resume"
- ❌ Any explanation of constraints or process
- ❌ Any preamble or introduction
- ❌ Any comments about what you're doing

**YOU MUST:**
- ✅ Start IMMEDIATELY with the resume content (name, contact info on first line)
- ✅ Include ALL sections: Professional Summary, Technical Skills, Education, Experience
- ✅ Make it look like a complete, professional resume
- ✅ End with "---TAILORING SUMMARY---"
```

### File Location
**Implementation:** `backend/resume_tailor.py:115-166` (prompt formatting)
**System Message:** `backend/resume_tailor.py:237-240` (LLM call)

---

## ✅ **Summary**

| Output Component | Status |
|-----------------|--------|
| Name & Contact (first line) | ✅ Required |
| Professional Summary | ✅ Required (unchanged) |
| Technical Skills | ✅ Required (unchanged) |
| Experience (all roles) | ✅ Required (recent bullets modified) |
| Education | ✅ Required (unchanged) |
| Other sections | ✅ Required if in original (unchanged) |
| Tailoring Summary | ✅ Required (at end after "---") |
| Meta-text / preamble | ❌ Forbidden |
| Constraint explanations | ❌ Forbidden |

**The output must be a complete, clean resume ready for recruiters with no additional editing needed.**
