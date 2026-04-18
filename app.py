import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="NL2SQL", page_icon="📊", layout="wide")

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

        :root {
            --bg: #0b1220;
            --surface: rgba(15, 23, 42, 0.9);
            --surface-strong: #111b2e;
            --text: #e5ecf5;
            --muted: #94a3b8;
            --border: #263247;
            --brand: #14b8a6;
            --brand-soft: #0f2f36;
        }

        html, body, [class*="css"] {
            font-family: 'Sora', sans-serif;
            color: var(--text);
        }

        .stApp {
            background:
                radial-gradient(760px 320px at 10% -5%, #12303a 0%, transparent 60%),
                radial-gradient(900px 420px at 90% 0%, #14293f 0%, transparent 64%),
                var(--bg);
        }

        section[data-testid="stSidebar"] {
            background: #0f172a;
            border-right: 1px solid var(--border);
        }

        section[data-testid="stSidebar"] * {
            color: #d5dfec;
        }

        .shell {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 1rem;
            box-shadow: 0 18px 38px rgba(2, 6, 23, 0.45);
            margin-top: 0.35rem;
        }

        .topbar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            margin-bottom: 0.8rem;
            padding-bottom: 0.8rem;
            border-bottom: 1px solid var(--border);
        }

        .brand {
            display: inline-flex;
            align-items: center;
            gap: 0.55rem;
            font-size: 2rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            color: #f1f5f9;
            margin: 0;
        }

        .brand-badge {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 38px;
            height: 38px;
            border-radius: 10px;
            background: linear-gradient(135deg, #14b8a6, #2563eb);
            color: #ffffff;
            font-weight: 800;
            font-size: 1.05rem;
        }

        .tagline {
            margin: 0.3rem 0 0 0;
            color: var(--muted);
            font-size: 1.03rem;
            line-height: 1.5;
            max-width: 840px;
        }

        .panel {
            background: var(--surface-strong);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 1rem;
        }

        .panel-title {
            margin: 0 0 0.3rem 0;
            font-size: 1.02rem;
            font-weight: 700;
            color: #dce7f5;
        }

        .helper {
            margin: 0;
            color: var(--muted);
            font-size: 0.92rem;
        }

        .kpi-row {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.55rem;
            margin-top: 0.85rem;
        }

        .kpi {
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 0.65rem 0.75rem;
            background: #0f1a2f;
        }

        .kpi b {
            display: block;
            font-size: 0.78rem;
            color: #8ea3be;
            margin-bottom: 0.2rem;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }

        .kpi span {
            font-size: 1rem;
            font-weight: 700;
            color: #e6edf7;
        }

        @media (max-width: 900px) {
            .kpi-row {
                grid-template-columns: 1fr;
            }
            .brand {
                font-size: 1.7rem;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="shell">
        <div class="topbar">
            <div>
                <h1 class="brand"><span class="brand-badge">N</span>NL2SQL</h1>
                <p class="tagline">Turn business questions into SQL reports with one click. Built for clear answers, not technical complexity.</p>
            </div>
        </div>
        <div class="kpi-row">
            <div class="kpi"><b>Workflow</b><span>Question -> SQL -> Report</span></div>
            <div class="kpi"><b>Mode</b><span>Read-only safety checks enabled</span></div>
            <div class="kpi"><b>Output</b><span>Table + downloadable CSV</span></div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


API_URL = "http://127.0.0.1:8000/ask"

with st.sidebar:
    st.markdown("### Query Assistant")
    st.write("1. Ask a business question")
    st.write("2. Generate your report")
    st.write("3. Download or refine the result")
    st.markdown("---")
    st.markdown("### Starter Prompts")
    if st.button("Top 10 customers by total spend", use_container_width=True):
        st.session_state["question_input"] = "Show top 10 customers by total spending."
    if st.button("Invoices per month", use_container_width=True):
        st.session_state["question_input"] = "How many invoices were created per month?"
    if st.button("Best selling artists", use_container_width=True):
        st.session_state["question_input"] = "List the 5 best-selling artists."
    if st.button("Most expensive tracks", use_container_width=True):
        st.session_state["question_input"] = "Which tracks have the highest unit price?"

st.markdown('<div class="panel">', unsafe_allow_html=True)
st.markdown('<p class="panel-title">Ask your question</p>', unsafe_allow_html=True)
st.markdown('<p class="helper">Use natural language. Include timeframe, filters, and ranking details for better results.</p>', unsafe_allow_html=True)

question = st.text_area(
    "Ask a question about your data",
    value=st.session_state.get("question_input", ""),
    key="question_input",
    height=140,
    label_visibility="collapsed",
    placeholder="Example: Show monthly revenue for 2024, highest month first.",
)

run_report = st.button("Generate Report", type="primary", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

if run_report:
    if question:
        with st.spinner("Translating to SQL and fetching data..."):
            try:
                response = requests.post(API_URL, json={"question": question}, timeout=60)
                
                # Show useful backend errors (400/500) instead of a generic connection error.
                if response.status_code >= 400:
                    error_detail = response.text
                    try:
                        error_payload = response.json()
                        if isinstance(error_payload, dict) and "detail" in error_payload:
                            error_detail = error_payload["detail"]
                    except ValueError:
                        pass

                    st.error(f"API error ({response.status_code}): {error_detail}")
                    st.stop()

                result = response.json()
                
                st.markdown('<div class="panel">', unsafe_allow_html=True)
                st.subheader("Generated SQL")
                st.code(result.get("sql", "No SQL generated"), language="sql")
                st.markdown('</div>', unsafe_allow_html=True)
                
                if "error" in result:
                    st.error(f"Database Error: {result['error']}")
                else:
                    st.markdown('<div class="panel">', unsafe_allow_html=True)
                    st.subheader("Results")
                    df = pd.DataFrame(result.get("data", []))
                    st.caption(f"Rows returned: {len(df)}")
                    st.dataframe(df, use_container_width=True)
                    csv_data = df.to_csv(index=False)
                    st.download_button(
                        "Download results as CSV",
                        data=csv_data,
                        file_name="nl2sql_report.csv",
                        mime="text/csv",
                        use_container_width=True,
                    )
                    st.markdown('</div>', unsafe_allow_html=True)
                    
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to FastAPI at http://127.0.0.1:8000. Start it with: uvicorn main:app --reload")
            except requests.exceptions.Timeout:
                st.error("The API request timed out. Please try again.")
            except Exception as e:
                st.error(f"Unexpected client error: {e}")
    else:
        st.warning("Please enter a question before generating a report.")