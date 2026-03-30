"""
Agentic Data Analyst
Upload any CSV -> Claude writes Python analysis code -> executes it -> returns insights + charts
"""
import anthropic
import pandas as pd
import io
import json
import subprocess
import sys
import tempfile
import os
import streamlit as st

st.set_page_config(page_title="AI Data Analyst", page_icon="📊", layout="wide")
st.title("📊 AI Data Analyst")
st.caption("Upload any CSV → get instant AI analysis, statistics, and insights")

client = anthropic.Anthropic(api_key=st.sidebar.text_input("Anthropic API Key", type="password"))

def safe_exec(code: str, df: pd.DataFrame) -> tuple[str, list]:
    """Execute pandas code safely, return output and any generated files"""
    with tempfile.TemporaryDirectory() as tmpdir:
        data_path = os.path.join(tmpdir, "data.csv")
        df.to_csv(data_path, index=False)

        script = f"""
import pandas as pd
import json
import sys
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv("{data_path}")

{code}
"""
        result = subprocess.run(
            [sys.executable, "-c", script],
            capture_output=True, text=True, timeout=30
        )
        return result.stdout + result.stderr, []

def analyze_dataset(df: pd.DataFrame, question: str = None) -> str:
    schema = {
        "shape": df.shape,
        "columns": {col: str(df[col].dtype) for col in df.columns},
        "sample": df.head(3).to_dict(),
        "missing": df.isnull().sum().to_dict(),
        "numeric_stats": df.describe().to_dict() if df.select_dtypes(include='number').shape[1] > 0 else {},
    }

    prompt = f"""You are a data analyst. Analyze this dataset and {'answer: ' + question if question else 'provide comprehensive insights'}.

DATASET INFO:
{json.dumps(schema, indent=2, default=str)}

{'QUESTION: ' + question if question else ''}

Write Python/pandas code to:
1. Answer the question (or do comprehensive EDA if no question)
2. Print key statistics and insights as clear text
3. Identify patterns, outliers, correlations

Format code between ```python and ``` markers.
After the code, provide a plain-text summary of what the analysis reveals.

Keep code simple and focused. Use only pandas, no matplotlib (for compatibility)."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )

    full_response = response.content[0].text

    # Extract and run code
    if "```python" in full_response:
        code = full_response.split("```python")[1].split("```")[0].strip()
        output, _ = safe_exec(code, df)

        # Get Claude to interpret the output
        if output.strip():
            interpret_response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=800,
                messages=[{
                    "role": "user",
                    "content": f"Interpret these analysis results in plain English for a business user. Be specific with numbers:\n\n{output}"
                }]
            )
            return f"**Analysis Output:**\n```\n{output[:2000]}\n```\n\n**Interpretation:**\n{interpret_response.content[0].text}"

    return full_response

uploaded = st.file_uploader("Upload CSV file", type="csv")

if uploaded:
    df = pd.read_csv(uploaded)
    st.success(f"Loaded: {df.shape[0]:,} rows × {df.shape[1]} columns")

    col1, col2 = st.columns([2, 1])
    with col1:
        st.dataframe(df.head(10), use_container_width=True)
    with col2:
        st.markdown("**Column Types**")
        for col in df.columns:
            st.text(f"{col}: {df[col].dtype}")

    st.divider()

    question = st.text_input("Ask a specific question about your data (optional)",
                             placeholder="e.g. What's the correlation between age and salary?")

    quick_qs = ["Give me a complete EDA summary", "Find outliers and anomalies",
                "What are the top trends?", "Identify missing data patterns"]
    selected = st.selectbox("Or choose a quick analysis:", ["Custom question above"] + quick_qs)
    final_q = question if question else (selected if selected != "Custom question above" else None)

    if st.button("🔍 Analyze", type="primary"):
        if not st.session_state.get("api_key_set") and not client.api_key:
            st.error("Please enter your API key")
        else:
            with st.spinner("Analyzing your data..."):
                result = analyze_dataset(df, final_q)
            st.markdown(result)
