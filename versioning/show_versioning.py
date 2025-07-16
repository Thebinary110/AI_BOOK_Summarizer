# versioning/show_versions.py
from chromadb import PersistentClient

client = PersistentClient(path=".chromadb")
collection = client.get_collection("book_versions")

results = collection.get()
for i, doc in enumerate(results["documents"]):
    print(f"\n📘 Version {i+1}:")
    print(doc)
