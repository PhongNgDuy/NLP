import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from src.models.text_classifier import TextClassifier

def main():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    results_dir = os.path.join(project_root, "results")
    os.makedirs(results_dir, exist_ok=True)
    output_path = os.path.join(results_dir, "lab5_sklearn_output.txt")

    texts = [
        "This movie is fantastic and I love it!",
        "I hate this film, it's terrible.",
        "The acting was superb, a truly great experience.",
        "What a waste of time, absolutely boring.",
        "Highly recommend this, a masterpiece.",
        "Could not finish watching, so bad."
    ]
    labels = [1, 0, 1, 0, 1, 0]  # 1 = positive, 0 = negative

    with open(output_path, "w", encoding="utf-8") as f:
        def log(msg=""):
            print(msg)
            f.write(msg + "\n")

        log("=" * 60)
        log("Lab 5 - Task 1 & 2: Text Classification (Scikit-learn)")
        log("=" * 60)

        # 1. Chia train/test
        X_train, X_test, y_train, y_test = train_test_split(
            texts, labels, test_size=0.2, random_state=42
        )

        # 2. Khởi tạo vectorizer TF-IDF
        vectorizer = TfidfVectorizer()

        # 3. Tạo classifier
        clf = TextClassifier(vectorizer)

        # 4. Huấn luyện
        clf.fit(X_train, y_train)

        # 5. Dự đoán
        y_pred = clf.predict(X_test)
        log(f"Predictions: {y_pred}")

        # 6. Đánh giá
        metrics = clf.evaluate(y_test, y_pred)
        log("\nEvaluation Results:")
        for k, v in metrics.items():
            log(f"{k.capitalize()}: {v:.4f}")

        log("=" * 60)
        log("Text classification (sklearn) completed.")
        log(f"Output saved to: {output_path}")

if __name__ == "__main__":
    main()
