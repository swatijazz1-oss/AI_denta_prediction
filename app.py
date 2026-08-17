import os
import base64

import streamlit as st
from dotenv import load_dotenv
from google import genai

from database import save_assessment
from rag import retrieve_documents
from web_fallback import web_fallback, format_web_context


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Dental AI Analyzer",
    page_icon="🦷",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# GOOGLE LOGIN
# ============================================================

if not st.user.is_logged_in:

    st.title("🦷 Dental AI Analyzer")

    st.warning(
        "Please sign in with your Google account to use "
        "the Dental AI Analyzer."
    )

    st.write(
        "This application uses your Google account only "
        "for authentication."
    )

    st.button(
        "🔐 Sign in with Google",
        on_click=st.login
    )

    st.stop()


# ============================================================
# LOGGED-IN USER INFORMATION
# ============================================================

user_name = st.user.get(
    "name",
    "User"
)

user_email = st.user.get(
    "email",
    ""
)


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

MODEL_NAME = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.5-flash"
)

RAG_THRESHOLD = float(
    os.getenv(
        "RAG_THRESHOLD",
        "0.60"
    )
)


if not API_KEY:

    st.error(
        "GEMINI_API_KEY was not found in your .env file."
    )

    st.stop()


# ============================================================
# GEMINI CLIENT
# ============================================================

client = genai.Client(
    api_key=API_KEY
)


# ============================================================
# CUSTOM CSS
# ============================================================

# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Main application width */
    .main .block-container {
        max-width: 1200px;
        padding-top: 1.2rem;
        padding-bottom: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    /* Main title */
    .main-title {
        font-size: 2rem;
        font-weight: 750;
        letter-spacing: -0.5px;
        margin-bottom: 0.1rem;
    }

    /* Subtitle */
    .subtitle {
        font-size: 0.95rem;
        color: #6b7280;
        margin-bottom: 0.8rem;
    }

    /* Section headings */
    .section-title {
        font-size: 1.15rem;
        font-weight: 700;
        margin-top: 0.8rem;
        margin-bottom: 0.35rem;
    }

    /* Small helper text */
    .helper-text {
        color: #6b7280;
        font-size: 0.85rem;
        margin-bottom: 0.5rem;
    }

    /* Jaw labels */
    .jaw-label {
        text-align: center;
        font-weight: 700;
        font-size: 0.85rem;
        margin: 0.35rem 0;
        color: #374151;
    }

    /* Reduce spacing around Streamlit elements */
    div[data-testid="stVerticalBlock"] {
        gap: 0.55rem;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
    }

    /* Primary button */
    .stButton > button[kind="primary"] {
        min-height: 2.6rem;
        font-size: 1rem;
    }

    /* File uploader */
    div[data-testid="stFileUploader"] {
        margin-top: 0.2rem;
    }

    /* Images */
    img {
        border-radius: 10px;
    }

    /* Metrics */
    div[data-testid="stMetric"] {
        padding: 0.35rem 0.5rem;
    }

    /* Expanders */
    div[data-testid="stExpander"] {
        border-radius: 10px;
    }

    /* Alerts */
    div[data-testid="stAlert"] {
        border-radius: 10px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        padding-top: 1rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">'
    '🦷 Dental AI Analyzer'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-assisted preliminary dental image analysis'
    '</div>',
    unsafe_allow_html=True
)

st.warning(
    "⚠️ This application provides a preliminary "
    "AI-assisted analysis only. It does not provide "
    "a definitive diagnosis and does not replace "
    "examination by a qualified dental professional."
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    # --------------------------------------------------------
    # ACCOUNT
    # --------------------------------------------------------

    st.header("👤 Account")

    st.write(
        f"Welcome, **{user_name}**"
    )

    if user_email:

        st.caption(
            user_email
        )

    st.button(
        "🚪 Log out",
        on_click=st.logout
    )

    st.divider()

    # --------------------------------------------------------
    # ABOUT
    # --------------------------------------------------------

    st.header("About")

    st.write(
        "This project combines dental image analysis "
        "with structured symptom information, "
        "vector-based dental knowledge and web "
        "retrieval."
    )

    st.divider()

    # --------------------------------------------------------
    # CURRENT PIPELINE
    # --------------------------------------------------------

    st.subheader(
        "Current pipeline"
    )

    st.write(
        "🖼️ Dental image"
    )

    st.write(
        "📋 Patient information"
    )

    st.write(
        "🦷 Tooth selection"
    )

    st.write(
        "🔎 RAG vector search"
    )

    st.write(
        "🌐 Web fallback"
    )

    st.write(
        "🤖 Gemini multimodal AI"
    )

    st.write(
        "💾 Assessment database"
    )

    st.divider()

    st.caption(
        f"RAG similarity threshold: "
        f"{RAG_THRESHOLD:.2f}"
    )


## ============================================================
# 1. IMAGE UPLOAD
# ============================================================

st.markdown(
    '<div class="section-title">1. Dental Image</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="helper-text">'
    'Upload an existing dental image or take a new photo.'
    '</div>',
    unsafe_allow_html=True
)


# ------------------------------------------------------------
# IMAGE SOURCE SELECTION
# ------------------------------------------------------------

image_source = st.radio(
    "Choose image source",
    [
        "📁 Upload from gallery",
        "📷 Take a photo"
    ],
    horizontal=True,
    label_visibility="collapsed"
)


uploaded_file = None


# ------------------------------------------------------------
# GALLERY
# ------------------------------------------------------------

if image_source == "📁 Upload from gallery":

    uploaded_file = st.file_uploader(
        "Choose a dental image",
        type=[
            "jpg",
            "jpeg",
            "png"
        ],
        help=(
            "Use a clear, well-lit image where "
            "the affected tooth is visible."
        )
    )


# ------------------------------------------------------------
# CAMERA
# ------------------------------------------------------------

else:

    camera_file = st.camera_input(
        "Take a photo of the affected tooth"
    )

    if camera_file is not None:

        uploaded_file = camera_file


# ------------------------------------------------------------
# IMAGE PREVIEW
# ------------------------------------------------------------

if uploaded_file is not None:

    preview_col, info_col = st.columns(
        [1, 2],
        gap="medium"
    )

    with preview_col:

        st.image(
            uploaded_file,
            caption="Selected dental image",
            use_container_width=True
        )

    with info_col:

        st.success(
            "✓ Image ready for analysis"
        )

        st.caption(
            "For best results, use a close-up image "
            "with good lighting and minimal blur."
        )

else:

    st.info(
        "Select an image source above to continue."
    )
# ============================================================
# 2. PATIENT INFORMATION
# ============================================================

st.markdown(
    '<div class="section-title">2. Patient Information</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="helper-text">'
    'Provide symptoms to help the AI interpret the image.'
    '</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(
    2,
    gap="large"
)


# ============================================================
# LEFT COLUMN
# ============================================================

with col1:

    age = st.number_input(
        "Age",
        min_value=1,
        max_value=120,
        value=21,
        step=1
    )

    pain_level = st.slider(
        "Pain level",
        min_value=0,
        max_value=10,
        value=0
    )

    pain_type = st.selectbox(
        "Type of pain",
        [
            "None",
            "Sharp",
            "Dull",
            "Throbbing",
            "Constant",
            "Occasional",
            "Burning",
            "Pressure"
        ]
    )

    pain_duration = st.selectbox(
        "How long have you had the pain?",
        [
            "No pain",
            "Less than 1 day",
            "1–3 days",
            "4–7 days",
            "More than 1 week",
            "More than 1 month"
        ]
    )


# ============================================================
# RIGHT COLUMN
# ============================================================

with col2:

    cold_sensitivity = st.checkbox(
        "Sensitivity to cold"
    )

    hot_sensitivity = st.checkbox(
        "Sensitivity to hot"
    )

    chewing_pain = st.checkbox(
        "Pain while chewing"
    )

    gum_bleeding = st.checkbox(
        "Gum bleeding"
    )

    gum_swelling = st.checkbox(
        "Gum swelling"
    )

    bad_breath = st.checkbox(
        "Persistent bad breath"
    )

    tooth_mobility = st.checkbox(
        "Tooth feels loose"
    )

    recent_dental_treatment = st.checkbox(
        "Recent dental treatment"
    )


# ============================================================
# 3. TOOTH CHART
# ============================================================

st.markdown(
    '<div class="section-title">'
    '3. Select Affected Tooth / Teeth'
    '</div>',
    unsafe_allow_html=True
)

st.caption(
    "Click one or more teeth that you believe "
    "are causing the problem."
)


# ============================================================
# SESSION STATE
# ============================================================

if "selected_teeth" not in st.session_state:

    st.session_state.selected_teeth = []


def toggle_tooth(tooth_number):

    if tooth_number in st.session_state.selected_teeth:

        st.session_state.selected_teeth.remove(
            tooth_number
        )

    else:

        st.session_state.selected_teeth.append(
            tooth_number
        )


# ============================================================
# FDI TOOTH NUMBERING
# ============================================================

upper_left = [
    "18",
    "17",
    "16",
    "15",
    "14",
    "13",
    "12",
    "11"
]

upper_right = [
    "21",
    "22",
    "23",
    "24",
    "25",
    "26",
    "27",
    "28"
]

lower_left = [
    "48",
    "47",
    "46",
    "45",
    "44",
    "43",
    "42",
    "41"
]

lower_right = [
    "31",
    "32",
    "33",
    "34",
    "35",
    "36",
    "37",
    "38"
]


# ============================================================
# UPPER JAW
# ============================================================

st.markdown(
    '<div class="jaw-label">'
    'UPPER JAW'
    '</div>',
    unsafe_allow_html=True
)

upper_teeth = (
    upper_left +
    upper_right
)

upper_cols = st.columns(
    16
)


for i, tooth_number in enumerate(
    upper_teeth
):

    with upper_cols[i]:

        st.caption(
            tooth_number
        )

        if tooth_number in st.session_state.selected_teeth:

            button_label = "🔴"

        else:

            button_label = "🦷"

        st.button(
            button_label,
            key=f"upper_tooth_{tooth_number}",
            help=f"Select tooth {tooth_number}",
            on_click=toggle_tooth,
            args=(tooth_number,)
        )


st.divider()


# ============================================================
# LOWER JAW
# ============================================================

st.markdown(
    '<div class="jaw-label">'
    'LOWER JAW'
    '</div>',
    unsafe_allow_html=True
)

lower_teeth = (
    lower_left +
    lower_right
)

lower_cols = st.columns(
    16
)


for i, tooth_number in enumerate(
    lower_teeth
):

    with lower_cols[i]:

        st.caption(
            tooth_number
        )

        if tooth_number in st.session_state.selected_teeth:

            button_label = "🔴"

        else:

            button_label = "🦷"

        st.button(
            button_label,
            key=f"lower_tooth_{tooth_number}",
            help=f"Select tooth {tooth_number}",
            on_click=toggle_tooth,
            args=(tooth_number,)
        )


# ============================================================
# SELECTED TEETH
# ============================================================

selected_teeth = (
    st.session_state.selected_teeth
)


if selected_teeth:

    selected_text = ", ".join(
        selected_teeth
    )

    st.success(
        f"🦷 Selected tooth/teeth: "
        f"{selected_text}"
    )

else:

    st.info(
        "No specific tooth selected."
    )


# ============================================================
# 4. ADDITIONAL INFORMATION
# ============================================================

st.markdown(
    '<div class="section-title">'
    '4. Additional Information'
    '</div>',
    unsafe_allow_html=True
)

description = st.text_area(
    "Describe anything else you have noticed",
    placeholder=(
        "Example: I noticed a dark spot on this tooth "
        "and it hurts when I drink something cold. "
        "The pain started three days ago."
    ),
    height=120
)


# ============================================================
# STRUCTURED ASSESSMENT
# ============================================================

assessment = {

    "age": age,

    "pain_level": pain_level,

    "pain_type": pain_type,

    "pain_duration": pain_duration,

    "cold_sensitivity": cold_sensitivity,

    "hot_sensitivity": hot_sensitivity,

    "chewing_pain": chewing_pain,

    "gum_bleeding": gum_bleeding,

    "gum_swelling": gum_swelling,

    "bad_breath": bad_breath,

    "tooth_mobility": tooth_mobility,

    "recent_dental_treatment":
        recent_dental_treatment,

    "affected_teeth":
        selected_teeth,

    "description":
        description
}


# ============================================================
# 5. AI ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">'
    '5. AI Analysis'
    '</div>',
    unsafe_allow_html=True
)

st.caption(
    f"AI model: {MODEL_NAME}"
)


if st.button(
    "🔍 Analyze Tooth",
    type="primary",
    use_container_width=True
):

    # ========================================================
    # VALIDATE IMAGE
    # ========================================================

    if uploaded_file is None:

        st.error(
            "Please upload an image or take a photo first."
        )

        st.stop()


    # ========================================================
    # GET IMAGE
    # ========================================================

    image_bytes = uploaded_file.getvalue()

    mime_type = uploaded_file.type


    # ========================================================
    # VALIDATE IMAGE TYPE
    # ========================================================

    allowed_types = [
        "image/jpeg",
        "image/png"
    ]

    if mime_type not in allowed_types:

        st.error(
            "Please upload a JPG, JPEG or PNG image."
        )

        st.stop()


    # ========================================================
    # SELECTED TEETH
    # ========================================================

    if selected_teeth:

        affected_teeth_text = ", ".join(
            selected_teeth
        )

    else:

        affected_teeth_text = (
            "No specific tooth selected"
        )


    # ========================================================
    # BUILD RAG QUERY
    # ========================================================

    rag_query = f"""
Dental image assessment context:

Age: {age}

Pain level: {pain_level}/10

Pain type: {pain_type}

Pain duration: {pain_duration}

Cold sensitivity: {cold_sensitivity}

Hot sensitivity: {hot_sensitivity}

Pain while chewing: {chewing_pain}

Gum bleeding: {gum_bleeding}

Gum swelling: {gum_swelling}

Bad breath: {bad_breath}

Tooth mobility: {tooth_mobility}

Recent dental treatment: {recent_dental_treatment}

Affected teeth: {affected_teeth_text}

User description:
{description}
"""


    # ========================================================
    # RAG RETRIEVAL
    # ========================================================

    retrieved_documents = []

    highest_similarity = 0.0

    rag_used = False

    rag_error = None


    with st.spinner(
        "🔎 Searching dental knowledge base..."
    ):

        try:

            retrieved_documents = retrieve_documents(
                rag_query
            )

        except Exception as e:

            rag_error = str(e)

            retrieved_documents = []


    # ========================================================
    # NORMALIZE RAG RESULTS
    # ========================================================

    normalized_documents = []


    for document in retrieved_documents:

        if isinstance(document, dict):

            similarity = document.get(
                "similarity",
                document.get(
                    "score",
                    0
                )
            )

            try:

                similarity = float(
                    similarity
                )

            except (
                TypeError,
                ValueError
            ):

                similarity = 0.0


            normalized_documents.append(
                {
                    "content": document.get(
                        "content",
                        document.get(
                            "text",
                            ""
                        )
                    ),

                    "title": document.get(
                        "title",
                        document.get(
                            "disease",
                            "Dental knowledge"
                        )
                    ),

                    "similarity": similarity
                }
            )


        else:

            normalized_documents.append(
                {
                    "content": str(document),
                    "title": "Dental knowledge",
                    "similarity": 0.0
                }
            )


    # ========================================================
    # HIGHEST SIMILARITY
    # ========================================================

    if normalized_documents:

        highest_similarity = max(
            document["similarity"]
            for document in normalized_documents
        )


    # ========================================================
    # DECIDE WHETHER RAG IS SUFFICIENT
    # ========================================================

    if (
        normalized_documents
        and
        highest_similarity >= RAG_THRESHOLD
    ):

        rag_used = True

        normalized_documents = [
            document
            for document in normalized_documents
            if document["similarity"]
            >= RAG_THRESHOLD
        ]

    else:

        rag_used = False

        normalized_documents = []


    # ========================================================
    # RETRIEVAL INFORMATION
    # ========================================================

    st.markdown(
        "### 🔎 Retrieval information"
    )


    if rag_error:

        st.warning(
            "RAG retrieval could not be completed. "
            "The system will attempt the web fallback."
        )


    if rag_used:

        st.success(
            "Relevant dental knowledge was retrieved "
            "from the vector database."
        )

        st.write(
            f"Highest retrieval similarity: "
            f"{highest_similarity:.3f}"
        )

        st.write(
            f"Configured threshold: "
            f"{RAG_THRESHOLD:.3f}"
        )

        st.write(
            f"Knowledge items retrieved: "
            f"{len(normalized_documents)}"
        )

    else:

        st.warning(
            "The vector database did not provide "
            "sufficiently relevant information."
        )

        st.write(
            f"Highest retrieval similarity: "
            f"{highest_similarity:.3f}"
        )

        st.write(
            f"Configured threshold: "
            f"{RAG_THRESHOLD:.3f}"
        )


    # ========================================================
    # BUILD RAG KNOWLEDGE CONTEXT
    # ========================================================

    knowledge_context = ""


    if rag_used:

        context_parts = []


        for index, document in enumerate(
            normalized_documents,
            start=1
        ):

            context_parts.append(
                f"""
KNOWLEDGE SOURCE {index}

Title:
{document["title"]}

Similarity:
{document["similarity"]:.3f}

Content:
{document["content"]}
"""
            )


        knowledge_context = "\n".join(
            context_parts
        )


    # ========================================================
    # WEB FALLBACK
    # ========================================================

    web_used = False

    web_results = []

    web_context = ""


    if not rag_used:

        st.markdown(
            "### 🌐 Web fallback"
        )

        web_query = f"""
dental symptoms and possible causes for:

pain type: {pain_type}

pain duration: {pain_duration}

cold sensitivity: {cold_sensitivity}

hot sensitivity: {hot_sensitivity}

chewing pain: {chewing_pain}

gum bleeding: {gum_bleeding}

gum swelling: {gum_swelling}

bad breath: {bad_breath}

tooth mobility: {tooth_mobility}

user description:
{description}
"""


        with st.spinner(
            "🌐 Searching the web for relevant dental information..."
        ):

            try:

                web_data = web_fallback(
                    web_query,
                    max_results=3
                )

                web_results = web_data.get(
                    "results",
                    []
                )

                web_used = web_data.get(
                    "used",
                    False
                )

            except Exception as e:

                st.warning(
                    "Web fallback could not be completed."
                )

                st.exception(e)

                web_used = False


        if web_used:

            st.success(
                f"Web fallback retrieved "
                f"{len(web_results)} source(s)."
            )

            web_context = format_web_context(
                web_results
            )


            # ------------------------------------------------
            # WEB SOURCES
            # ------------------------------------------------

            with st.expander(
                "🌐 View web sources"
            ):

                for index, result in enumerate(
                    web_results,
                    start=1
                ):

                    st.markdown(
                        f"**{index}. "
                        f"{result.get('title', 'Source')}**"
                    )

                    st.write(
                        result.get(
                            "snippet",
                            ""
                        )
                    )

                    source_url = result.get(
                        "url",
                        ""
                    )

                    if source_url:

                        st.markdown(
                            f"[Open source]({source_url})"
                        )

                    st.divider()


        else:

            st.warning(
                "No useful web sources were retrieved. "
                "The AI will continue using the user-provided "
                "information and image only."
            )


    # ========================================================
    # FINAL AI PROMPT
    # ========================================================

    prompt = f"""
You are an AI assistant providing a preliminary
dental image analysis.

Analyze the uploaded dental photograph together
with the symptoms and information provided by
the user.

IMPORTANT SAFETY RULES:

1. Do NOT provide a definitive medical diagnosis.

2. Do NOT say that the patient definitely has
   a disease.

3. Only describe visual findings that are reasonably
   supported by the uploaded image.

4. Do not invent findings that cannot be seen.

5. If the image is blurry, poorly lit, obstructed,
   too distant, or otherwise insufficient, explicitly
   state that image quality limits the analysis.

6. Do not exaggerate the severity.

7. A photograph alone cannot reliably determine
   many dental conditions.

8. Clearly separate visual observations from
   reported symptoms.

9. The selected tooth numbers use the FDI
   two-digit tooth numbering system.

10. Do not infer visual findings solely from
    the selected tooth number.

11. This is a preliminary educational assessment
    and not a professional dental diagnosis.

12. Retrieved knowledge is supporting information.
    It must NOT be used to claim that a condition
    is definitely present.

13. Web information may be incomplete or outdated.
    Use it cautiously.

PATIENT INFORMATION
===================

Age:
{age}

Pain level:
{pain_level}/10

Pain type:
{pain_type}

Pain duration:
{pain_duration}

Sensitivity to cold:
{cold_sensitivity}

Sensitivity to hot:
{hot_sensitivity}

Pain while chewing:
{chewing_pain}

Gum bleeding:
{gum_bleeding}

Gum swelling:
{gum_swelling}

Persistent bad breath:
{bad_breath}

Tooth feels loose:
{tooth_mobility}

Recent dental treatment:
{recent_dental_treatment}

Affected tooth/teeth:
{affected_teeth_text}

Additional description:
{description}


RETRIEVED DENTAL KNOWLEDGE
==========================

{
    knowledge_context
    if knowledge_context
    else
    "No sufficiently relevant vector-database knowledge was retrieved."
}


WEB FALLBACK INFORMATION
========================

{
    web_context
    if web_context
    else
    "No web fallback information was retrieved."
}


RESPONSE FORMAT
===============

### 1. Visible observations

Describe only things that can reasonably be observed
from the photograph.

### 2. Reported symptoms

Briefly summarize what the user reported.

### 3. Possible explanations

Mention a small number of reasonable possibilities.

Use phrases such as:

"may be consistent with"

"could be associated with"

"one possibility is"

Do not present possibilities as confirmed diagnoses.

### 4. What the image cannot determine

Explain the limitations of photograph-based analysis.

### 5. Preliminary concern level

Choose exactly one:

Low
Moderate
High

Then briefly explain the reasoning.

This is NOT a medical diagnosis.

### 6. Recommended next step

Give a practical recommendation based only on
the available information.

### 7. Warning signs

Mention important symptoms that would warrant
prompt professional evaluation.

Keep the answer concise and avoid unnecessary
alarmism.

If external information was used, do not invent
citations. Simply state that web-based supporting
information was consulted.
"""


    # ========================================================
    # GEMINI MULTIMODAL ANALYSIS
    # ========================================================

    with st.spinner(
        "🔬 Analyzing the image and retrieved information..."
    ):

        try:

            image_base64 = base64.b64encode(
                image_bytes
            ).decode(
                "utf-8"
            )


            interaction = client.interactions.create(

                model=MODEL_NAME,

                input=[
                    {
                        "type": "image",
                        "data": image_base64,
                        "mime_type": mime_type
                    },

                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            )


            # =================================================
            # RESPONSE
            # =================================================

            result_text = (
                interaction.output_text
            )


            if result_text:

                st.success(
                    "✅ Analysis complete"
                )

                st.divider()

                st.subheader(
                    "Preliminary AI Assessment"
                )

                st.markdown(
                    result_text
                )


                # =================================================
                # ASSESSMENT INFORMATION
                # =================================================

                st.divider()

                st.subheader(
                    "📊 Assessment Information"
                )

                source_col1, source_col2, source_col3 = (
                    st.columns(3)
                )


                with source_col1:

                    if rag_used:

                        st.metric(
                            "Knowledge source",
                            "RAG"
                        )

                    elif web_used:

                        st.metric(
                            "Knowledge source",
                            "Web fallback"
                        )

                    else:

                        st.metric(
                            "Knowledge source",
                            "Image + symptoms"
                        )


                with source_col2:

                    st.metric(
                        "RAG similarity",
                        f"{highest_similarity:.3f}"
                    )


                with source_col3:

                    st.metric(
                        "Affected teeth",
                        len(selected_teeth)
                    )


                # =================================================
                # SAVE ASSESSMENT
                # =================================================

                try:

                    save_assessment(

                        assessment=assessment,

                        image_filename=(
                            uploaded_file.name
                            if uploaded_file.name
                            else "camera_capture.jpg"
                        ),

                        image_mime_type=mime_type,

                        ai_analysis=result_text,

                        concern_level=(
                            "Not extracted yet"
                        )
                    )

                    st.success(
                        "💾 Assessment saved successfully."
                    )

                except Exception as db_error:

                    st.warning(
                        "The AI analysis succeeded, "
                        "but the assessment could not "
                        "be saved."
                    )

                    st.exception(
                        db_error
                    )


            else:

                st.warning(
                    "The AI returned an empty response."
                )


        except Exception as e:

            st.error(
                "Something went wrong while contacting "
                "the Gemini API."
            )

            st.exception(
                e
            )