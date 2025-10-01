# AIResume - AI-Powered Resume Tailoring

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**AIResume** is an intelligent resume tailoring application that uses AI to optimize your resume for specific job descriptions. It analyzes the match between your resume and a job posting, then intelligently modifies your resume to improve the match score while preserving dates, structure, and truthfulness.

## 🌟 Features

- **📤 Multi-Format Support**: Upload resumes and job descriptions in PDF, DOCX, or TXT format
- **🔍 Match Score Analysis**: Calculate detailed match scores between resume and job description
- **🤖 AI-Powered Tailoring**: Uses OpenRouter AI (Claude, GPT, LLaMA) to intelligently rewrite bullet points
- **📊 Before/After Comparison**: See your match score improvement side-by-side
- **✅ Smart Preservation**: Keeps all dates, personal info, and overall structure intact
- **🎯 Targeted Modifications**: Tailors only the most recent 1-2 projects
- **⬇️ Multiple Export Formats**: Download tailored resume as PDF or DOCX
- **📝 Change Summary**: Detailed explanation of what was modified and why

## 🎯 How It Works

1. **Upload Your Resume**: PDF, DOCX, or TXT format
2. **Provide Job Description**: Upload file or paste text
3. **Analyze Match**: See your current match score (typically 70-85%)
4. **Tailor Resume**: AI optimizes your resume for the job
5. **Download**: Get your tailored resume in PDF or DOCX format

The AI modifies only job responsibilities (bullet points) in your most recent 1-2 projects while:
- Preserving all dates and date ranges
- Maintaining bullet point count (±1)
- Keeping personal information unchanged
- Incorporating relevant keywords from the job description
- Adding quantifiable achievements where possible

## 📋 Prerequisites

- **Python 3.11 or higher**
- **macOS, Linux, or Windows**
- **OpenRouter API Key** (supports Claude, GPT, LLaMA, and more)

## 🚀 Installation

### 1. Clone the Repository

```bash
cd /Users/Sri/projects
git clone https://github.com/sthama121-del/AIResume.git
cd AIResume
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate  # On Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

The `.env` file is already configured with your OpenRouter API key:

```env
OPENROUTER_API_KEY=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
```

**Note**: The `.env` file is excluded from Git via `.gitignore` to protect your API key.

If you need to get a new API key:
1. Visit [OpenRouter](https://openrouter.ai/)
2. Sign up/login and create an API key
3. Replace the key in `.env`

## 🎮 Usage

### Running the Application

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

### Using the Interface

1. **Upload Resume** (left column)
   - Click "Browse files" or drag and drop
   - Supported formats: PDF, DOCX, TXT

2. **Provide Job Description** (right column)
   - Option 1: Upload file
   - Option 2: Paste text directly

3. **Analyze Match Score**
   - Click "🔍 Analyze Match Score"
   - View overall match percentage
   - See matched and missing skills

4. **Tailor Resume**
   - Click "✨ Tailor Resume to Job Description"
   - Wait 30-60 seconds for AI processing
   - Review the improved match score

5. **Download Tailored Resume**
   - Download as DOCX (editable)
   - Download as PDF (print-ready)

### Configuration Options (Sidebar)

- **Select AI Model**: Choose from Claude 3.5 Sonnet, GPT-4, GPT-3.5, or LLaMA
- **Projects to Tailor**: Set how many recent projects to modify (1-3)

## 📁 Project Structure

```
AIResume/
├── app.py                        # Streamlit frontend application
├── config.py                     # Configuration and environment setup
├── requirements.txt              # Python dependencies
├── .env                          # Environment variables (API keys)
├── .gitignore                    # Git ignore rules
├── README.md                     # This file
├── backend/
│   ├── __init__.py              # Package initialization
│   ├── file_parser.py           # Extract text from PDF/DOCX/TXT
│   ├── resume_analyzer.py       # Calculate match scores
│   ├── resume_tailor.py         # AI-powered resume tailoring
│   └── document_generator.py    # Generate PDF/DOCX outputs
└── uploads/                      # Temporary file storage (gitignored)
```

## 🔧 Configuration

### Changing AI Models

Edit `config.py` to modify the default model:

```python
DEFAULT_MODEL = "anthropic/claude-3.5-sonnet"  # Or any OpenRouter model
```

Available models:
- `anthropic/claude-3.5-sonnet` (recommended)
- `openai/gpt-4-turbo`
- `openai/gpt-3.5-turbo`
- `meta-llama/llama-3.1-70b-instruct`

### Adjusting Tailoring Parameters

In `config.py`:

```python
MAX_PROJECTS_TO_TAILOR = 2           # Number of recent projects to modify
BULLET_VARIATION_ALLOWED = 1         # Allow +1 or -1 bullets
TARGET_MATCH_SCORE_MIN = 77          # Minimum target score
TARGET_MATCH_SCORE_MAX = 95          # Maximum realistic score
```

## 📊 Match Score Breakdown

The match score is calculated using:

- **60% Technical Skills Match**: Programming languages, frameworks, tools, technologies
- **40% General Keywords Match**: Job-specific terminology, domain knowledge, soft skills

Target scores:
- **70-75%**: Basic match
- **77-86%**: Good match (typical result)
- **87-95%**: Excellent match (achievable with straightforward requirements)
- **95%+**: Rare (only for very specific JDs)

## 🛠️ Troubleshooting

### API Key Issues

**Error**: "OPENROUTER_API_KEY not found"

**Solution**: Ensure `.env` file exists in the project root with:
```env
OPENROUTER_API_KEY=your_key_here
```

### File Upload Issues

**Error**: "Unsupported file format"

**Solution**: Ensure files are in PDF, DOCX, or TXT format

### PDF Extraction Issues

**Error**: "Could not extract text from PDF"

**Solution**: Try these formats in order:
1. Save as text-based PDF (not scanned image)
2. Convert to DOCX
3. Copy text and paste as TXT

### Low Match Scores

If initial match score is very low (<50%):
- Ensure job description is complete
- Check that resume contains relevant technical skills
- Verify resume format is being parsed correctly

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [OpenRouter](https://openrouter.ai/) for providing unified LLM API access
- [Streamlit](https://streamlit.io/) for the amazing web framework
- [Anthropic](https://www.anthropic.com/) for Claude AI
- [OpenAI](https://openai.com/) for GPT models

## 📧 Contact

For questions, issues, or suggestions:

- **GitHub Issues**: [github.com/sthama121-del/AIResume/issues](https://github.com/sthama121-del/AIResume/issues)
- **GitHub**: [@sthama121-del](https://github.com/sthama121-del)

## 🚀 Future Enhancements

Planned features:
- [ ] Multi-language support
- [ ] Resume templates library
- [ ] Cover letter generation
- [ ] ATS compatibility checker
- [ ] Batch processing for multiple job descriptions
- [ ] Resume version history
- [ ] LinkedIn profile optimization
- [ ] Interview preparation based on tailored resume

## 📈 Version History

- **v1.0.0** (2024-10) - Initial release
  - Multi-format file support
  - AI-powered tailoring with OpenRouter
  - Match score analysis
  - PDF/DOCX export
  - Professional Streamlit UI

---

**Made with ❤️ by Sri | Powered by AI**
