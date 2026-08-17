from knowledge.embeddings import create_embedding


text = """
Dental caries is a disease involving damage
to tooth structure.
"""


embedding = create_embedding(text)


print()
print("Embedding successfully created!")
print()
print("Dimension:", len(embedding))
print()
print("First 5 values:")
print(embedding[:5])