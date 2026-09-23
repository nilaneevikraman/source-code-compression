import json
import re
import sys


def decompress_file(compressed_file):
    """Decompress a tokenized source-code file."""

    dictionary_file = "results/dict.json"
    output_file = "results/recovered_code.txt"

    # Read compressed code
    with open(compressed_file, "r", encoding="utf-8") as file:
        compressed_code = file.read()

    # Read token dictionary
    with open(dictionary_file, "r", encoding="utf-8") as file:
        token_dictionary = json.load(file)

    # Reverse the dictionary
    reverse_dictionary = {
        token: word
        for word, token in token_dictionary.items()
    }

    # Replace tokens with original words
    sorted_tokens = sorted(
        reverse_dictionary.keys(),
        key=len,
        reverse=True
    )

    recovered_code = compressed_code

    for token in sorted_tokens:
        word = reverse_dictionary[token]

        pattern = rf"(?<!\w){re.escape(token)}(?!\w)"

        recovered_code = re.sub(
            pattern,
            word,
            recovered_code
        )

    # Save recovered source code
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(recovered_code)

    print("=" * 50)
    print("SOURCE CODE DECOMPRESSION")
    print("=" * 50)
    print(f"\nCompressed file: {compressed_file}")
    print(f"Dictionary: {dictionary_file}")
    print(f"Recovered file: {output_file}")
    print("\nDecompression completed successfully!")
    print("\nNote: Formatting is normalized during compression.")
    print("The recovered source preserves the code content,")
    print("but original indentation and blank lines are not restored.")


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: python src/decompressor.py <compressed_file>")
        print("Example: python src/decompressor.py results/comp.txt")
    else:
        compressed_file = sys.argv[1]

        decompress_file(compressed_file)