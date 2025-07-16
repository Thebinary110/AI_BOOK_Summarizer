import chromadb

class VersionManager:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="./chromadb_store")
        self.collection = self.client.get_or_create_collection("chapters")

    def add_version(self, chapter, content, author):
        import uuid, datetime
        self.collection.add(
            documents=[content],
            metadatas=[{"chapter": chapter, "author": author, "timestamp": str(datetime.datetime.now())}],
            ids=[str(uuid.uuid4())],
        )

    def show_all_versions(self):
        results = self.collection.get()
        versions = []
        for doc, meta in zip(results['documents'], results['metadatas']):
            versions.append({
                "chapter": meta.get("chapter", ""),
                "author": meta.get("author", ""),
                "timestamp": meta.get("timestamp", ""),
                "content": doc
            })
        return versions
