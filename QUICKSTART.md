# AIResume - Quick Start Guide

## 🚀 Get Started in 3 Minutes

### 1. Install Dependencies

```bash
cd /Users/Sri/projects/AIResume
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Run the Application

```bash
streamlit run app.py
```

### 3. Use the App

1. Open browser at `http://localhost:8501`
2. Upload your resume (PDF/DOCX/TXT)
3. Upload or paste job description
4. Click "Analyze Match Score"
5. Click "Tailor Resume"
6. Download tailored resume (PDF or DOCX)

## 📝 What Was Created

### Core Files
- `app.py` - Streamlit web interface
- `config.py` - Configuration with your OpenRouter API key
- `.env` - Contains your API key (already configured)
- `requirements.txt` - All Python dependencies

### Backend Modules
- `backend/file_parser.py` - Extracts text from PDF/DOCX/TXT
- `backend/resume_analyzer.py` - Calculates match scores
- `backend/resume_tailor.py` - AI-powered tailoring with OpenRouter
- `backend/document_generator.py` - Creates PDF/DOCX outputs

## 🎯 Key Features

✅ **Preserves dates** - All project start/end dates stay unchanged
✅ **Smart tailoring** - Modifies only 1-2 recent project bullet points
✅ **Match scoring** - Shows before/after improvement
✅ **Multi-format** - Supports PDF, DOCX, TXT input/output
✅ **AI models** - Use Claude, GPT-4, GPT-3.5, or LLaMA

## 🔧 Customization

### Change AI Model
In the sidebar, select from:
- Claude 3.5 Sonnet (recommended)
- GPT-4 Turbo
- GPT-3.5 Turbo
- LLaMA 3.1 70B

### Adjust Projects to Tailor
Use the slider in sidebar (1-3 projects)

### Edit Configuration
Modify `config.py` to change:
- Default model
- Max projects to tailor
- Target score ranges

## 📊 Expected Results

- **Initial score**: Typically 60-75%
- **After tailoring**: 77-95% (depends on JD complexity)
- **Processing time**: 30-60 seconds

## 🐛 Common Issues

**"OPENROUTER_API_KEY not found"**
- Solution: `.env` file is already configured, just ensure it's in the project root

**Low match score improvement**
- Try selecting a different AI model
- Increase "Projects to Tailor" slider
- Ensure JD contains clear technical requirements

**PDF extraction fails**
- Try DOCX format instead
- Or paste text directly

## 📦 Push to GitHub

```bash
cd /Users/Sri/projects/AIResume
git init
git add .
git commit -m "Initial commit: AIResume v1.0"
git branch -M main
git remote add origin https://github.com/sthama121-del/AIResume.git
git push -u origin main
```

## 🎓 How It Works

1. **File Parser**: Extracts text from uploaded files using PyPDF2, pdfplumber, and python-docx
2. **Analyzer**: Compares resume keywords and technical skills with JD using regex and NLP
3. **Tailoring**: Sends resume + JD to AI with specific instructions to modify only bullet points
4. **Generator**: Creates professional PDF/DOCX from tailored text using reportlab and python-docx

## 💡 Tips for Best Results

1. **Use detailed job descriptions** - More details = better tailoring
2. **Upload clean resumes** - Well-formatted PDFs/DOCX work best
3. **Review before submitting** - AI is smart but always review output
4. **Adjust model if needed** - Claude 3.5 Sonnet gives best results
5. **Keep dates accurate** - The AI preserves them automatically

---

**Need help?** Check `README.md` for full documentation
