# file_indexer.py

#!/usr/bin/env python3
import os
import json
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

WATCH_DIR = "/root"
INDEX_FILE = "/root/file_index.json"

class FileIndexer(FileSystemEventHandler):
    def __init__(self):
        self.index = self.load_index()
        self.build_initial_index()

    def load_index(self):
        try:
            with open(INDEX_FILE, "r") as f:
                return json.load(f)
        except:
            return {}

    def save_index(self):
        with open(INDEX_FILE, "w") as f:
            json.dump(self.index, f)

    def build_initial_index(self):
        for root, _, files in os.walk(WATCH_DIR):
            for file in files:
                self.index_file(os.path.join(root, file))

    def index_file(self, file_path):
        try:
            with open(file_path, "r") as f:
                content = f.read()

            rel_path = os.path.relpath(file_path, WATCH_DIR)
            self.index[rel_path] = {
                "path": file_path,
                "size": os.path.getsize(file_path),
                "modified": os.path.getmtime(file_path),
                "content": content[:1000]  # Store first 1000 chars to save memory
            }
            self.save_index()
        except Exception as e:
            print(f"Error indexing {file_path}: {e}")

    def on_modified(self, event):
        if not event.is_directory:
            self.index_file(event.src_path)

    def on_created(self, event):
        if not event.is_directory:
            self.index_file(event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            rel_path = os.path.relpath(event.src_path, WATCH_DIR)
            if rel_path in self.index:
                del self.index[rel_path]
                self.save_index()

def main():
    event_handler = FileIndexer()
    observer = Observer()
    observer.schedule(event_handler, WATCH_DIR, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
