import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import traceback
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

# ── Page Config ───────────────────────────────────────────
st.set_page_config(
    page_title="AI Data Analyst",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
.chat-user   { background:#1a56db; border-left:4px solid #1240a8;
               padding:10px 15px; border-radius:6px; margin:8px 0;
               color:#ffffff; }
.chat-ai     { background:#f0f0f0; border-left:4px solid #27ae60;
               padding:10px 15px; border-radius:6px; margin:8px 0;
               color:#000000; }
.code-block  { background:#1e1e1e; color:#d4d4d4; padding:12px;
               border-radius:6px; font-size:13px; margin:6px 0; }
.metric-card { background:#ffffff; border:1px solid #e0e0e0;
               border-radius:8px; padding:12px; text-align:center; }
</style>
""", unsafe_allow_html=True)

# ── Helper Functions ──────────────────────────────────────
def get_dataframe_context(df):
    return f"""
You have access to a pandas DataFrame called `df`:
Shape: {df.shape[0]} rows × {df.shape[1]} columns
Columns and Types:\n{df.dtypes.to_string()}
Sample (first 3 rows):\n{df.head(3).to_string()}
Missing Values:\n{df.isnull().sum().to_string()}
Statistics:\n{df.describe().to_string()}
Unique values in categorical columns:
{chr(10).join([f"  {col}: {df[col].dropna().unique()[:10].tolist()}" for col in df.select_dtypes(include='object').columns])}
"""

def generate_code(question, df, llm, chat_history):
    history_text = ""
    if chat_history:
        history_text = "\n\nPrevious conversation:\n"
        for turn in chat_history[-4:]:
            history_text += f"User: {turn['question']}\nResult: {str(turn['result'])[:200]}\n\n"

    messages = [
        SystemMessage(content=f"""You are an expert data analyst who writes precise Pandas code.
{get_dataframe_context(df)}{history_text}
STRICT RULES:
1. Write code that works on DataFrame `df`
2. Store final result in variable called `result`
3. result must be: DataFrame, Series, scalar, or dict
4. No print() statements
5. No imports — pandas (pd) and numpy (np) already available
6. Handle missing values with dropna() or fillna()
7. Return ONLY Python code — no markdown, no backticks, no explanation"""),
        HumanMessage(content=f"Question: {question}\n\nWrite the Pandas code:")
    ]

    code = llm.invoke(messages).content.strip()
    for marker in ["```python", "```"]:
        if marker in code:
            code = code.split(marker)[1].split("```")[0].strip()
            break
    return code

def execute_code(code, df):
    local_vars = {"df": df.copy(), "pd": pd, "np": np, "result": None}
    try:
        exec(code, {"__builtins__": {}}, local_vars)
        result = local_vars.get("result")
        if result is None:
            return None, "⚠️ No `result` variable was set."
        return result, None
    except Exception:
        return None, traceback.format_exc()

def run_pipeline(question, df, llm, chat_history):
    code = generate_code(question, df, llm, chat_history)
    result, error = execute_code(code, df)

    if error:
        fix = llm.invoke([
            SystemMessage(content="Fix this Pandas code. Return ONLY corrected code."),
            HumanMessage(content=f"Code:\n{code}\n\nError:\n{error}\n\nFixed:")
        ]).content.strip()
        for marker in ["```python", "```"]:
            if marker in fix:
                fix = fix.split(marker)[1].split("```")[0].strip()
                break
        result, error = execute_code(fix, df)
        code = fix

    if result is not None:
        chat_history.append({"question": question, "code": code, "result": result, "error": error})

    return result, code, error, chat_history

def generate_chart(result, question, llm):
    decision = llm.invoke([
        SystemMessage(content="""You are a data visualization expert.
Reply with ONLY one word: bar, line, pie, scatter, histogram, none
- bar: category comparisons
- line: trends over time
- pie: proportions
- scatter: two numeric columns
- histogram: single numeric distribution
- none: scalar or complex result"""),
        HumanMessage(content=f"Question: {question}\nResult type: {type(result).__name__}\nPreview: {str(result)[:300]}")
    ]).content.strip().lower()

    fig = None
    try:
        if decision == "bar" and hasattr(result, "reset_index"):
            plot_df = result.reset_index()
            plot_df.columns = [str(c) for c in plot_df.columns]
            fig = px.bar(plot_df, x=plot_df.columns[0], y=plot_df.columns[1],
                         title=question, color=plot_df.columns[0], template="plotly_white")
        elif decision == "pie" and hasattr(result, "reset_index"):
            plot_df = result.reset_index()
            plot_df.columns = [str(c) for c in plot_df.columns]
            fig = px.pie(plot_df, names=plot_df.columns[0], values=plot_df.columns[1],
                         title=question, template="plotly_white")
        elif decision == "line" and hasattr(result, "reset_index"):
            plot_df = result.reset_index()
            plot_df.columns = [str(c) for c in plot_df.columns]
            fig = px.line(plot_df, x=plot_df.columns[0], y=plot_df.columns[1],
                          title=question, template="plotly_white", markers=True)
        elif decision == "histogram" and hasattr(result, "values"):
            fig = px.histogram(x=result.values, title=question, template="plotly_white")
        elif decision == "scatter" and hasattr(result, "reset_index"):
            plot_df = result.reset_index()
            plot_df.columns = [str(c) for c in plot_df.columns]
            fig = px.scatter(plot_df, x=plot_df.columns[0], y=plot_df.columns[1],
                             title=question, template="plotly_white")
    except Exception:
        fig = None

    return fig, decision

def format_result(result):
    if isinstance(result, pd.DataFrame):
        return result
    elif isinstance(result, pd.Series):
        return result.reset_index()
    elif isinstance(result, dict):
        return pd.DataFrame(list(result.items()), columns=["Key", "Value"])
    else:
        return result

# ── Main App ──────────────────────────────────────────────
st.title("📊 Conversation-Style AI Data Analyst")
st.markdown("Upload any CSV and chat with your data in plain English.")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    model   = st.selectbox("Model", ["llama-3.1-8b-instant", "llama3-8b-8192"])
    st.markdown("---")
    st.markdown("### 💡 Sample Questions")
    st.markdown("""
- What is the average price per category?
- How many products are out of stock?
- Which category has the highest rating?
- Show the discount distribution
- What is the price range for each category?
- Which category has the most missing ratings?
""")
    st.markdown("---")
    if st.button("🗑️ Clear Conversation"):
        st.session_state.chat_history = []
        st.session_state.messages     = []
        st.rerun()

# Session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "messages" not in st.session_state:
    st.session_state.messages = []
if "df" not in st.session_state:
    st.session_state.df = None

# File Upload
uploaded_file = st.file_uploader("📁 Upload your CSV file", type=["csv"])

if uploaded_file:
    st.session_state.df = pd.read_csv(uploaded_file)
    df = st.session_state.df

    # Data Profile
    st.markdown("### 📋 Dataset Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Rows",          f"{df.shape[0]:,}")
    col2.metric("Columns",       df.shape[1])
    col3.metric("Missing Values",f"{df.isnull().sum().sum():,}")
    col4.metric("Duplicates",    df.duplicated().sum())

    with st.expander("🔍 Preview Data & Column Info", expanded=False):
        st.dataframe(df.head(10), use_container_width=True)
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("**Column Types**")
            st.dataframe(df.dtypes.reset_index().rename(columns={"index":"Column", 0:"Type"}))
        with col_b:
            st.markdown("**Missing Values**")
            missing = df.isnull().sum().reset_index()
            missing.columns = ["Column", "Missing"]
            missing["Pct"] = (missing["Missing"] / len(df) * 100).round(1).astype(str) + "%"
            st.dataframe(missing)

    st.markdown("---")

    # Chat Interface

    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")

    if api_key:
        llm = ChatGroq(api_key=api_key, model_name=model, temperature=0)

        st.markdown("### 💬 Chat with Your Data")

        # Display conversation history
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f'<div class="chat-user">🧑 <b>You:</b> {msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-ai">🤖 <b>AI Analyst:</b></div>', unsafe_allow_html=True)
                
                # Show result
                if msg.get("result") is not None:
                    formatted = format_result(msg["result"])
                    if isinstance(formatted, (pd.DataFrame, pd.Series)):
                        st.dataframe(formatted, use_container_width=True)
                    else:
                        st.success(f"**Result:** {formatted}")

                # Show chart
                if msg.get("fig"):
                    st.plotly_chart(msg["fig"], use_container_width=True)

                # Show code expander
                if msg.get("code"):
                    with st.expander("🔎 View Generated Code"):
                        st.code(msg["code"], language="python")

        # Input
        question = st.chat_input("Ask anything about your data...")

        if question:
            # Add user message
            st.session_state.messages.append({"role": "user", "content": question})

            with st.spinner("🤖 Analyzing your data..."):
                result, code, error, st.session_state.chat_history = run_pipeline(
                    question, df, llm, st.session_state.chat_history
                )

                fig = None
                if result is not None and error is None:
                    fig, _ = generate_chart(result, question, llm)

            # Add AI message
            st.session_state.messages.append({
                "role":   "assistant",
                "result": result,
                "code":   code,
                "fig":    fig,
                "error":  error
            })

            st.rerun()

    else:
        st.warning("⚠️ Enter your Groq API key in the sidebar to start chatting.")

elif not uploaded_file:
    st.info("👆 Upload a CSV file to get started.")bar to start chatting.")

elif not uploaded_file:
    st.info("👆 Upload a CSV file to get started.")
