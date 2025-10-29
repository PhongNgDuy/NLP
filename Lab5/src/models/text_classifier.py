# src/models/text_classifier.py

from typing import List, Dict
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

class TextClassifier:
    def __init__(self, vectorizer):
        """
        vectorizer: đối tượng TF-IDF hoặc CountVectorizer đã được khởi tạo sẵn.
        """
        self.vectorizer = vectorizer
        self._model = LogisticRegression(solver='liblinear')

    def fit(self, texts: List[str], labels: List[int]) -> None:
        """
        Huấn luyện mô hình Logistic Regression.
        """
        X = self.vectorizer.fit_transform(texts)
        self._model.fit(X, labels)

    def predict(self, texts: List[str]) -> List[int]:
        """
        Dự đoán nhãn cho danh sách văn bản mới.
        """
        X = self.vectorizer.transform(texts)
        return self._model.predict(X)

    def evaluate(self, y_true: List[int], y_pred: List[int]) -> Dict[str, float]:
        """
        Tính các chỉ số đánh giá: Accuracy, Precision, Recall, F1.
        """
        return {
            "accuracy": accuracy_score(y_true, y_pred),
            "precision": precision_score(y_true, y_pred),
            "recall": recall_score(y_true, y_pred),
            "f1": f1_score(y_true, y_pred)
        }
