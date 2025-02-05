import json
from indexer.trees.avl_tree import AVLTreeIndex
from indexer.trees.bst_index import BinarySearchTreeIndex
from indexer.util.timer import timer
from indexer.abstract_index import AbstractIndex
from indexer.trees.trie_index import TrieIndex
from indexer.maps.hash_map import HashMapIndex
import random
import string
import os
import pickle
import csv
import argparse


DATASET_PICKLE_FILE = "datasets.pkl"
TIMING_CSV_FILE = "timing_data/timing_data.csv"
SEARCH_RESULTS_DIR = "search_results/"

os.makedirs("timing_data", exist_ok=True)
os.makedirs(SEARCH_RESULTS_DIR, exist_ok=True)

def save_datasets(datasets, filename=DATASET_PICKLE_FILE):
    with open(filename, "wb") as f:
        pickle.dump(datasets, f)

def load_datasets(filename=DATASET_PICKLE_FILE):
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            return pickle.load(f)
    return None
def index_files(path: str, index: AbstractIndex) -> None:
    # path should contain the location of the news articles you want to parse
    if path is not None:
        print(f"path = {path}")

    for folder in os.listdir(path):
        folder_path = os.path.join(path, folder)
        if os.path.isdir(folder_path):
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                # skip over hidden, non-json file in folder called ".DS_Store"
                if os.path.isfile(file_path) and ".DS_Store" not in file_path:
                    with open(file_path, 'r') as f:
                        #print(file_path)
                        contents = json.load(f)

                        words = contents["preprocessed_text"]
                        for word in words:
                            index.insert(word, file_name)

                        title = contents["title"].split(" ")
                        for word in title:
                            word_clean = word.strip(string.punctuation)
                            word_clean = word_clean.lower()
                            index.insert(word_clean, file_name)

                        url = contents["url"]
                        if 'http://' in url:
                            domain = url.partition("http://")[2].partition("/")[0]
                            index.insert(domain, file_name)
                        else:
                            domain = url.partition("https://")[2].partition("/")[0]
                            index.insert(domain, file_name)

                        author = contents["author"].split(" ")[-1]
                        if author.isspace() or author == "" or author is None:
                            pass
                        else:
                            author_clean = author.strip(string.punctuation)
                            index.insert(author_clean, file_name)


def generate_dataset(indexed_terms, n):
    # Random sample of n indexed words
    component_a = random.sample(indexed_terms, n)

    # Form (n/4) 2-3 word phrases from Component A
    component_b = []
    for i in range(n//4):
        component_b.append(' '.join(random.sample(component_a, random.choice([2, 3]))))

    # Generate n random strings
    component_c = []
    for i in range(n):
        str = ''.join(random.choices(string.printable, k = random.randint(1, 10)))
        component_c.append(str)

    # (n/4) 2-3 word phrases from Component C
    component_d = []
    for i in range(n//4):
        component_d.append(' '.join(random.sample(component_c, random.choice([2, 3]))))

    # Combine and shuffle dataset
    dataset = component_a + component_b + component_c + component_d
    random.shuffle(dataset)

    return dataset
@timer
def search_dataset(term, index_type):
    return index_type.search(term)

timed_results = {}
def experiment_runs(data_structures, datasets, n_ls, COMPUTE_PROC_TYPE,PRIMARY_MEMORY_SIZE):
    csv_rows = []
    search_times = []
    run_id = 1

    # loop through each dataset (x8), each data structure (x4) for 5 iterations each (x5) = 160 rows
    for id, dataset in enumerate(datasets):
        search_terms = random.sample(dataset, 4)
        for index_name, index in data_structures.items():
            for i in range(5):
                total_time = 0
                doc_results = set()
                for term in search_terms:
                    result, time_ns = search_dataset(term, index)
                    total_time += time_ns
                    doc_results.update(result)
                search_times.append(total_time)

                csv_rows.append([
                    run_id, COMPUTE_PROC_TYPE, PRIMARY_MEMORY_SIZE, index_name, search_terms,
                    len(doc_results), len(search_terms), n_ls[id], total_time])
                run_id += 1

    
    return csv_rows

def write_csv(data, filename=TIMING_CSV_FILE):
    file_exists = os.path.exists(filename)

    with open(filename, mode='a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow([
                "run_id", "compute_proc_type", "primary_memory_size", "index_type", "term",
                "num_docs_indexed", "num_tokens_indexed", "search_set_base_size", "search_time"
            ])
        writer.writerows(data)

def main():
    # Parse command-line arguments
    # parser = argparse.ArgumentParser(description="Index files and run search experiments.")
    # parser.add_argument("-d", "--dataset", required=True, help="Path to the dataset directory")
    # args = parser.parse_args()
    # change to command line
    #data_directory = args.dataset
    data_directory = "/Users/priyankaadhikari/Documents/ds4300/practical-01-ruchidhiyanka/USFinancialNewsArticles-preprocessed"

    # index data into all structures
    bst_index = BinarySearchTreeIndex()
    index_files(data_directory, bst_index)
    print("BST done indexing")
    avl_index = AVLTreeIndex()
    index_files(data_directory, avl_index)
    print("AVL done indexing")
    trie_index = TrieIndex()
    index_files(data_directory, trie_index)
    print("Trie done indexing")
    hash_map_index = HashMapIndex()
    index_files(data_directory, hash_map_index)
    print("Hashmap done indexing")

    # load datasets
    datasets = load_datasets()
    n_ls = [4444, 4804, 5224, 5600, 4008, 4488, 4004, 4808]
    indexed_terms = bst_index.get_keys_in_order()
    if datasets is None:
        datasets = [generate_dataset(indexed_terms, size) for size in n_ls]
        save_datasets(datasets)
    data_structures = {'BST': bst_index, 'AVL': avl_index,
                       'Trie': trie_index, 'Hash Map': hash_map_index}
    print("Datasets loaded")
    specified_search_terms = ['Northeastern', 'Beanpot', 'Husky']
    specified_search_terms_documents = dict()
    for structure in data_structures:
        for term in specified_search_terms:
            docs = data_structures[structure].search(term)
            specified_search_terms_documents[structure] = docs
    print(specified_search_terms_documents)

    csv_data = experiment_runs(data_structures, datasets, n_ls, 'Apple M3', '16 GB')
    write_csv(csv_data)

if __name__ == "__main__":
    main()
