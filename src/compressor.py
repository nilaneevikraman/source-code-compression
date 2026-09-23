import re
import json
import os


def read_source_code(file_path):
    """Read the original source-code file."""
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def remove_comments_and_extra_whitespace(code):
    """Remove comments, blank lines, and unnecessary whitespace."""

    # Remove single-line comments
    code = re.sub(r"//.*", "", code)

    # Remove multi-line comments
    code = re.sub(r"/\*.*?\*/", "", code, flags=re.DOTALL)

    # Remove blank lines
    lines = code.splitlines()
    lines = [line.strip() for line in lines if line.strip()]

    return "\n".join(lines)


def create_token_dictionary(code):
    """Find repeated identifiers/keywords and assign short tokens."""

    # Find words used in the source code
    words = re.findall(r"\b[A-Za-z_][A-Za-z0-9_]*\b", code)

    # Count occurrences
    word_counts = {}

    for word in words:
        word_counts[word] = word_counts.get(word, 0) + 1

    # Only replace words that occur more than once
    repeated_words = {
        word: count
        for word, count in word_counts.items()
        if count > 1
    }

    # Sort by frequency, highest first
    repeated_words = sorted(
        repeated_words.items(),
        key=lambda item: item[1],
        reverse=True
    )

    token_dictionary = {}

    for index, (word, _) in enumerate(repeated_words, start=1):
        token_dictionary[word] = f"@{index}"

    return token_dictionary


def apply_token_mapping(code, token_dictionary):
    """Replace repeated words with their assigned tokens."""

    # Replace longer words first to avoid partial replacement issues
    sorted_words = sorted(
        token_dictionary.keys(),
        key=len,
        reverse=True
    )

    for word in sorted_words:
        token = token_dictionary[word]

        pattern = rf"\b{re.escape(word)}\b"
        code = re.sub(pattern, token, code)

    return code


def calculate_compression_ratio(original_size, compressed_size):
    """Calculate compression percentage."""

    if original_size == 0:
        return 0

    return ((original_size - compressed_size) / original_size) * 100


def compress_file(input_file):
    """Complete compression workflow."""

    print("=" * 50)
    print("TOKEN-BASED SOURCE CODE COMPRESSION")
    print("=" * 50)

    # Read source code
    original_code = read_source_code(input_file)

    original_size = len(original_code.encode("utf-8"))

    print(f"\nInput file: {input_file}")
    print(f"Original size: {original_size} bytes")

    # Preprocess source code
    cleaned_code = remove_comments_and_extra_whitespace(original_code)

    # Create token dictionary
    token_dictionary = create_token_dictionary(cleaned_code)

    print(f"Repeated words replaced: {len(token_dictionary)}")

    # Apply token mapping
    compressed_code = apply_token_mapping(
        cleaned_code,
        token_dictionary
    )

    # Create output directory
    output_directory = "results"
    os.makedirs(output_directory, exist_ok=True)

    # Save compressed code
    compressed_file = os.path.join(
        output_directory,
        "comp.txt"
    )

    with open(compressed_file, "w", encoding="utf-8") as file:
        file.write(compressed_code)

    # Save dictionary
    dictionary_file = os.path.join(
        output_directory,
        "dict.json"
    )

    with open(dictionary_file, "w", encoding="utf-8") as file:
        json.dump(
            token_dictionary,
            file,
            indent=4
        )

    # Calculate compressed size
    compressed_size = os.path.getsize(compressed_file)

    compression_ratio = calculate_compression_ratio(
        original_size,
        compressed_size
    )

    print(f"Compressed size: {compressed_size} bytes")
    print(f"Compression ratio: {compression_ratio:.2f}%")

    print("\nFiles created:")
    print(f"  {compressed_file}")
    print(f"  {dictionary_file}")

    print("\nCompression completed successfully!")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python src/compressor.py <source_file>")
        print("Example: python src/compressor.py data/test.py")
    else:
        input_file = sys.argv[1]
        compress_file(input_file)