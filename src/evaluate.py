import os
import csv

from compressor import (
    read_source_code,
    remove_comments_and_extra_whitespace,
    create_token_dictionary,
    apply_token_mapping,
    calculate_compression_ratio,
)


DATA_DIR = "data"
RESULTS_DIR = "results"
OUTPUT_FILE = os.path.join(RESULTS_DIR, "evaluation_results.csv")


def evaluate_file(input_file):
    """Compress one source-code file and return its statistics."""

    original_code = read_source_code(input_file)

    original_size = len(original_code.encode("utf-8"))

    cleaned_code = remove_comments_and_extra_whitespace(
        original_code
    )

    token_dictionary = create_token_dictionary(
        cleaned_code
    )

    compressed_code = apply_token_mapping(
        cleaned_code,
        token_dictionary
    )

    filename = os.path.basename(input_file)
    base_name = os.path.splitext(filename)[0]

    compressed_file = os.path.join(
        RESULTS_DIR,
        f"{base_name}_compressed.txt"
    )

    dictionary_file = os.path.join(
        RESULTS_DIR,
        f"{base_name}_dictionary.csv"
    )

    with open(compressed_file, "w", encoding="utf-8") as file:
        file.write(compressed_code)

    with open(dictionary_file, "w", encoding="utf-8") as file:
        for word, token in token_dictionary.items():
            file.write(f"{word},{token}\n")

    compressed_size = os.path.getsize(compressed_file)

    compression_ratio = calculate_compression_ratio(
        original_size,
        compressed_size
    )

    return {
        "File": filename,
        "Original Size (bytes)": original_size,
        "Compressed Size (bytes)": compressed_size,
        "Compression Ratio (%)": round(compression_ratio, 2),
        "Tokens Replaced": len(token_dictionary),
    }


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)

    supported_extensions = (
        ".c",
        ".cpp",
        ".py",
        ".java",
    )

    results = []

    for filename in sorted(os.listdir(DATA_DIR)):
        if filename.lower().endswith(supported_extensions):
            input_file = os.path.join(DATA_DIR, filename)

            result = evaluate_file(input_file)
            results.append(result)

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        fieldnames = [
            "File",
            "Original Size (bytes)",
            "Compressed Size (bytes)",
            "Compression Ratio (%)",
            "Tokens Replaced",
        ]

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(results)

    print("=" * 60)
    print("SOURCE CODE COMPRESSION EVALUATION")
    print("=" * 60)

    for result in results:
        print(
            f"{result['File']}: "
            f"{result['Original Size (bytes)']} → "
            f"{result['Compressed Size (bytes)']} bytes | "
            f"{result['Compression Ratio (%)']}%"
        )

    print("\nEvaluation completed successfully!")
    print(f"Results saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()