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

    # a sample json news article.  assume this is in a file named sample.json
    # sample_filename = "sample.json"
    # sample_json = """
    #     {
    #         "author": " ",
    #         "title": "Some article",
    #         "text": "here is the text of a sample news article",
    #         "preprocessed_text": ["here", "text", "sample", "news", "article"]
    #     }
    # """

    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                # Process the file contents here
                contents = file.read()

    # extract the preprocessed_text words and add them to the index with
    # sample.json as the file name
    the_json = json.loads(sample_json)
    words = the_json["preprocessed_text"]

    for word in words:
        index.insert(word, sample_filename)

    for word in the_json["title"].split(" "):
        index.insert(word, sample_filename)

    author = the_json["author"].split(" ")[-1]
    if author.isspace() or author == "" or author is None:
        pass
    else:
        index.insert(author, sample_filename)


# A simple demo of how the @timer decoration can be used
@timer
def loopy_loop():
    total = sum((x for x in range(0, 1000000)))


def main():
    # You'll need to change this to be the absolute path to the root folder
    # of the dataset
    data_directory = "/Users/nidhibendre/Documents/ds4300/practical-01-ruchidhiyanka/USFinancialNewsArticles-preprocessed/April2018"

    # # Here, we are creating a sample binary search tree index object
    # # and sending it to the index_files function
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


    #avl
    print('avl')
    avl_index = AVLTreeIndex()
    index_files(data_directory, avl_index)

    # As a gut check, we are printing the keys that were added to the
    # index in order.
    #print(avl_index.get_keys_in_order())

    # quick demo of how
    # to use the timing decorator included
    # in indexer.util
    loopy_loop()


if __name__ == "__main__":
    main()
