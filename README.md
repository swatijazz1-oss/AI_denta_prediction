# 🦷 AI Dental Analyzer

An AI-assisted dental image analysis application that combines **multimodal AI, Retrieval-Augmented Generation (RAG), dental knowledge retrieval, web fallback, structured patient information, and analytics** to provide a preliminary educational assessment of dental images.

> ⚠️ **Medical Disclaimer:** This application is intended for educational and preliminary assessment purposes only. It does not provide a definitive medical diagnosis and must not replace examination, diagnosis, or treatment by a qualified dental professional.

---

## 🚀 Overview

AI Dental Analyzer allows users to upload or capture a dental photograph, provide structured symptom information, select affected teeth using the **FDI two-digit tooth numbering system**, and receive an AI-assisted preliminary assessment.

The system combines:

- 🖼️ Dental image analysis
- 📋 Structured patient information
- 🦷 Interactive FDI tooth selection
- 🤖 Gemini multimodal AI
- 🔎 Retrieval-Augmented Generation (RAG)
- 🧠 Vector-based dental knowledge retrieval
- 🌐 Web fallback for additional supporting information
- 💾 Supabase database storage
- 📊 Analytics dashboard
- 🔐 Google authentication
- 🌐 Streamlit deployment

---

## ✨ Features

### 🖼️ Dental Image Input

Users can:

- Upload a JPG/JPEG/PNG dental image
- Capture a dental image using the device camera
- Preview the selected image before analysis

The application validates the image format before sending it for analysis.

---

### 📋 Patient Information

The application collects structured information including:

- Age
- Pain level
- Pain type
- Pain duration
- Cold sensitivity
- Hot sensitivity
- Pain while chewing
- Gum bleeding
- Gum swelling
- Persistent bad breath
- Tooth mobility
- Recent dental treatment
- Additional patient description

This structured information is combined with the image to improve the context available to the AI model.

---

### 🦷 Interactive Tooth Selection

The application provides an interactive dental chart based on the:

**FDI two-digit tooth numbering system**

Users can select one or multiple affected teeth.

Example:

