# test/Lab4_test.py

import sys, os
import numpy as np
import time

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.representations.word_embedder import WordEmbedder


def main():
    # === Setup log file ===
    results_dir = "results"
    os.makedirs(results_dir, exist_ok=True)
    log_path = os.path.join(results_dir, "lab4_word_embedding_demo_log.txt")

    start_time = time.time()

    with open(log_path, "w", encoding="utf-8") as log:
        log.write("Lab 4 - Word Embedding Demonstration\n")
        log.write("=" * 60 + "\n\n")

        # Redirect print to both console & file
        def log_print(*args, **kwargs):
            text = " ".join(str(a) for a in args)
            print(text, **kwargs)
            log.write(text + "\n")

        # === Load model ===
        embedder = WordEmbedder("glove-wiki-gigaword-50")

        log_print("\n=== Word Vector Example ===")
        king_vec = embedder.get_vector("king")
        log_print("Vector for 'king':")
        log_print(np.round(king_vec, 4))

        log_print("\n=== Word Similarities ===")
        sim1 = embedder.get_similarity("king", "queen")
        sim2 = embedder.get_similarity("king", "man")
        log_print(f"Similarity (king, queen): {sim1:.4f}")
        log_print(f"Similarity (king, man):   {sim2:.4f}")

        log_print("\n=== Most Similar Words to 'computer' ===")
        similar_words = embedder.get_most_similar("computer", top_n=10)
        for word, score in similar_words:
            log_print(f"{word:15s} -> {score:.4f}")

        log_print("\n=== Document Embedding ===")
        doc = "The queen rules the country."
        doc_vec = embedder.embed_document(doc)
        log_print(f"Document: '{doc}'")
        log_print("Embedding vector (mean of word vectors):")
        log_print(np.round(doc_vec, 4))

        end_time = time.time()
        total_time = end_time - start_time

        log_print("\n" + "=" * 60)
        log_print(f"Total runtime: {total_time:.2f}s")

    print(f"Log file generated at: {log_path}")


if __name__ == "__main__":
    main()
