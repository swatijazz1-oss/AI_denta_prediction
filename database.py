import os

from dotenv import load_dotenv
from supabase import create_client


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


SUPABASE_URL = os.getenv(
    "SUPABASE_URL"
)

SUPABASE_KEY = os.getenv(
    "SUPABASE_KEY"
)


# ============================================================
# VALIDATE CONFIGURATION
# ============================================================

if not SUPABASE_URL:

    raise ValueError(
        "SUPABASE_URL is missing from .env"
    )


if not SUPABASE_KEY:

    raise ValueError(
        "SUPABASE_KEY is missing from .env"
    )


# ============================================================
# CREATE CLIENT
# ============================================================

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


# ============================================================
# SAVE ASSESSMENT
# ============================================================

def save_assessment(
    assessment,
    image_filename,
    image_mime_type,
    ai_analysis,
    concern_level
):

    data = {

        "age":
            assessment.get("age"),

        "pain_level":
            assessment.get("pain_level"),

        "pain_type":
            assessment.get("pain_type"),

        "pain_duration":
            assessment.get("pain_duration"),

        "cold_sensitivity":
            assessment.get(
                "cold_sensitivity"
            ),

        "hot_sensitivity":
            assessment.get(
                "hot_sensitivity"
            ),

        "chewing_pain":
            assessment.get(
                "chewing_pain"
            ),

        "gum_bleeding":
            assessment.get(
                "gum_bleeding"
            ),

        "gum_swelling":
            assessment.get(
                "gum_swelling"
            ),

        "bad_breath":
            assessment.get(
                "bad_breath"
            ),

        "tooth_mobility":
            assessment.get(
                "tooth_mobility"
            ),

        "recent_dental_treatment":
            assessment.get(
                "recent_dental_treatment"
            ),

        "affected_teeth":
            assessment.get(
                "affected_teeth"
            ),

        "description":
            assessment.get(
                "description"
            ),

        "image_filename":
            image_filename,

        "image_mime_type":
            image_mime_type,

        "ai_analysis":
            ai_analysis,

        "concern_level":
            concern_level
    }


    response = (
        supabase
        .table("assessments")
        .insert(data)
        .execute()
    )


    return response
# ============================================================
# ANALYTICS FUNCTIONS
# ============================================================

def get_all_assessments():

    response = (
        supabase
        .table("assessments")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )

    return response.data


def get_assessment_count():

    response = (
        supabase
        .table("assessments")
        .select("id", count="exact")
        .execute()
    )

    return response.count or 0


def get_analytics_data():

    response = (
        supabase
        .table("assessments")
        .select(
            """
            id,
            created_at,
            age,
            pain_level,
            pain_type,
            pain_duration,
            cold_sensitivity,
            hot_sensitivity,
            chewing_pain,
            gum_bleeding,
            gum_swelling,
            bad_breath,
            tooth_mobility,
            recent_dental_treatment,
            affected_teeth,
            concern_level
            """
        )
        .order(
            "created_at",
            desc=True
        )
        .execute()
    )

    return response.data