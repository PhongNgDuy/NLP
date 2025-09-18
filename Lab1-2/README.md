# Lab 1 & 2 Report

## Lab 1: Text Tokenization
### Mô tả công việc
- Tạo interface `Tokenizer` trong `src/core/interfaces.py`.
- Cài đặt `SimpleTokenizer` trong `src/preprocessing/simple_tokenizer.py`.
- Cài đặt `RegexTokenizer` trong `src/preprocessing/regex_tokenizer.py`.
- Tạo file `main.py` để chạy thử nghiệm trên:
  - Corpus mẫu.
  - UD_English-EWT dataset.
### Cách chạy code và ghi log kết quả
  ```
  python -m test.main
  ```

### Kết quả chạy
```
--- Testing SimpleTokenizer and RegexTokenizer ---

Input: Hello, world! This is a test.
SimpleTokenizer: ['hello', ',', 'world', '!', 'this', 'is', 'a', 'test', '.']
RegexTokenizer : ['hello', ',', 'world', '!', 'this', 'is', 'a', 'test', '.']

Input: NLP is fascinating... isn't it?
SimpleTokenizer: ['nlp', 'is', 'fascinating', '.', '.', '.', 'isn', "'", 't', 'it', '?']
RegexTokenizer : ['nlp', 'is', 'fascinating', '.', '.', '.', 'isn', "'", 't', 'it', '?']

Input: Let's see how it handles 123 numbers and punctuation!
SimpleTokenizer: ['let', "'", 's', 'see', 'how', 'it', 'handles', '123', 'numbers', 'and', 'punctuation', '!']
RegexTokenizer : ['let', "'", 's', 'see', 'how', 'it', 'handles', '123', 'numbers', 'and', 'punctuation', '!']

--- Tokenizing Sample Text from UD_English-EWT ---
Original Sample (first 100 chars): Al-Zaman : American forces killed Shaikh Abdullah al-Ani, the preacher at the       
mosque in the town of ...
SimpleTokenizer Output (first 20 tokens): ['al', '-', 'zaman', ':', 'american', 'forces', 'killed', 'shaikh', 'abdullah', 'al', '-', 'ani', ',', 'the', 'preacher', 'at', 'the', 'mosque', 'in', 'the']
RegexTokenizer Output  (first 20 tokens): ['al', '-', 'zaman', ':', 'american', 'forces', 'killed', 'shaikh', 'abdullah', 'al', '-', 'ani', ',', 'the', 'preacher', 'at', 'the', 'mosque', 'in', 'the']
```
### Giải thích kết quả
- SimpleTokenizer chỉ dựa vào khoảng trắng và xử lý thủ công dấu câu nên hoạt động tốt với các ví dụ cơ bản.  
- RegexTokenizer sử dụng regex nên tách token chính xác hơn trong các trường hợp phức tạp.  


## Lab 2: Count Vectorization
### Mô tả công việc
- Tạo interface `Vectorizer` trong `src/core/interfaces.py`.
- Cài đặt `CountVectorizer` trong `src/representations/count_vectorizer.py`.
- Tạo file `test/lab2_test.py` để chạy thử nghiệm trên:
  - Corpus mẫu.
  - UD_English-EWT dataset.
### Cách chạy code và ghi log kết quả
  ```
  python -m test.lab2_test 
  ```

### Kết quả chạy
```
--- Testing CountVectorizer ---
Vocabulary: {'.': 0, 'a': 1, 'ai': 2, 'i': 3, 'is': 4, 'love': 5, 'nlp': 6, 'of': 7, 'programming': 8, 'subfield': 9}  
Document-Term Matrix:
[1, 0, 0, 1, 0, 1, 1, 0, 0, 0]
[1, 0, 0, 1, 0, 1, 0, 0, 1, 0]
[1, 1, 1, 0, 1, 0, 1, 1, 0, 1]

--- Vectorize Sample Text from UD_English-EWT ---
Vocabulary size: 65
Tokens in vocab: ['!', ',', '-', '.', '2', '3', ':', '[', ']', 'a', 'abdullah', 'al', 'american', 'ani', 'announced', 'at', 'authorities', 'baghdad', 'be', 'being', 'border', 'busted', 'by', 'causing', 'cells', 'cleric', 'come', 'dpa', 'for', 'forces', 'had', 'in', 'interior', 'iraqi', 'killed', 'killing', 'ministry', 'moi', 'mosque', 'near', 'of', 'officials', 'operating', 'preacher', 'qaim', 'respected', 'run', 'shaikh', 'syrian', 'terrorist', 'that', 'the', 'them', 'they', 'this', 'to', 'town', 'trouble', 'two', 'up', 'us', 'were', 'will', 'years', 'zaman']
Document-Term Matrix:
[0, 1, 2, 0, 0, 0, 1, 0, 0, 0, 1, 2, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
[0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 2, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 2, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0]
[0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0]
[1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 2, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
```
### Giải thích kết quả
- Với corpus nhỏ, ma trận dễ quan sát và trực quan.  
Với dataset lớn như UD_English-EWT, vocab sẽ có hàng chục nghìn token và document-term matrix sẽ rất thưa.
- Bag-of-Words đơn giản và hiệu quả cho các bài toán cơ bản, nhưng có hạn chế là không nắm bắt được ngữ cảnh hay thứ tự từ.  
  
