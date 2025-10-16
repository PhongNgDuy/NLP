# src/representations/word_embedder.py

import numpy as np
import scipy.linalg

if not hasattr(scipy.linalg, "triu"):
    scipy.linalg.triu = np.triu

import gensim.downloader as api

from typing import List

class WordEmbedder:
    def __init__(self, model_name: str = "glove-wiki-gigaword-50"):
        """
        Load a pre-trained word embedding model from gensim.
        """
        print(f"Loading model '{model_name}' (this may take a while the first time)...")
        self.model = api.load(model_name)
        self.vector_size = self.model.vector_size
        print(f"Model '{model_name}' loaded successfully with {self.vector_size}-dimensional vectors.")

    def get_vector(self, word: str) -> np.ndarray:
        """
        Return the embedding vector of a given word.
        If the word is not in the vocabulary, return a zero vector.
        """
        if word in self.model.key_to_index:
            return self.model[word]
        else:
            print(f"'{word}' not found in vocabulary (OOV). Returning zero vector.")
            return np.zeros(self.vector_size)

    def get_similarity(self, word1: str, word2: str) -> float:
        """
        Compute cosine similarity between two words.
        """
        if word1 not in self.model.key_to_index or word2 not in self.model.key_to_index:
            print(f"One of the words ('{word1}', '{word2}') is not in vocabulary.")
            return 0.0
        return self.model.similarity(word1, word2)

    def get_most_similar(self, word: str, top_n: int = 10) -> List[tuple]:
        """
        Get top N most similar words.
        """
        if word not in self.model.key_to_index:
            print(f"'{word}' not found in vocabulary.")
            return []
        return self.model.most_similar(word, topn=top_n)

    def embed_document(self, document: str) -> np.ndarray:
        """
        Compute a document embedding by averaging all word vectors in the document.
        Uses a simple whitespace-based tokenizer.
        """
        tokens = document.lower().split()
        vectors = [self.get_vector(tok) for tok in tokens if tok in self.model.key_to_index]

        if not vectors:
            print("No valid tokens found in document. Returning zero vector.")
            return np.zeros(self.vector_size)

        return np.mean(vectors, axis=0)
