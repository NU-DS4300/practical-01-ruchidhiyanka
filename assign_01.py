import json
from indexer.trees.avl_tree import AVLTreeIndex
from indexer.trees.bst_index import BinarySearchTreeIndex
from indexer.util.timer import timer
from indexer.abstract_index import AbstractIndex
from indexer.trees.trie_index import TrieIndex

import os

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
                            index.insert(word, file_name)

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




# A simple demo of how the @timer decoration can be used
@timer
def loopy_loop():
    total = sum((x for x in range(0, 1000000)))


import random
import string


def generate_dataset(indexed_terms, n):
    """
    Generates search datasets with Components A, B, C, and D.

    :param indexed_terms: Set of words currently indexed
    :param n_values: List of values for n (must be multiple of 4, >= 4000)
    :return: List of search datasets
    """
    # Random sample of n indexed words
    component_a = random.sample(indexed_terms, n)

    # Form (n/4) 2-3 word phrases from Component A
    component_b = []
    for i in range(n/4):
        component_b.append(' '.join(random.sample(component_a, random.choice([2, 3]))))

    # Generate n random strings
    component_c = []
    for i in range(n):
        str = ''.join(random.choices(string.printable, k = random.randint(1, 10)))
        component_c.append(str)

    # (n/4) 2-3 word phrases from Component C
    component_d = []
    for i in range(n/4):
        component_d.append(' '.join(random.sample(component_c, random.choice([2, 3]))))

    # Combine and shuffle dataset
    dataset = component_a + component_b + component_c + component_d
    random.shuffle(dataset)

    return dataset


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
    #
    # # quick demo of how to use the timing decorator included
    # # in indexer.util
    # loopy_loop()


    # #avl
    # print('avl')
    # avl_index = AVLTreeIndex()
    # index_files(data_directory, avl_index)
    #
    # # As a gut check, we are printing the keys that were added to the
    # # index in order.
    # print(avl_index.get_keys_in_order())
    #
    # # quick demo of how
    # # to use the timing decorator included
    # # in indexer.util
    # loopy_loop()

    #trie
    trie_index = TrieIndex()
    index_files(data_directory, trie_index)

    # As a gut check, we are printing the keys that were added to the
    # index in order.
    indexed_terms = trie_index.get_keys_in_order()

    # quick demo of how
    # to use the timing decorator included
    # in indexer.util
    loopy_loop()

    dataset_1 = generate_dataset(indexed_terms, 4444)
    dataset_2 = generate_dataset(indexed_terms, 4444)
    dataset_3 = generate_dataset(indexed_terms, 4444)
    dataset_4 = generate_dataset(indexed_terms, 4444)
    dataset_5 = generate_dataset(indexed_terms, 4444)
    dataset_6 = generate_dataset(indexed_terms, 4444)
    dataset_7 = generate_dataset(indexed_terms, 4444)
    dataset_8 = generate_dataset(indexed_terms, 4444)

if __name__ == "__main__":
    main()
