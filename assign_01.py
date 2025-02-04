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
            for file_name in os.listdir(path):
                file_path = os.path.join(path, file_name)
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
def experiment_run(index_type, datasets):
    i = 1
    for dataset in datasets:
        search_terms = random.sample(dataset, 4)
        for idx, word in enumerate(dataset):
            index_type.insert(word, idx)

        results = []
        for term in search_terms:
            total_time = 0
            for test in range(6):
                result, time_ns = search_dataset(term, index_type)
                total_time += time_ns
            results.append((total_time/5))
        timed_results[f'dataset_{i}'] = results
        i += 1
    return timed_results

def write_csv(data, filename=TIMING_CSV_FILE):
    file_exists = os.path.exists(filename)

    with open(filename, mode='a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow([
                "run_id", "compute_proc_type", "primary_memory_size", "index_type",
                "num_docs_indexed", "num_tokens_indexed", "search_set_base_size", "search_time"
            ])
        writer.writerows(data)

def main():
    # change to command line
    data_directory = "/Users/nidhibendre/Documents/ds4300/practical-01-ruchidhiyanka/data/P01-verify-dataset"


    # bst_index = BinarySearchTreeIndex()
    # index_files(data_directory, bst_index)
    #print(bst_index.get_keys_in_order())

    #avl
    # print('avl')
    # avl_index = AVLTreeIndex()
    # index_files(data_directory, avl_index)
    #print(avl_index.get_keys_in_order())

     # trie
    # trie_index = TrieIndex()
    # index_files(data_directory, trie_index)
    #indexed_terms = bst_index.get_keys_in_order()
    # print(trie_index.get_keys_in_order())


    # # hashmap
    # hash_map_index = HashMapIndex()
    # index_files(data_directory, hash_map_index)
    # print(hash_map_index.print_hashmap())

    # datasets = load_datasets()
    # n_ls = [4444, 4804, 5224, 5600, 4008, 4488, 4004, 4808]
    # if datasets is None:
    #  datasets = [generate_dataset(indexed_terms, size) for size in n_ls]
    #  save_datasets(datasets)
    # data_structures = {'BST': BinarySearchTreeIndex(), 'AVL': AVLTreeIndex()}
    #
    #
    # csv_data, search_results = experiment_run(data_structures, datasets)
    # write_csv(csv_data)

if __name__ == "__main__":
    main()
