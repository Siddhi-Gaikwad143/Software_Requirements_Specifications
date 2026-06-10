import streamlit as st
import json
import os
from dotenv import load_dotenv
import pdfplumber
import io

load_dotenv()

# ── Page Config ───────────────────────────────────────────────
st.set_page_config(
    page_title="Advanced AI SRS Generator",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1F4E79, #2E75B6);
        color: white; padding: 1.5rem 2rem;
        border-radius: 12px; margin-bottom: 1.5rem;
    }
    .section-card {
        background: #f8fafc; border-left: 4px solid #2E75B6;
        padding: 1rem 1.2rem; border-radius: 6px; margin-bottom: 1rem;
    }
    .metric-box {
        background: white; border: 1px solid #e2e8f0;
        border-radius: 8px; padding: 1rem; text-align: center;
    }
    .stButton > button {
        background: linear-gradient(135deg, #2E75B6, #1F4E79);
        color: white; border: none; border-radius: 8px;
        font-weight: bold; font-size: 1rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1 style="margin:0; font-size:1.8rem;">📋 Advanced AI SRS Generator</h1>
    <p style="margin:0.3rem 0 0; opacity:0.85;">
        Upload a PDF <b>or</b> describe your project → AI generates a full SRS with 6 embedded diagrams
    </p>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Project Settings")
    project_name = st.text_input("Project Name *", placeholder="e.g. Hospital Management System")
    project_desc = st.text_area("Project Description (optional)",
                                placeholder="Brief description of the project goals...",
                                height=80)
    st.markdown("---")
    st.markdown("**📊 Diagrams Included:**")
    st.markdown("""
    - 🥧 Requirements Distribution Pie  
    - 🎭 Use Case Diagram  
    - 🏗️ System Architecture (3-tier)  
    - 🔄 Data Flow Diagram (Level 0)  
    - 📊 NFR Category Bar Chart  
    - 🚶 User Activity Flow  
    """)
    st.markdown("---")
    st.caption("Powered by Groq (LLaMA 3.3) + Python-docx")

# ── Input Section ─────────────────────────────────────────────
st.subheader("📥 Step 1 — Provide Project Information")

input_tab1, input_tab2 = st.tabs(["📄 Upload PDF", "✍️ Type / Paste Requirements"])

raw_text = ""

with input_tab1:
    uploaded_file = st.file_uploader("Upload project document (PDF)", type=["pdf"])
    if uploaded_file:
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    raw_text += t + "\n"
        if raw_text:
            st.success(f"✅ Extracted {len(raw_text)} characters from {uploaded_file.name}")
            with st.expander("Preview extracted text"):
                st.text(raw_text[:1500] + ("..." if len(raw_text) > 1500 else ""))
        else:
            st.error("❌ Could not extract text — PDF may be scanned/image-based.")

with input_tab2:
    manual_text = st.text_area(
        "Paste your project requirements, features, or description here:",
        height=250,
        placeholder="""Example:
Project: Online Shopping Platform

Features:
1. User registration and login with email/password
2. Product catalog with search and filter
3. Shopping cart and checkout process
4. Payment gateway integration (credit card, UPI)
5. Order tracking and history
6. Admin panel for inventory management

Performance: Page load under 2 seconds, support 5000 concurrent users
Security: SSL encryption, PCI-DSS compliance for payments
Mobile: Responsive design for iOS and Android browsers
Availability: 99.9% uptime SLA"""
    )
    if manual_text.strip():
        raw_text = manual_text
        st.success(f"✅ {len(manual_text)} characters ready for processing")

# ── AI Classification ─────────────────────────────────────────
def classify_with_groq(text: str) -> dict:
    from groq import Groq
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    prompt = f"""You are a senior software requirements analyst.
Analyze the following project description and extract ALL requirements.
Classify each requirement as Functional or Non-Functional.

IMPORTANT: Return ONLY valid JSON. No explanation. No markdown. No backticks.

Format:
{{
  "functional": [
    {{"id": "FR-001", "title": "Short title (max 6 words)", "description": "Detailed requirement description"}}
  ],
  "non_functional": [
    {{"id": "NFR-001", "category": "Performance|Security|Usability|Reliability|Scalability|Maintainability|Availability|Compliance", "title": "Short title", "description": "Detailed requirement description"}}
  ]
}}

Project text:
\"\"\"{text[:4000]}\"\"\"
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=4096,
        temperature=0.1
    )
    result = response.choices[0].message.content.strip()
    # Clean markdown fences
    if "```" in result:
        result = result.split("```")[1]
        if result.startswith("json"):
            result = result[4:]
    return json.loads(result.strip())


# ── Generate Button ───────────────────────────────────────────
st.markdown("---")
st.subheader("📤 Step 2 — Generate SRS")

if not project_name:
    st.warning("⚠️ Enter a **Project Name** in the sidebar first.")
elif not raw_text.strip():
    st.info("👆 Upload a PDF or type your requirements above.")
elif not os.getenv("GROQ_API_KEY"):
    st.error("❌ GROQ_API_KEY missing in .env file")
else:
    if st.button("🚀 Generate Advanced SRS with Diagrams", use_container_width=True):

        progress = st.progress(0, text="Starting...")

        # Step 1 — Classify
        progress.progress(20, text="🤖 AI classifying requirements...")
        try:
            requirements = classify_with_groq(raw_text)
        except Exception as e:
            st.error(f"AI Error: {e}")
            st.stop()

        functional     = requirements.get("functional", [])
        non_functional = requirements.get("non_functional", [])

        progress.progress(50, text="📊 Generating diagrams...")

        # Show metrics
        st.markdown("### 📊 Classification Results")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("✅ Functional", len(functional))
        c2.metric("⚡ Non-Functional", len(non_functional))
        c3.metric("📋 Total", len(functional) + len(non_functional))
        c4.metric("🗂️ NFR Categories",
                  len(set(r.get("category","General") for r in non_functional)))

        # Preview requirements
        tab1, tab2 = st.tabs(["✅ Functional Requirements", "⚡ Non-Functional Requirements"])
        with tab1:
            for req in functional:
                with st.expander(f"**{req['id']}** — {req['title']}"):
                    st.write(req["description"])
        with tab2:
            for req in non_functional:
                with st.expander(f"**{req['id']}** [{req.get('category','General')}] — {req['title']}"):
                    st.write(req["description"])

        # Step 2 — Generate SRS
        progress.progress(75, text="📝 Building SRS document with diagrams...")
        try:
            from advanced_srs_generator import generate_advanced_srs
            srs_bytes = generate_advanced_srs(project_name, requirements, project_desc)
        except Exception as e:
            st.error(f"Document generation error: {e}")
            import traceback; st.code(traceback.format_exc())
            st.stop()

        progress.progress(100, text="✅ Done!")

        st.success("🎉 Advanced SRS Document with 6 Diagrams is ready!")
        st.download_button(
            label="⬇️ Download Advanced SRS (.docx)",
            data=srs_bytes,
            file_name=f"Advanced_SRS_{project_name.replace(' ', '_')}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True
        )

        st.markdown("### 📋 Document Contains:")
        st.markdown("""
        | Section | Content |
        |---|---|
        | Cover Page | Project title, date, total requirements |
        | Table of Contents | All 10 sections listed |
        | Section 1 | Introduction, scope, conventions |
        | Section 2 | Summary table + **Pie Chart** |
        | Section 3 | **Use Case Diagram** |
        | Section 4 | **3-Tier Architecture Diagram** |
        | Section 5 | **Data Flow Diagram (Level 0)** |
        | Section 6 | Functional requirements table |
        | Section 7 | NFR tables grouped by category + **Bar Chart** |
        | Section 8 | **User Activity Flow Diagram** |
        | Section 9 | Assumptions & Constraints |
        | Section 10 | Glossary |
        """)