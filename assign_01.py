import json
from indexer.trees.avl_tree import AVLTreeIndex
from indexer.trees.bst_index import BinarySearchTreeIndex
from indexer.maps.hash_map import HashMapIndex
from indexer.util.timer import timer
from indexer.abstract_index import AbstractIndex
import os
import string

def index_files(path: str, index: AbstractIndex) -> None:
    if path is not None:
        print(f"path = {path}")

    # for folder in os.listdir(path):
    # folder_path = os.path.join(path, folder)
    folder_path = path
    if os.path.isdir(folder_path):
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                with open(file_path, 'r') as file:
                    # Process the file contents here
                    contents = json.load(file)

                    words = contents["preprocessed_text"]
                    for word in words:
                        index.insert(word, file_name)

                    title = contents["title"].split(" ")
                    for word in title:
                        word_clean = word.strip(string.punctuation)
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




# A simple demo of how the @timer decoration can be used
@timer
def loopy_loop():
    total = sum((x for x in range(0, 1000000)))


def main():
    # You'll need to change this to be the absolute path to the root folder of the dataset
    data_directory = "/Users/priyankaadhikari/Documents/ds4300/practical-01-ruchidhiyanka/USFinancialNewsArticles-preprocessed/April2018"

    # Create a sample binary search tree index object and index the files
    # bst_index = BinarySearchTreeIndex()
    # index_files(data_directory, bst_index)
    #
    # # Print the keys that were added to the index in order
    # print(bst_index.get_keys_in_order())

    # Test the Hash Map Indexing & print the hash map contents
    hash_map_index = HashMapIndex()
    index_files(data_directory, hash_map_index)
    print(hash_map_index.print_hashmap())

    # quick demo of how to use the timing decorator included in indexer.util
    loopy_loop()


    # #avl
    # print('avl')
    # avl_index = AVLTreeIndex()
    # index_files(data_directory, avl_index)
    #
    # Print the keys that were added to the index in order
    # print(avl_index.get_keys_in_order())


if __name__ == "__main__":
    main()