```text
11 12 13 14 15 16 17 18
21 22 23 24 25 26 27 28

31 32 33 34 35 36 37 38
41 42 43 44 45 46 47 48
Selected teeth are highlighted in the interface.

🤖 Multimodal AI Analysis

The application uses Google's Gemini multimodal model to analyze:

The uploaded dental photograph
Patient symptoms
Selected teeth
Retrieved dental knowledge
Web fallback information when required

The AI response is structured into:

1. Visible observations

Findings that can reasonably be observed from the photograph.

2. Reported symptoms

A summary of the information provided by the user.

3. Possible explanations

Potential explanations are presented cautiously using language such as:

"may be consistent with"
"could be associated with"
"one possibility is"
4. Image limitations

Explains what cannot reliably be determined from a photograph.

5. Preliminary concern level

The system categorizes the preliminary concern as:

Low
Moderate
High
6. Recommended next step

Provides a practical recommendation based on the available information.

7. Warning signs

Highlights symptoms that may require prompt professional evaluation.

🔎 Retrieval-Augmented Generation (RAG)

The application uses a local dental knowledge base together with vector similarity search.

The RAG pipeline works approximately as follows:
Patient information
        │
        ▼
Construct retrieval query
        │
        ▼
Generate embedding
        │
        ▼
Vector similarity search
        │
        ▼
Retrieve relevant dental knowledge
        │
        ▼
Apply similarity threshold
        │
        ▼
Add relevant knowledge to AI prompt
The application displays retrieval information such as:
Highest retrieval similarity
Configured threshold
Knowledge items retrieved
Example:
Highest retrieval similarity: 0.685
Configured threshold: 0.600
Knowledge items retrieved: 3
Dental Knowledge Base

The project contains a structured dental knowledge base under:

knowledge/

The knowledge pipeline includes:

knowledge/
├── __init__.py
├── documents.py
├── embeddings.py
└── ingest.py

The system generates embeddings for dental knowledge and stores/retrieves them through the configured vector database.

🌐 Web Fallback

RAG is not always guaranteed to return sufficiently relevant information.

The application therefore implements a fallback mechanism:

             ┌──────────────────────┐
             │ Patient information  │
             │ + image context      │
             └──────────┬───────────┘
                        │
                        ▼
                ┌───────────────┐
                │ Vector Search │
                └───────┬───────┘
                        │
              ┌─────────┴─────────┐
              │                   │
       Relevant results      Insufficient
              │                   │
              ▼                   ▼
        Use RAG context       Web fallback
                                  │
                                  ▼
                         Supporting information

If the highest RAG similarity is below the configured threshold, the application can perform a web search for relevant dental information.

The web results are then provided to Gemini as supporting context.

The application does not treat web information as a definitive diagnosis.

💾 Database

Supabase is used to store assessment information.

Stored information includes:

Age
Pain level
Pain type
Pain duration
Symptoms
Affected teeth
User description
Image filename
Image MIME type
AI analysis
Concern level
Assessment timestamp

The database functionality is implemented in:

database.py
📊 Analytics Dashboard

The project includes an analytics dashboard for reviewing assessment data.

The dashboard provides information such as:

Overview
Total assessments
Average pain level
Average age
Most common concern level
Concern Analysis
Low
Moderate
High
Pain Analysis
Pain type distribution
Pain level distribution
Symptom Analysis
Cold sensitivity
Hot sensitivity
Chewing pain
Gum bleeding
Gum swelling
Bad breath
Tooth mobility
Recent dental treatment
Demographic Analysis
Age distribution
Tooth Analysis
Most frequently selected teeth
Recent Assessments

A table of recently recorded assessments.

The analytics functionality is implemented in:

analytics.py

and exposed through:

pages/2_Analytics.py
🔐 Authentication

The application supports Google authentication using OAuth.

Authentication helps restrict application access and provides a more controlled deployment environment.

OAuth credentials and application secrets should never be committed to GitHub.

🏗️ Project Structure
AI_denta_prediction/
│
├── .streamlit/
│   └── secrets.toml          # Local secrets - NOT committed
│
├── knowledge/
│   ├── __init__.py
│   ├── documents.py
│   ├── embeddings.py
│   └── ingest.py
│
├── pages/
│   └── 2_Analytics.py
│
├── app.py                    # Main Streamlit application
├── analytics.py              # Analytics functionality
├── database.py               # Supabase database operations
├── rag.py                    # RAG retrieval
├── web_fallback.py           # Web retrieval fallback
│
├── test_analytics.py         # Analytics testing
├── test_embedding.py         # Embedding testing
├── test_rag.py               # RAG testing
│
├── requirements.txt
├── .gitignore
└── README.md
🔄 Application Architecture

The overall system can be represented as:

                         ┌──────────────────┐
                         │      User        │
                         └────────┬─────────┘
                                  │
                                  ▼
                    ┌─────────────────────────┐
                    │ Streamlit Frontend      │
                    │                         │
                    │ Image / Camera          │
                    │ Patient information     │
                    │ Tooth selection         │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │ Retrieval Query Builder │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │ Vector Database / RAG   │
                    └────────────┬────────────┘
                                 │
                         ┌───────┴────────┐
                         │                │
                    Relevant          Insufficient
                    knowledge          relevance
                         │                │
                         │                ▼
                         │       ┌────────────────┐
                         │       │ Web Fallback   │
                         │       └───────┬────────┘
                         │               │
                         └───────┬───────┘
                                 ▼
                    ┌─────────────────────────┐
                    │ Gemini Multimodal AI    │
                    │                         │
                    │ Image + symptoms +      │
                    │ retrieved knowledge     │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │ Preliminary Assessment  │
                    └────────────┬────────────┘
                                 │
                    ┌────────────┴────────────┐
                    ▼                         ▼
             Supabase Database          User Interface
                    │
                    ▼
             Analytics Dashboard
🛠️ Technology Stack
Technology	Purpose
Python	Core programming language
Streamlit	Web application frontend
Google Gemini	Multimodal AI analysis
RAG	Retrieval-Augmented Generation
Vector Search	Dental knowledge retrieval
Supabase	Database and data storage
Pandas	Analytics and data processing
BeautifulSoup	Web content extraction
Google OAuth	Authentication
Git/GitHub	Version control and source hosting
⚙️ Installation
1. Clone the repository
git clone https://github.com/swatijazz1-oss/AI_denta_prediction.git

Move into the project:

cd AI_denta_prediction
2. Create a virtual environment
Windows
python -m venv .venv

Activate it:

.venv\Scripts\activate
macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
3. Install dependencies
pip install -r requirements.txt
🔑 Environment Variables

Create a .env file locally.

Example:

GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=your_gemini_model


RAG_THRESHOLD=0.60


SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

Do not commit .env to GitHub.

The repository already ignores sensitive files through .gitignore.

▶️ Running the Application

Start the Streamlit application:

streamlit run app.py

The application will normally be available at:

http://localhost:8501
🧪 Testing

The project contains separate test scripts for major components.

Test embeddings
python test_embedding.py
Test RAG
python test_rag.py
Test analytics
python test_analytics.py
📈 Example Workflow

A typical user workflow is:

1. Open application
        ↓
2. Sign in
        ↓
3. Upload or capture dental image
        ↓
4. Enter patient symptoms
        ↓
5. Select affected teeth
        ↓
6. Click "Analyze Tooth"
        ↓
7. Retrieve dental knowledge
        ↓
8. Use web fallback if necessary
        ↓
9. Analyze image + context with Gemini
        ↓
10. Display preliminary assessment
        ↓
11. Save assessment
        ↓
12. View aggregated analytics
🔒 Security Considerations

Sensitive credentials should never be stored in the GitHub repository.

The following files are excluded from version control:

.env
.streamlit/secrets.toml
.venv/
.idea/
__pycache__/

For production deployment, secrets should be configured using the deployment platform's secret management system.

⚠️ Medical Safety

This project is an AI-assisted educational tool, not a replacement for professional dental care.

Important limitations include:

Dental photographs cannot reliably determine pulp vitality.
Photographs cannot reliably determine the depth of decay.
Radiographs may be required to evaluate roots and surrounding bone.
AI-generated explanations may be incorrect.
Web information may be incomplete or outdated.
Visual findings should not be interpreted as confirmed diagnoses.

Users should seek evaluation from a qualified dental professional for diagnosis and treatment.

Urgent professional/medical evaluation may be appropriate for symptoms such as:

Significant facial or oral swelling
Difficulty breathing
Difficulty swallowing
Severe or rapidly worsening pain
Fever or systemic illness
Other concerning symptoms
🚧 Current Limitations

The current system has several limitations:

Image-based assessment is limited by image quality.
A photograph cannot replace clinical examination.
RAG quality depends on the available knowledge base.
Web fallback information may vary in quality.
AI-generated results require professional verification.
The system does not independently establish a definitive diagnosis.
🔮 Future Improvements

Potential future improvements include:

Improved dental image classification
More comprehensive dental knowledge base
Better tooth-level localization
Dental X-ray analysis
Automatic concern-level extraction
More advanced analytics
User assessment history
Doctor/dentist review workflow
Improved authentication and role-based access
Better source citation and provenance
Automated model evaluation
More robust clinical validation
Mobile-friendly interface
👩‍💻 Project

AI Dental Analyzer

An AI-assisted dental image analysis and retrieval system built using Python, Streamlit, Gemini, RAG, Supabase, and web-based supporting information.

GitHub:

https://github.com/swatijazz1-oss/AI_denta_prediction

