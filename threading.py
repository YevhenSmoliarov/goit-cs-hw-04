import threading
import os
import time
from collections import defaultdict

def search_keywords_in_file(file_path, keywords, result_dict, lock):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            for keyword in keywords:
                if keyword in content:
                    with lock:
                        result_dict[keyword].append(file_path)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

def threaded_search(files, keywords):
    result_dict = defaultdict(list)
    lock = threading.Lock()
    threads = []
    
    for file_path in files:
        thread = threading.Thread(target=search_keywords_in_file, args=(file_path, keywords, result_dict, lock))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return result_dict

if __name__ == "__main__":
    keywords = ["example", "test", "keyword"]
    directory = "./texts"  # Specify the directory where your text files are located
    files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.txt')]
    
    start_time = time.time()
    results = threaded_search(files, keywords)
    end_time = time.time()

    for keyword, paths in results.items():
        print(f"Keyword '{keyword}' found in: {paths}")
    
    print(f"Threaded search took {end_time - start_time:.2f} seconds")
