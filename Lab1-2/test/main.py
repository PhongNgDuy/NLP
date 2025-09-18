from src.preprocessing.simple_tokenizer import SimpleTokenizer
from src.preprocessing.regex_tokenizer import RegexTokenizer
from src.core.dataset_loaders import load_raw_text_data

if __name__ == "__main__":
    simple_tokenizer = SimpleTokenizer()
    regex_tokenizer = RegexTokenizer()

    test_sentences = [
        "Hello, world! This is a test.",
        "NLP is fascinating... isn't it?",
        "Let's see how it handles 123 numbers and punctuation!"
    ]

    print("\n--- Testing SimpleTokenizer and RegexTokenizer ---")
    for sent in test_sentences:
        print(f"\nInput: {sent}")
        print("SimpleTokenizer:", simple_tokenizer.tokenize(sent))
        print("RegexTokenizer :", regex_tokenizer.tokenize(sent))

    dataset_path = r"D:\NLP\Lab1\UD_English-EWT\en_ewt-ud-train.txt"
    raw_text = load_raw_text_data(dataset_path)
    sample_text = raw_text[:500] 

    print("\n--- Tokenizing Sample Text from UD_English-EWT ---")
    print(f"Original Sample (first 100 chars): {sample_text[:100]}...")

    simple_tokens = simple_tokenizer.tokenize(sample_text)
    regex_tokens = regex_tokenizer.tokenize(sample_text)

    print("SimpleTokenizer Output (first 20 tokens):", simple_tokens[:20])
    print("RegexTokenizer Output  (first 20 tokens):", regex_tokens[:20])
