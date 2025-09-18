import string
from src.core.interfaces import Tokenizer

class SimpleTokenizer(Tokenizer):
    def tokenize(self, text: str) -> list[str]:
        text = text.lower()
        for p in string.punctuation:
            text = text.replace(p, f" {p} ")
        tokens = text.split()
        return tokens
