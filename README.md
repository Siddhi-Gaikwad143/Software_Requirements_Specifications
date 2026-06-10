
# 📋 AI-Powered Software Requirements Specification (SRS) Generator
---
## 🚀 Overview

This project is an **AI-powered SRS Generator** that converts raw project descriptions or PDF documents into a structured **Software Requirements Specification (SRS)** document.
It uses **Streamlit** as the interactive web interface to allow users to upload or enter requirements and generate a complete SRS document along with diagrams.

### 🎯 Use Cases
- Software Engineering students  
- Final-year academic projects  
- Requirement analysis automation  
- AI-based documentation generation  

---

## ⚙️ Execution Platform

The application runs on **Streamlit**, providing a simple web-based interface.

### Features of UI:
- 📄 PDF upload support  
- ✍️ Text input for requirements  
- 🤖 AI processing trigger  
- 📊 Output visualization  
- ⬇️ Download final SRS document  

---

## ▶️ How to Run
```bash
streamlit run app.py
````

Then open:
```
http://localhost:8501
```

---
## ✨ Features

### 🤖 AI-Based Requirement Analysis
* Uses **Groq LLaMA 3 model**
* Extracts requirements from text/PDF
* Classifies into:
  * Functional Requirements (FR)
  * Non-Functional Requirements (NFR)

---

## 📊 Generated Outputs
The system automatically generates:
* 📄 Complete SRS Document (.docx)
* 🧠 AI-classified requirements
* 🥧 Requirements distribution pie chart
* 🎭 Use Case Diagram
* 🏗️ System Architecture (3-tier)
* 🔄 Data Flow Diagram (DFD Level 0)
* 📊 NFR analysis chart
* 🚶 User activity flow diagram
* 📈 Venn diagram (FR vs NFR)

---

## 🧠 Tech Stack
* Python 3.x
* Streamlit (UI layer)
* Groq API (LLaMA 3 model)
* python-docx (document generation)
* matplotlib (charts & diagrams)
* matplotlib-venn (Venn diagrams)
* pdfplumber (PDF extraction)
* numpy
* python-dotenv

---

## 📁 Project Structure
```
SRS_Generator/
│
├── app.py                      # Streamlit entry point
├── advanced_srs_generator.py  # SRS generation logic
├── diagram_generator.py        # Diagram creation module
├── extractor.py                # PDF extraction module
├── requirements.txt            # Dependencies
├── README.md                   # Project documentation
├── .gitignore                  # Ignored files
└── venv/ (not included)
```

---
## ⚙️ Installation Guide
### 1️⃣ Clone Repository

```bash
git clone https://github.com/USERNAME/Software_Requirements_Specifications.git
cd Software_Requirements_Specifications
```

### 2️⃣ Create Virtual Environment (Optional)
```bash
python -m venv venv
```

Activate it:
**Windows**
```bash
venv\Scripts\activate
```

**Mac/Linux**
```bash
source venv/bin/activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

---
## 🔑 Environment Setup
Create a `.env` file in the root directory:

```
GROQ_API_KEY=your_api_key_here
```

---

## 📥 Output
After execution, the system generates:
* 📄 Professional SRS document (.docx)
* 🧠 Structured AI requirements
* 📊 Requirement analysis summary
* 📈 Embedded system diagrams
* ⬇️ Downloadable final report

---

## 🔄 Workflow
```
User Input (PDF/Text)
        ↓
Streamlit UI
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
```

---

## 📊 System Capabilities
✔ AI-powered requirement extraction
✔ Automatic FR & NFR classification
✔ Professional SRS document generation
✔ Multiple system diagrams
✔ Interactive Streamlit UI
✔ PDF + text input support

---

## 🚀 Future Enhancements
* 🌐 Cloud deployment (Streamlit Cloud / AWS)
* 📊 Advanced AI diagrams (UML auto-generation)
* 🧾 Multi-language SRS support
* 🔐 User authentication system
* 📱 Mobile-friendly UI upgrade


