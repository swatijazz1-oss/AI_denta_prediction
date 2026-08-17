import os

from dotenv import load_dotenv
from google import genai
from google.genai import types


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

EMBEDDING_MODEL = os.getenv(
    "GEMINI_EMBEDDING_MODEL",
    "gemini-embedding-001"
)

EMBEDDING_DIMENSIONS = 768


if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is missing from .env"
    )


client = genai.Client(
    api_key=API_KEY
)


# ============================================================
# CREATE EMBEDDING
# ============================================================

def create_embedding(text: str):

    response = client.models.embed_content(

        model=EMBEDDING_MODEL,

        contents=text,

        config=types.EmbedContentConfig(
            output_dimensionality=EMBEDDING_DIMENSIONS
        )
    )

    embedding = response.embeddings[0].values

    # --------------------------------------------------------
    # SAFETY CHECK
    # --------------------------------------------------------

    if len(embedding) != EMBEDDING_DIMENSIONS:

        raise RuntimeError(
            f"Embedding dimension mismatch: "
            f"expected {EMBEDDING_DIMENSIONS}, "
            f"received {len(embedding)}"
        )

    return embedding