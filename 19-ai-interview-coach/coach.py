"""AI Interview Coach — mock interviews with scoring and detailed feedback"""
import anthropic, json, streamlit as st

st.set_page_config(page_title="AI Interview Coach", page_icon="🎤", layout="wide")
st.title("🎤 AI Interview Coach")
st.caption("Practice interviews with Claude — get scored feedback on every answer")

client = anthropic.Anthropic(api_key=st.sidebar.text_input("Anthropic API Key", type="password"))

with st.sidebar:
    role = st.text_input("Target Role", placeholder="Software Engineer at Google")
    jd = st.text_area("Job Description (optional)", height=150)
    interview_type = st.selectbox("Interview Type", ["Technical", "Behavioral", "System Design", "Case Study", "HR"])
    difficulty = st.selectbox("Difficulty", ["Entry Level", "Mid Level", "Senior", "Staff/Principal"])

def generate_question(role: str, jd: str, q_type: str, difficulty: str, asked: list[str]) -> str:
    asked_str = "\n".join(asked[-5:]) if asked else "None yet"
    r = client.messages.create(model="claude-sonnet-4-20250514", max_tokens=300,
        messages=[{"role": "user", "content": f"""Generate one {q_type} interview question for a {difficulty} {role} position.

Job description context: {jd[:500] if jd else 'Not provided'}
Already asked: {asked_str}

Generate a NEW question not similar to ones already asked. Return ONLY the question, nothing else."""}])
    return r.content[0].text.strip()

def evaluate_answer(question: str, answer: str, role: str, q_type: str) -> dict:
    r = client.messages.create(model="claude-sonnet-4-20250514", max_tokens=1000,
        messages=[{"role": "user", "content": f"""Evaluate this interview answer for a {role} position.

QUESTION: {question}
ANSWER: {answer}

Provide JSON evaluation:
{{
  "overall_score": <0-10>,
  "grade": "<A/B/C/D/F>",
  "strengths": ["strength1", "strength2"],
  "improvements": ["improvement1", "improvement2"],
  "missing_elements": ["what was missing"],
  "better_answer_structure": "<how to structure a better answer>",
  "sample_strong_answer": "<a stronger version of the answer>",
  "communication_score": <0-10>,
  "content_score": <0-10>,
  "specific_feedback": "<2-3 sentences of specific, actionable feedback>"
}}
Return ONLY valid JSON."""}])
    raw = r.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"): raw = raw[4:]
    return json.loads(raw.strip())

if "questions" not in st.session_state:
    st.session_state.questions = []
    st.session_state.answers = []
    st.session_state.scores = []
    st.session_state.current_q = None

if not role:
    st.info("Enter your target role in the sidebar to start")
    st.stop()

col1, col2 = st.columns([2, 1])

with col1:
    if st.button("🎯 Get Next Question", type="primary"):
        with st.spinner("Generating question..."):
            q = generate_question(role, jd, interview_type, difficulty, st.session_state.questions)
            st.session_state.current_q = q

    if st.session_state.current_q:
        st.markdown("### Current Question")
        st.info(st.session_state.current_q)
        answer = st.text_area("Your Answer:", height=200, placeholder="Type your answer here... (aim for 2-3 minutes worth of speech)")

        if st.button("📊 Submit & Get Feedback"):
            if not answer.strip():
                st.warning("Please write an answer first")
            else:
                with st.spinner("Evaluating your answer..."):
                    evaluation = evaluate_answer(st.session_state.current_q, answer, role, interview_type)
                
                score = evaluation.get("overall_score", 0)
                grade = evaluation.get("grade", "?")
                color = "green" if score >= 8 else "orange" if score >= 6 else "red"

                st.markdown(f"### Score: :{color}[{score}/10 — Grade {grade}]")

                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("**✅ Strengths**")
                    for s in evaluation.get("strengths", []):
                        st.markdown(f"- {s}")
                with c2:
                    st.markdown("**📈 Improvements**")
                    for i in evaluation.get("improvements", []):
                        st.markdown(f"- {i}")

                with st.expander("💡 Better Answer Structure"):
                    st.write(evaluation.get("better_answer_structure", ""))

                with st.expander("⭐ Sample Strong Answer"):
                    st.write(evaluation.get("sample_strong_answer", ""))

                st.info(evaluation.get("specific_feedback", ""))

                st.session_state.questions.append(st.session_state.current_q)
                st.session_state.answers.append(answer)
                st.session_state.scores.append(score)
                st.session_state.current_q = None

with col2:
    if st.session_state.scores:
        avg = sum(st.session_state.scores) / len(st.session_state.scores)
        st.metric("Questions Answered", len(st.session_state.scores))
        st.metric("Average Score", f"{avg:.1f}/10")

        st.markdown("**Score History**")
        for i, (q, s) in enumerate(zip(st.session_state.questions, st.session_state.scores), 1):
            color = "🟢" if s >= 8 else "🟡" if s >= 6 else "🔴"
            st.text(f"{color} Q{i}: {s}/10")

        if st.button("📋 Generate Final Report"):
            report_prompt = f"""Generate a final interview performance report.
Role: {role} | Type: {interview_type}
Questions: {len(st.session_state.questions)}
Scores: {st.session_state.scores}
Average: {avg:.1f}/10

Provide: Overall readiness assessment, top 3 strengths, top 3 areas to improve, specific preparation recommendations, and honest verdict on readiness for this role."""
            with st.spinner("Generating report..."):
                r = client.messages.create(model="claude-sonnet-4-20250514", max_tokens=800,
                    messages=[{"role": "user", "content": report_prompt}])
            st.markdown(r.content[0].text)
