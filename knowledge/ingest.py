import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


from database import supabase

from knowledge.documents import documents

from knowledge.embeddings import create_embedding


# ============================================================
# INGEST DOCUMENTS
# ============================================================

def ingest_documents():

    print(
        "\nStarting dental knowledge ingestion...\n"
    )


    for index, document in enumerate(
        documents,
        start=1
    ):

        print(
            f"[{index}/{len(documents)}] "
            f"{document['title']}"
        )


        # ----------------------------------------------------
        # CREATE EMBEDDING
        # ----------------------------------------------------

        embedding = create_embedding(
            document["content"]
        )


        # ----------------------------------------------------
        # PREPARE DATABASE RECORD
        # ----------------------------------------------------

        record = {

            "title":
                document["title"],

            "source":
                document["source"],

            "content":
                document["content"],

            "metadata": {

                "type":
                    "dental_knowledge",

                "title":
                    document["title"]
            },

            "embedding":
                embedding
        }


        # ----------------------------------------------------
        # INSERT
        # ----------------------------------------------------

        response = (

            supabase

            .table(
                "knowledge_documents"
            )

            .insert(record)

            .execute()
        )


        if response.data:

            print(
                "   ✓ inserted"
            )

        else:

            print(
                "   ✗ insertion failed"
            )


    print(
        "\nKnowledge ingestion completed.\n"
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    ingest_documents()