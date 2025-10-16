import os
import re
import sys
import time
from typing import List
import numpy as np
import scipy.linalg
if not hasattr(scipy.linalg, "triu"):
    scipy.linalg.triu = np.triu
from gensim.models import Word2Vec

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
src_dir = os.path.join(project_root, "src", "representations")
sys.path.insert(0, src_dir)

class EWTDataStreamer:
    """Stream and tokenize sentences from the UD English EWT corpus."""

    def __init__(self, file_path: str):
        self.file_path = file_path

    def load_sentences(self, output_file=None) -> List[List[str]]:
        """Load and clean sentences (alphabetic tokens only)."""
        if not os.path.exists(self.file_path):
            msg = f"[ERROR] File not found: {self.file_path}"
            if output_file:
                output_file.write(msg + "\n")
            return []

        sentences = []
        with open(self.file_path, "r", encoding="utf-8") as f:
            for line in f:
                tokens = re.findall(r"\b[a-zA-Z]+\b", line.lower())
                if len(tokens) >= 3:
                    sentences.append(tokens)

        return sentences

def train_word2vec_model(data_path: str, model_save_path: str, output_file) -> Word2Vec:
    """Train a Word2Vec model and log training details."""
    output_file.write("Loading and preprocessing data...\n")
    streamer = EWTDataStreamer(data_path)
    sentences = streamer.load_sentences(output_file)

    if not sentences:
        output_file.write("No sentences found. Exiting.\n")
        return None

    output_file.write(f"Training on {len(sentences):,} sentences.\n")

    start_time = time.time()

    model = Word2Vec(
        sentences=sentences,
        vector_size=100,
        window=5,
        min_count=2,
        workers=4,
        sg=0,
        epochs=15
    )

    duration = time.time() - start_time
    output_file.write(f"Duration: {duration:.2f}s ({duration/60:.2f} min)\n")
    output_file.write(f"Vocabulary size: {len(model.wv.key_to_index):,}\n\n")

    os.makedirs(os.path.dirname(model_save_path), exist_ok=True)
    model.save(model_save_path)
    output_file.write(f"Model saved to: {model_save_path}\n\n")

    return model

def demonstrate_model_usage(model: Word2Vec, output_file):
    """Demonstrate similarity and analogy examples."""
    output_file.write("=== Model Demonstration ===\n")
    test_words = ["good", "people", "go", "day"]
    for w in test_words:
        if w in model.wv.key_to_index:
            sims = model.wv.most_similar(w, topn=3)
            output_file.write(f"\nMost similar to '{w}':\n")
            for word, score in sims:
                output_file.write(f"  {word:10s}  {score:.3f}\n")

    # Analogy example
    if all(w in model.wv.key_to_index for w in ["man", "woman", "king"]):
        analogy = model.wv.most_similar(positive=["king", "woman"], negative=["man"], topn=3)
        output_file.write("\nAnalogy: man : woman :: king : ?\n")
        for w, s in analogy:
            output_file.write(f"  {w:10s}  {s:.3f}\n")

def main():
    """Main entry point for training and evaluation."""
    results_dir = "results"
    os.makedirs(results_dir, exist_ok=True)
    output_log = os.path.join(results_dir, "lab4_training_log.txt")

    with open(output_log, "w", encoding="utf-8") as f:
        f.write("Lab 4 - Custom Word2Vec Training\n")
        f.write("=" * 60 + "\n")

        data_path = r"d:\NLP\data\UD_English-EWT\en_ewt-ud-train.txt"
        model_path = os.path.join(results_dir, "word2vec_ewt.model")

        if not os.path.exists(data_path):
            f.write(f"[ERROR] Training data not found: {data_path}\n")
            return

        try:
            total_start = time.time()
            model = train_word2vec_model(data_path, model_path, f)
            if model:
                demonstrate_model_usage(model, f)
            total_end = time.time()

            f.write("\n" + "=" * 60 + "\n")
            f.write(f"Total runtime: {total_end - total_start:.2f}s\n")

        except Exception as e:
            f.write(f"\n[ERROR] {e}\n")

    print(f"Output log saved to: {output_log}")


if __name__ == "__main__":
    main()
