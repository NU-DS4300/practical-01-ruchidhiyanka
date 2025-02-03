import json
from indexer.trees.avl_tree import AVLTreeIndex
from indexer.trees.bst_index import BinarySearchTreeIndex
from indexer.util.timer import timer
from indexer.abstract_index import AbstractIndex
from indexer.trees.trie_index import TrieIndex
import random
import string
import os
from indexer.util.parser_utils import preprocess_text
import pickle

DATASET_PICKLE_FILE = "datasets.pkl"

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
                if os.path.isfile(file_path):
                    with open(file_path, 'r') as file:
                        # Process the file contents here
                        #file_name = "preproc-blogs_0000001.json"
                        contents = json.load(file)

                        words = contents["preprocessed_text"]
                        for word in words:
                            index.insert(word, file_name)

                        title = contents["title"].split(" ")
                        for word in title:
                            word_processed = preprocess_text(word)
                            index.insert(word_processed, file_name)

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
                            index.insert(author, file_name)

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

def main():
    # You'll need to change this to be the absolute path to the root folder
    # of the dataset
    data_directory = "/Users/ruchirabanerjee/practical-01-ruchidhiyanka/USFinancialNewsArticles-preprocessed"

    # Here, we are creating a sample binary search tree index object
    # and sending it to the index_files function
    # bst_index = BinarySearchTreeIndex()
    # index_files(data_directory, bst_index)
    #
    # # As a gut check, we are printing the keys that were added to the
    # # index in order.
    # print(bst_index.get_keys_in_order())

    # #avl
    # print('avl')
    # avl_index = AVLTreeIndex()
    # index_files(data_directory, avl_index)
    #
    # # As a gut check, we are printing the keys that were added to the
    # # index in order.
    # print(avl_index.get_keys_in_order())

    #trie
    trie_index = TrieIndex()
    index_files(data_directory, trie_index)

    # As a gut check, we are printing the keys that were added to the
    # index in order.
    indexed_terms = trie_index.get_keys_in_order()

    # Try to load datasets from pickle
    datasets = load_datasets()

    if datasets is None:
        datasets = [generate_dataset(indexed_terms, size) for size in [4444, 4804, 5224, 5600, 4008, 4488, 4004, 4808]]
        save_datasets(datasets)

    trie_index = TrieIndex()
    bst_index = BinarySearchTreeIndex()
    avl_index = AVLTreeIndex()
    data_structures = [trie_index, bst_index, avl_index]

    index_type_results = {}
    for index_type in data_structures:
        timed_results = experiment_run(index_type, datasets)
        index_type_results[index_type] = timed_results

    print(index_type_results)

if __name__ == "__main__":
    main()
