# DS4300 - Spring 2025 - Practical #1 - Index It

## Overview
This program indexes financial news articles using different indexing data structures, including a Binary Search Tree (BST), an AVL Tree, a Hash Map, and a Trie (Prefix) Tree. It processes preprocessed text files, inserts words into an index, and performs searches to measure the most efficient data structures to store and search for this data.

## Installation and Setup
### Prerequisites
- Python 3.11
- Required libraries: `json`, `pickle`, `csv`, `random`, `string`, `os`, `hashlib`, `argparse`, `typing`, `time`, `jupyter`, `jupyterlab`
- The dataset of preprocessed news articles

### Directory Structure
Ensure the following directory structure exists before running the program:
```
practical-01-ruchidhiyanka/
│── docs/
│── indexer/
│   ├── maps/
│   │   ├── hash_map.py
│   ├── trees/
│   │   ├── avl_node.py
│   │   ├── avl_tree.py
│   │   ├── bst_index.py
│   │   ├── bst_node.py
│   │   ├── trie_index.py
│   │   ├── trie_node.py
│   ├── util/
│   │   ├── nltk_modules.py
│   │   ├── parser_utils.py
│   │   ├── timer.py
│   ├── abstract_index.py
│── timing_data/
│   │   ├── timing_data.csv
│── search_results/
│   │   ├── results_of_specific_searches_here
│── tests/
│   │   ├── test_bin_search_tree.py
│── timing_data/
│   │   ├── Timing_Data_Visualizations.ipynb
│   │   ├── timing_data.csv
│── README.md
│── assign_01.py
│── requirements.txt
```

## Execution Instructions

1. **Set the Data Directory**
   Update the `data_directory` variable in `main()` of `assign_01.py` with the absolute path to the dataset folder containing preprocessed JSON articles.

2. **Run the Program**
   Execute the script from the terminal:
   ```sh
   python assign_01.py -d "./practical-01-ruchidhiyanka/USFinancialNewsArticles-preprocessed"
   ```
   
3. **Indexing and Searching**
   - The script will index words from the dataset into the selected data structures (BST, AVL Tree, Hashmap, and Trie Tree).
   - It will generate search datasets and run experiments to measure the time it takes to search for the tokens from the test datasets.
   - Results will be saved in CSV files under `timing_data/`.

## Output Files
- **Timing Data**: `timing_data/timing_data.csv` (search performance metrics)
- **Search Results**: `search_results/Add_results_of_specific_searches_here` (individual search result files)
- **Generated Datasets**: `datasets.pkl` (pickled test datasets)

## Notes
- Modify `data_structures` in `main()` of `assign_01.py` to experiment with different index types.

