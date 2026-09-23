# Token-Based Source Code Compression

A Python-based source code compression system that uses preprocessing, dynamic tokenization, and dictionary-based mapping to reduce the size of source code files.

## Project Overview

This project compresses source code by:

1. Removing comments and unnecessary whitespace.
2. Detecting repeated identifiers and keywords.
3. Replacing repeated words with compact tokens such as `@1`, `@2`, etc.
4. Storing the token mappings in a dictionary.
5. Calculating the compression ratio.
6. Supporting decompression by reversing the token mapping.

## Project Structure

```text
source-code-compression/
│
├── data/
│   ├── example.c
│   ├── module.java
│   ├── sample.cpp
│   └── test.py
│
├── results/
│   └── evaluation_results.csv
│
├── src/
│   ├── compressor.py
│   ├── decompressor.py
│   └── evaluate.py
│
├── .gitignore
└── README.md