import os
from collections import defaultdict

class LFUCache:
    def __init__(self, folder_path, max_cache_size=5):
        self.folder_path = folder_path
        self.max_cache_size = max_cache_size
        self.cache = {}  
        self.freq = defaultdict(int)  

    def _evict_if_needed(self):
        if len(self.cache) > self.max_cache_size:
            min_freq = min(self.freq.values())
            least_used_files = [file for file, count in self.freq.items() if count == min_freq]
            file_to_evict = least_used_files[0]
            print(f"Evicting '{file_to_evict}' from cache (frequency {min_freq})")
            self.cache.pop(file_to_evict)
            self.freq.pop(file_to_evict)

    def access_file(self, filename):
        file_path = os.path.join(self.folder_path, filename)

        if not os.path.exists(file_path):
            print(f"File '{filename}' does not exist in folder.")
            return None

        if filename in self.cache:
            print(f"Cache hit: '{filename}'")
        else:
            print(f"Cache miss: '{filename}' - loading into cache.")
            with open(file_path, 'r') as f:
                self.cache[filename] = f.read()
            self._evict_if_needed()

        self.freq[filename] += 1
        return self.cache[filename]

    def show_cache(self):
        print("\nCurrent Cache Status:")
        for filename, content in self.cache.items():
            print(f"  - {filename} (accessed {self.freq[filename]} times)")

    def list_least_used_files(self):
        if not self.freq:
            print("Cache is empty.")
            return

        min_freq = min(self.freq.values())
        least_used_files = [file for file, count in self.freq.items() if count == min_freq]

        print("\nLeast Frequently Used Files:")
        for file in least_used_files:
            print(f"  - {file} (accessed {self.freq[file]} times)")

if __name__ == "__main__":
    folder = "C:/local path"  
    lfu_cache = LFUCache(folder_path=folder, max_cache_size=3)

    while True:
        print("\nOptions: [access] filename | [show] cache | [least] used files | [exit]")
        command = input("Enter command: ").strip().lower()

        if command == 'exit':
            break
        elif command.startswith('access'):
            _, filename = command.split(maxsplit=1)
            content = lfu_cache.access_file(filename)
            if content:
                print(f"Content of '{filename}':\n{content[:100]}...")
        elif command == 'show':
            lfu_cache.show_cache()
        elif command == 'least':
            lfu_cache.list_least_used_files()
        else:
            print("Invalid command.")
