"""
AIResume - Streamlit Frontend
Professional resume tailoring application with AI-powered optimization.
"""

import streamlit as st
from pathlib import Path
import config
from backend.file_parser import extract_text_from_uploaded_file
from backend.resume_analyzer import calculate_match_score, get_match_summary
from backend.resume_tailor import quick_tailor
from backend.document_generator import generate_resume_document


# Page configuration
st.set_page_config(
    page_title="AIResume - AI-Powered Resume Tailoring",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)


def init_session_state():
    """Initialize session state variables."""
    if 'resume_text' not in st.session_state:
        st.session_state.resume_text = None
    if 'jd_text' not in st.session_state:
        st.session_state.jd_text = None
    if 'initial_score' not in st.session_state:
        st.session_state.initial_score = None
    if 'tailoring_result' not in st.session_state:
        st.session_state.tailoring_result = None
    if 'initial_analysis' not in st.session_state:
        st.session_state.initial_analysis = None


def main():
    """Main application function."""
    init_session_state()

    # Header
    st.title("📄 AIResume")
    st.markdown("### AI-Powered Resume Tailoring for Job Applications")
    st.markdown("---")

    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")

        # Credit Balance Section
        st.subheader("💳 Account Balance")

        # Add refresh button
        col1, col2 = st.columns([3, 1])
        with col2:
            refresh_balance = st.button("🔄", help="Refresh balance")

        # Initialize balance in session state
        if 'balance_info' not in st.session_state or refresh_balance:
            from backend.resume_tailor import get_account_balance
            st.session_state.balance_info = get_account_balance()

        balance_info = st.session_state.balance_info

        if balance_info.get('success'):
            usage = balance_info.get('usage', 0)
            limit = balance_info.get('limit', 0)

            if limit and limit > 0:
                remaining = limit - usage
                usage_percent = (usage / limit) * 100

                # Display balance
                st.metric(
                    "Remaining Credits",
                    f"${remaining:.2f}",
                    delta=f"-{usage_percent:.1f}% used",
                    delta_color="inverse"
                )

                # Progress bar
                st.progress(usage_percent / 100)

                # Additional info
                with st.expander("💰 Credit Details"):
                    st.write(f"**Credit Limit:** ${limit:.2f}")
                    st.write(f"**Used:** ${usage:.2f}")
                    st.write(f"**Remaining:** ${remaining:.2f}")
                    st.write(f"**Usage:** {usage_percent:.1f}%")
                    if balance_info.get('is_free_tier'):
                        st.caption("🆓 Free Tier Account")
            else:
                st.info("💳 Pay-as-you-go account (no credit limit)")
        else:
            st.warning(f"⚠️ Unable to fetch balance: {balance_info.get('error', 'Unknown error')}")

        st.markdown("---")

        # Model selection with cost information
        st.subheader("🤖 AI Model Selection")

        # Create display options with name and cost
        model_display_options = [
            f"{model['name']} ({model['cost']})"
            for model in config.ALTERNATIVE_MODELS
        ]

        selected_model_display = st.selectbox(
            "Choose Model",
            options=model_display_options,
            index=0,
            help="Select the AI model for tailoring. GPT-3.5 is recommended (cheapest and most obedient)."
        )

        # Extract the actual model ID
        selected_model_index = model_display_options.index(selected_model_display)
        selected_model = config.ALTERNATIVE_MODELS[selected_model_index]["id"]
        selected_model_info = config.ALTERNATIVE_MODELS[selected_model_index]

        # Show model description
        st.caption(f"ℹ️ {selected_model_info['description']}")

        st.markdown("---")

        # Projects to tailor
        max_projects = st.slider(
            "Projects to Tailor",
            min_value=1,
            max_value=3,
            value=config.MAX_PROJECTS_TO_TAILOR,
            help="Number of recent projects to modify"
        )

        st.markdown("---")

        # Cost information
        st.info(f"""
        💰 **Cost Info:**
        - Selected: {selected_model_info['cost']}
        - 10 resumes ≈ ${float(selected_model_info['cost'].split('$')[1].split('/')[0]) * 10:.2f}
        - 50 resumes ≈ ${float(selected_model_info['cost'].split('$')[1].split('/')[0]) * 50:.2f}

        💡 **Tip:** Start with GPT-3.5 Turbo (cheapest, often best results for copy tasks!)
        """)

        st.markdown("---")
        st.info("📝 **Note:** Your ChatGPT/Claude subscriptions don't include API access. This tool uses pay-per-use API.")

    # Main content area
    col1, col2 = st.columns(2)

    with col1:
        st.header("📤 Upload Resume")
        resume_file = st.file_uploader(
            "Choose your resume file",
            type=['pdf', 'docx', 'txt'],
            help="Upload your current resume in PDF, DOCX, or TXT format"
        )

        if resume_file:
            try:
                with st.spinner("Extracting resume text..."):
                    st.session_state.resume_text = extract_text_from_uploaded_file(resume_file)
                st.success(f"✅ Resume loaded: {resume_file.name}")

                # Show preview
                with st.expander("📄 View Resume Text"):
                    st.text_area(
                        "Resume Content",
                        st.session_state.resume_text,
                        height=300,
                        disabled=True
                    )
            except Exception as e:
                st.error(f"❌ Error loading resume: {e}")

    with col2:
        st.header("📋 Job Description")

        # Option to upload or paste
        jd_input_method = st.radio(
            "Input method",
            options=["Upload File", "Paste Text"],
            horizontal=True
        )

        if jd_input_method == "Upload File":
            jd_file = st.file_uploader(
                "Choose job description file",
                type=['pdf', 'docx', 'txt'],
                help="Upload the job description"
            )

            if jd_file:
                try:
                    with st.spinner("Extracting job description..."):
                        st.session_state.jd_text = extract_text_from_uploaded_file(jd_file)
                    st.success(f"✅ Job description loaded: {jd_file.name}")

                    with st.expander("📄 View Job Description"):
                        st.text_area(
                            "JD Content",
                            st.session_state.jd_text,
                            height=300,
                            disabled=True
                        )
                except Exception as e:
                    st.error(f"❌ Error loading job description: {e}")

        else:  # Paste Text
            jd_text_input = st.text_area(
                "Paste job description here",
                height=300,
                placeholder="Copy and paste the job description text here..."
            )

            if jd_text_input:
                st.session_state.jd_text = jd_text_input
                st.success("✅ Job description loaded from text input")

    # Analysis section
    st.markdown("---")

    if st.session_state.resume_text and st.session_state.jd_text:
        # Calculate initial match score
        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:
            if st.button("🔍 Analyze Match Score", type="primary", use_container_width=True):
                with st.spinner("Analyzing match between resume and job description..."):
                    st.session_state.initial_analysis = calculate_match_score(
                        st.session_state.resume_text,
                        st.session_state.jd_text
                    )
                    st.session_state.initial_score = st.session_state.initial_analysis['overall_score']

        # Display initial score
        if st.session_state.initial_score is not None:
            st.markdown("### 📊 Current Match Analysis")

            score_col1, score_col2, score_col3 = st.columns(3)

            with score_col1:
                st.metric(
                    "Overall Match",
                    f"{st.session_state.initial_score:.1f}%",
                    help="Combined score based on keywords and technical skills"
                )

            with score_col2:
                tech_score = st.session_state.initial_analysis.get('technical_match', 0)
                st.metric(
                    "Technical Skills",
                    f"{tech_score:.1f}%",
                    help="Match percentage for technical skills"
                )

            with score_col3:
                keyword_score = st.session_state.initial_analysis.get('keyword_match', 0)
                st.metric(
                    "Keywords",
                    f"{keyword_score:.1f}%",
                    help="General keyword match percentage"
                )

            # Detailed analysis
            with st.expander("📈 Detailed Match Analysis"):
                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("✅ Matched Skills")
                    matched_tech = st.session_state.initial_analysis.get('matched_technical', set())
                    if matched_tech:
                        for skill in sorted(list(matched_tech))[:15]:
                            st.markdown(f"- {skill}")
                    else:
                        st.info("No technical skills matched")

                with col2:
                    st.subheader("❌ Missing Skills")
                    missing_tech = st.session_state.initial_analysis.get('missing_technical', set())
                    if missing_tech:
                        for skill in sorted(list(missing_tech))[:15]:
                            st.markdown(f"- {skill}")
                    else:
                        st.success("All technical skills matched!")

            # Tailoring button
            st.markdown("---")
            col1, col2, col3 = st.columns([1, 2, 1])

            with col2:
                if st.button("✨ Tailor Resume to Job Description", type="primary", use_container_width=True):
                    with st.spinner("🤖 AI is tailoring your resume... This may take 30-60 seconds..."):
                        try:
                            # Update max_projects in config temporarily
                            config.MAX_PROJECTS_TO_TAILOR = max_projects

                            # Tailor resume
                            st.session_state.tailoring_result = quick_tailor(
                                st.session_state.resume_text,
                                st.session_state.jd_text,
                                model=selected_model
                            )

                            if st.session_state.tailoring_result['success']:
                                st.success("✅ Resume tailored successfully!")

                                # Refresh balance after successful tailoring
                                from backend.resume_tailor import get_account_balance
                                st.session_state.balance_info = get_account_balance()
                            else:
                                st.error(f"❌ Error: {st.session_state.tailoring_result.get('error', 'Unknown error')}")

                        except Exception as e:
                            st.error(f"❌ Tailoring failed: {e}")
                            st.session_state.tailoring_result = None

    # Display tailoring results
    if st.session_state.tailoring_result and st.session_state.tailoring_result.get('success'):
        st.markdown("---")
        st.markdown("## 🎯 Tailoring Results")

        # Score comparison
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Initial Score",
                f"{st.session_state.tailoring_result['initial_score']:.1f}%"
            )

        with col2:
            st.metric(
                "Improved Score",
                f"{st.session_state.tailoring_result['final_score']:.1f}%",
                delta=f"+{st.session_state.tailoring_result['improvement']:.1f}%"
            )

        with col3:
            improvement = st.session_state.tailoring_result['improvement']
            if improvement > 10:
                st.success("🎉 Great improvement!")
            elif improvement > 5:
                st.info("👍 Good improvement!")
            else:
                st.warning("⚠️ Minor improvement")

        # Summary of changes
        st.markdown("### 📝 Summary of Changes")
        st.info(st.session_state.tailoring_result['summary'])

        # Tailored resume
        st.markdown("### 📄 Tailored Resume")
        with st.expander("View Tailored Resume", expanded=True):
            st.text_area(
                "Tailored Resume Content",
                st.session_state.tailoring_result['tailored_resume'],
                height=400,
                disabled=True
            )

        # Download section
        st.markdown("### ⬇️ Download Tailored Resume")

        download_col1, download_col2 = st.columns(2)

        with download_col1:
            # Generate DOCX
            docx_result = generate_resume_document(
                st.session_state.tailoring_result['tailored_resume'],
                format='docx'
            )

            if docx_result['success']:
                st.download_button(
                    label="📥 Download as DOCX",
                    data=docx_result['docx_bytes'],
                    file_name="tailored_resume.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )

        with download_col2:
            # Generate PDF
            pdf_result = generate_resume_document(
                st.session_state.tailoring_result['tailored_resume'],
                format='pdf'
            )

            if pdf_result['success']:
                st.download_button(
                    label="📥 Download as PDF",
                    data=pdf_result['pdf_bytes'],
                    file_name="tailored_resume.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

        # Cost and usage information
        st.markdown("### 💰 API Usage & Cost")

        usage_info = st.session_state.tailoring_result.get('usage_info', {})
        cost_info = st.session_state.tailoring_result.get('cost_info', {})

        cost_col1, cost_col2, cost_col3, cost_col4 = st.columns(4)

        with cost_col1:
            st.metric(
                "Total Tokens",
                f"{usage_info.get('total_tokens', 'N/A'):,}" if usage_info.get('total_tokens') else "N/A",
                help="Total tokens used (prompt + completion)"
            )

        with cost_col2:
            st.metric(
                "Prompt Tokens",
                f"{usage_info.get('prompt_tokens', 'N/A'):,}" if usage_info.get('prompt_tokens') else "N/A",
                help="Tokens in your input (resume + job description)"
            )

        with cost_col3:
            st.metric(
                "Completion Tokens",
                f"{usage_info.get('completion_tokens', 'N/A'):,}" if usage_info.get('completion_tokens') else "N/A",
                help="Tokens in AI's response (tailored resume)"
            )

        with cost_col4:
            estimated_cost = cost_info.get('estimated_cost')
            if estimated_cost is not None:
                st.metric(
                    "Estimated Cost",
                    f"${estimated_cost:.4f}",
                    help=f"Approximate cost for this operation"
                )
            else:
                st.metric("Estimated Cost", "N/A")

        # Additional details in expander
        with st.expander("ℹ️ Detailed Usage Information"):
            st.write(f"**Model Used:** {st.session_state.tailoring_result.get('model_used', 'N/A')}")
            st.write(f"**Total Tokens:** {usage_info.get('total_tokens', 'N/A')}")

            if cost_info.get('estimated_cost') is not None:
                st.write(f"**Input Cost:** ${cost_info.get('input_cost', 0):.4f}")
                st.write(f"**Output Cost:** ${cost_info.get('output_cost', 0):.4f}")
                st.write(f"**Total Cost:** ${cost_info.get('estimated_cost', 0):.4f} {cost_info.get('currency', 'USD')}")
                st.caption("💡 Costs are approximate and based on standard OpenRouter pricing. Actual costs may vary slightly.")

    elif st.session_state.resume_text is None and st.session_state.jd_text is None:
        # Welcome message
        st.info("""
        👋 **Welcome to AIResume!**

        **How it works:**
        1. Upload your current resume (PDF, DOCX, or TXT)
        2. Upload or paste the job description
        3. Click "Analyze Match Score" to see your current match
        4. Click "Tailor Resume" to optimize your resume for the job
        5. Download your tailored resume in PDF or DOCX format

        **Features:**
        - ✅ Preserves all dates and personal information
        - ✅ Modifies only job responsibilities and bullet points
        - ✅ Targets the most recent 1-2 projects
        - ✅ Incorporates relevant keywords from job description
        - ✅ Shows before/after match scores
        """)

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
        <p>AIResume - Powered by OpenRouter AI | Built with Streamlit</p>
        <p>GitHub: <a href='https://github.com/sthama121-del/AIResume' target='_blank'>sthama121-del/AIResume</a></p>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    try:
        config.validate_config()
        main()
    except ValueError as e:
        st.error(f"Configuration Error: {e}")
        st.info("Please ensure your .env file contains a valid OPENROUTER_API_KEY")
