from src.preprocessing.regex_tokenizer import RegexTokenizer
from src.representations.count_vectorizer import CountVectorizer
from src.core.dataset_loaders import load_raw_text_data

def main():
    tokenizer = RegexTokenizer()
    vectorizer = CountVectorizer(tokenizer)

    corpus = [
        "I love NLP.",
        "I love programming.",
        "NLP is a subfield of AI."
    ]

    vectors = vectorizer.fit_transform(corpus)

    print("\n--- Testing CountVectorizer ---")
    print("Vocabulary:", vectorizer.vocabulary_)
    print("Document-Term Matrix:")
    for vec in vectors:
        print(vec)

    dataset_path = r"D:\NLP\Lab1\UD_English-EWT\en_ewt-ud-train.txt"
    raw_text = load_raw_text_data(dataset_path)

    sample_docs = raw_text.split("\n")[:5]
    sample_docs = [doc for doc in sample_docs if doc.strip()]

    print("\n--- Vectorize Sample Text from UD_English-EWT ---")
    vectors = vectorizer.fit_transform(sample_docs)

    print("Vocabulary size:", len(vectorizer.vocabulary_))
    print("Tokens in vocab:", list(vectorizer.vocabulary_.keys()))
    print("Document-Term Matrix:")
    for vec in vectors:
        print(vec)


if __name__ == "__main__":
    main()
