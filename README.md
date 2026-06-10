📋 AI-Powered Software Requirements Specification (SRS) Generator
🚀 Overview

This project is an AI-powered SRS Generator that converts raw project descriptions or PDF documents into a structured Software Requirements Specification (SRS) document.

The system uses Streamlit as the execution interface to provide an interactive web application where users can upload or enter requirements and generate a complete SRS document with diagrams.

It is designed for:

Software Engineering students
Final-year academic projects
Requirement analysis automation
Documentation generation using AI
⚙️ Execution Platform (Streamlit)
🌐 Streamlit is used as the main execution layer
Provides a web-based interactive UI
Handles:
PDF upload
Text input
AI processing trigger
Display of results
Download of final SRS document
▶️ Run Application
streamlit run app.py

Then open:

http://localhost:8501
✨ Features
🤖 AI-Based Requirement Analysis
Uses Groq LLaMA 3 model
Automatically extracts requirements from text/PDF
Classifies into:
Functional Requirements (FR)
Non-Functional Requirements (NFR)
📊 Generated Outputs

The system automatically generates:

📄 Complete SRS Document (.docx)
🧠 AI-classified requirements
🥧 Requirements distribution pie chart
🎭 Use Case Diagram
🏗️ System Architecture (3-tier)
🔄 Data Flow Diagram (DFD Level 0)
📊 Non-Functional Requirements (NFR) chart
🚶 User Activity Flow diagram
📊 Venn Diagram (FR vs NFR relationship)
🧠 Tech Stack
Python 3.x
Streamlit (UI + Execution Layer)
Groq API (LLaMA 3 - AI model)
python-docx (SRS document generation)
matplotlib (charts & diagrams)
matplotlib-venn (Venn diagram)
pdfplumber (PDF extraction)
numpy
dotenv (environment variables)
📁 Project Structure
SRS_Generator/
│
├── app.py                      # Streamlit execution file
├── advanced_srs_generator.py   # SRS document generator logic
├── diagram_generator.py        # Diagram generation module
├── extractor.py               # PDF text extraction module
├── requirements.txt            # Dependencies
├── README.md                   # Project documentation
├── .gitignore                  # Ignored files
└── venv/ (not uploaded)
⚙️ Installation Guide
1️⃣ Clone Repository
git clone https://github.com/USERNAME/Software_Requirements_Specifications.git
cd Software_Requirements_Specifications
2️⃣ Create Virtual Environment (Optional)
python -m venv venv

Activate:

Windows

venv\Scripts\activate

Mac/Linux

source venv/bin/activate
3️⃣ Install Dependencies
pip install -r requirements.txt
🔑 Environment Setup

Create a .env file in the root folder:

GROQ_API_KEY=your_api_key_here
▶️ How to Run
streamlit run app.py
📥 Output

After execution, the system generates:

📄 Professional SRS document (.docx)
📊 Requirement classification summary
🧠 AI-generated structured requirements
📈 Embedded diagrams inside document
⬇️ Downloadable final report
🔄 Workflow
User Input (PDF/Text)
        ↓
Streamlit UI (Execution Layer)
        ↓
Groq AI (Requirement Extraction)
        ↓
FR / NFR Classification
        ↓
Diagram Generation Module
        ↓
SRS Document Builder (DOCX)
        ↓
Final Download Output
📊 System Capabilities

✔ AI-powered requirement extraction
✔ Automatic classification (FR & NFR)
✔ Professional SRS document generation
✔ Multiple system diagrams
✔ Interactive Streamlit UI
✔ PDF + text input support

🚀 Future Enhancements
🌐 Cloud deployment (Streamlit Cloud / Render)
📄 Export as PDF format
🧠 Improved AI accuracy (prompt optimization)
🔐 User login system
🗄️ Database integration
📊 Advanced analytics dashboard
👨‍💻 Author
