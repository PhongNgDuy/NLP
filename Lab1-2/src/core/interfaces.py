from abc import ABC, abstractmethod
from typing import List

class Tokenizer(ABC):
    @abstractmethod
    def tokenize(self, text: str) -> List[str]:
        pass

class Vectorizer(ABC):
    @abstractmethod
    def fit(self, corpus: List[str]):
        pass

    @abstractmethod
    def transform(self, documents: List[str]) -> List[List[int]]:
        pass

    def fit_transform(self, corpus: List[str]) -> List[List[int]]:
        self.fit(corpus)
        return self.transform(corpus)
