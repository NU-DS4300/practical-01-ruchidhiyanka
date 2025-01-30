import json
from indexer.trees.avl_tree import AVLTreeIndex
from indexer.trees.bst_index import BinarySearchTreeIndex
from indexer.util.timer import timer
from indexer.abstract_index import AbstractIndex
import os

def index_files(path: str, index: AbstractIndex) -> None:
    # path should contain the location of the news articles you want to parse
    if path is not None:
        print(f"path = {path}")

    # for folder in os.listdir(path):
    #     folder_path = os.path.join(path, folder)
    #     if os.path.isdir(folder_path):
    for file_name in os.listdir(path):
        file_path = os.path.join(path, file_name)
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
                domain = url.partition("www.")[2].partition(".com")[0]
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


def main():
    # You'll need to change this to be the absolute path to the root folder
    # of the dataset
    data_directory = "/Users/nidhibendre/Documents/ds4300/practical-01-ruchidhiyanka/USFinancialNewsArticles-preprocessed/February2018"

    # Here, we are creating a sample binary search tree index object
    # and sending it to the index_files function
    bst_index = BinarySearchTreeIndex()
    index_files(data_directory, bst_index)

    # As a gut check, we are printing the keys that were added to the
    # index in order.
    print(bst_index.get_keys_in_order())

    # quick demo of how to use the timing decorator included
    # in indexer.util
    loopy_loop()


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


if __name__ == "__main__":
    main()
