from rag import retrieve_documents


# ============================================================
# TEST QUERY
# ============================================================

query = """
My tooth hurts when I drink something cold.
There is a dark area on the tooth and it hurts
when I chew.
"""


print()
print("========================================")
print("        DENTAL RAG RETRIEVAL TEST")
print("========================================")
print()


# ============================================================
# RETRIEVE
# ============================================================

results = retrieve_documents(
    query=query,
    match_threshold=0.30,
    match_count=5
)


# ============================================================
# DISPLAY
# ============================================================

if not results:

    print(
        "No relevant documents were retrieved."
    )

else:

    print(
        f"Retrieved {len(results)} documents:"
    )

    print()

    for index, result in enumerate(
        results,
        start=1
    ):

        print(
            "----------------------------------------"
        )

        print(
            f"Result #{index}"
        )

        print(
            f"Title: {result['title']}"
        )

        print(
            f"Source: {result['source']}"
        )

        print(
            f"Similarity: "
            f"{result['similarity']:.4f}"
        )

        print()

        print(
            result["content"]
        )

        print()


print(
    "========================================"
)
print("              TEST COMPLETE")
print("========================================")