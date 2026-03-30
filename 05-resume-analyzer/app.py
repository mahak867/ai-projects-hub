import streamlit as st
import anthropic
import PyPDF2
import io
import json

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📋", layout="wide")
st.title("📋 AI Resume Analyzer")
st.caption("Upload your resume + paste a job description → get a detailed match analysis")

with st.sidebar:
    api_key = st.text_input("Anthropic API Key", type="password")
    st.divider()
    st.markdown("**How to use:**")
    st.markdown("1. Enter your API key")
    st.markdown("2. Upload your resume (PDF)")
    st.markdown("3. Paste the job description")
    st.markdown("4. Click Analyze")

def extract_pdf(file) -> str:
    reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
    return "\n".join(page.extract_text() for page in reader.pages if page.extract_text())

def analyze_resume(client, resume: str, jd: str) -> dict:
    prompt = f"""You are an expert HR consultant and career coach. Analyze this resume against the job description.

RESUME:
{resume[:8000]}

JOB DESCRIPTION:
{jd[:4000]}

Provide a detailed JSON analysis with these exact keys:
{{
  "match_score": <0-100 integer>,
  "match_level": "<Poor/Fair/Good/Excellent>",
  "summary": "<2-3 sentence overall assessment>",
  "matching_skills": ["skill1", "skill2", ...],
  "missing_skills": ["skill1", "skill2", ...],
  "experience_match": "<assessment of experience level match>",
  "education_match": "<assessment of education requirements>",
  "strengths": ["strength1", "strength2", "strength3"],
  "gaps": ["gap1", "gap2", "gap3"],
  "resume_improvements": [
    {{"section": "Summary", "suggestion": "..."}},
    {{"section": "Skills", "suggestion": "..."}},
    {{"section": "Experience", "suggestion": "..."}}
  ],
  "cover_letter_points": ["point1", "point2", "point3"],
  "interview_preparation": ["topic1", "topic2", "topic3"],
  "overall_recommendation": "<detailed recommendation>"
}}

Return ONLY valid JSON, no other text."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}]
    )
    
    raw = response.content[0].text.strip()
    # Strip markdown code fences if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())

col1, col2 = st.columns(2)
with col1:
    resume_file = st.file_uploader("Upload Resume (PDF)", type="pdf")
with col2:
    jd_text = st.text_area("Paste Job Description", height=300, 
                           placeholder="Copy and paste the full job description here...")

if st.button("🔍 Analyze Match", type="primary", use_container_width=True):
    if not api_key:
        st.error("Please enter your API key")
        st.stop()
    if not resume_file:
        st.error("Please upload your resume")
        st.stop()
    if not jd_text.strip():
        st.error("Please paste the job description")
        st.stop()
    
    with st.spinner("Analyzing your resume... (~15 seconds)"):
        client = anthropic.Anthropic(api_key=api_key)
        resume_text = extract_pdf(resume_file)
        result = analyze_resume(client, resume_text, jd_text)
    
    # Score display
    score = result["match_score"]
    level = result["match_level"]
    color = {"Poor": "red", "Fair": "orange", "Good": "blue", "Excellent": "green"}.get(level, "blue")
    
    st.markdown(f"""
    <div style="text-align:center; padding:20px; background:#f8f9fa; border-radius:12px; margin:16px 0">
        <div style="font-size:64px; font-weight:800; color:{'#22c55e' if score>=75 else '#f59e0b' if score>=50 else '#ef4444'}">{score}</div>
        <div style="font-size:18px; font-weight:600; color:#374151">Match Score / 100</div>
        <div style="font-size:14px; color:#6b7280">{level} Match</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.info(result["summary"])
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("✅ Matching Skills")
        for s in result.get("matching_skills", []):
            st.markdown(f"- {s}")
        
        st.subheader("💪 Your Strengths")
        for s in result.get("strengths", []):
            st.markdown(f"- {s}")
    
    with col2:
        st.subheader("❌ Missing Skills")
        for s in result.get("missing_skills", []):
            st.markdown(f"- {s}")
        
        st.subheader("🎯 Gaps to Address")
        for g in result.get("gaps", []):
            st.markdown(f"- {g}")
    
    st.subheader("✏️ How to Improve Your Resume")
    for imp in result.get("resume_improvements", []):
        with st.expander(f"📝 {imp['section']}"):
            st.write(imp['suggestion'])
    
    st.subheader("📬 Cover Letter Key Points")
    for p in result.get("cover_letter_points", []):
        st.markdown(f"- {p}")
    
    st.subheader("🎤 Interview Preparation Topics")
    for t in result.get("interview_preparation", []):
        st.markdown(f"- {t}")
    
    st.subheader("💡 Overall Recommendation")
    st.write(result.get("overall_recommendation", ""))
