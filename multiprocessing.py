import multiprocessing
import os
import time
from collections import defaultdict

def search_keywords_in_file(file_path, keywords, queue):
    result = defaultdict(list)
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            for keyword in keywords:
                if keyword in content:
                    result[keyword].append(file_path)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    
    queue.put(result)

def multiprocess_search(files, keywords):
    result_dict = defaultdict(list)
    queue = multiprocessing.Queue()
    processes = []

    for file_path in files:
        process = multiprocessing.Process(target=search_keywords_in_file, args=(file_path, keywords, queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    while not queue.empty():
        result = queue.get()
        for keyword, paths in result.items():
            result_dict[keyword].extend(paths)

    return result_dict

if __name__ == "__main__":
    keywords = ["example", "test", "keyword"]
    directory = "./texts"  # Specify the directory where your text files are located
    files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.txt')]
    
    start_time = time.time()
    results = multiprocess_search(files, keywords)
    end_time = time.time()

    for keyword, paths in results.items():
        print(f"Keyword '{keyword}' found in: {paths}")
    
    print(f"Multiprocessing search took {end_time - start_time:.2f} seconds")
