# versioning/chromadb_handler.py

import chromadb
import argparse

class VersionManager:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=".chromadb")
        self.collection = self.client.get_or_create_collection(name="book_versions")

    def add_version(self, chapter_id, content):
        self.collection.add(
            documents=[content],
            ids=[chapter_id]
        )

    def get_version(self, chapter_id):
        result = self.collection.get(ids=[chapter_id])
        return result['documents'][0] if result['documents'] else "No version found."

    def show_all_versions(self):
        results = self.collection.get()
        return list(zip(results['ids'], results['documents'])) if results['ids'] else []

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--action', choices=['show_all_versions', 'get_version', 'add_version'], required=True)
    parser.add_argument('--id', help='Chapter ID')
    parser.add_argument('--content', help='Chapter content (if adding)')
    args = parser.parse_args()

    vm = VersionManager()

    if args.action == "show_all_versions":
        all_versions = vm.show_all_versions()
        for idx, (cid, doc) in enumerate(all_versions):
            print(f"\n[{idx+1}] ID: {cid}\n{doc}\n{'-'*50}")
    elif args.action == "get_version":
        if args.id:
            print(vm.get_version(args.id))
        else:
            print("Please provide --id to retrieve a version.")
    elif args.action == "add_version":
        if args.id and args.content:
            vm.add_version(args.id, args.content)
            print(f"Version added for {args.id}")
        else:
            print("Please provide --id and --content to add a version.")
