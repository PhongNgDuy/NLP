# Lab 4: Word Embeddings with Word2Vec

## Mô tả
- **Task 1**: Triển khai word embeddings với lớp `WordEmbedder`.
- **Task 2**: Tạo nhúng tài liệu bằng cách trung bình các vector từ.
- **Evaluation**: Kiểm tra và in kết quả chạy.
- **Bonus Task**: Huấn luyện mô hình Word2Vec từ đầu trên tập dữ liệu UD English EWT.
- **Advanced Task**: Mở rộng Word2Vec với Apache Spark trên tập dữ liệu lớn C4.


## Công nghệ sử dụng
- **Ngôn ngữ lập trình**: Python 3.11
- **Thư viện**:
  - Gensim
  - NumPy, SciPy
  - PySpark 
- **Công cụ**: Apache Spark
- **Tập dữ liệu**:
  - GloVe pre-trained: `glove-wiki-gigaword-50` (50 chiều, huấn luyện trên Wikipedia)
  - UD English EWT (`en_ewt-ud-train.txt`) cho Bonus Task
  - C4 (`c4-train.00000-of-01024-30K.json.gz`) cho Advanced Task

## Cài đặt
1. Cài đặt các thư viện cần thiết:
   ```bash
   pip install -r requirements.txt
   ```
   - Bao gồm: `gensim`, `numpy`, `scipy`, `pyspark`
2. Tải mô hình GloVe: Tự động tải khi chạy `WordEmbedder` lần đầu (khoảng 65MB).
3. Cài đặt Apache Spark.
5. Chuẩn bị dữ liệu:
   - Đặt `en_ewt-ud-train.txt` vào `D:\NLP\data\UD_English-EWT\` (cập nhật đường dẫn nếu cần trong code).
   - Đặt `c4-train.00000-of-01024-30K.json.gz` vào `D:\NLP\data\` (cập nhật đường dẫn nếu cần).

## Kết quả
### Task 1: Embeddings
- **File**: `src/representations/word_embedder.py`
- **Mô tả**: Lớp `WordEmbedder` tải mô hình GloVe, lấy vector từ, tính cosine similarity, tìm từ tương tự, và xử lý OOV (trả về vector zero).
- **Evaluation File**: `test/Lab4_test.py`
- **Chạy**:
   ```bash
   python test/Lab4_test.py
   ```
- **Kết quả** (từ `results/lab4_word_embedding_demo_log.txt`):
  - Vector cho "king": [0.5045, 0.6861, ...]
  - Độ tương đồng (king, queen): 0.7839
  - Độ tương đồng (king, man): 0.5309
  - Từ tương tự với "computer": computers (0.9165), software (0.8815), ...
  - Thời gian chạy: 10.35s

### Task 2: Nhúng Tài liệu
- **Triển khai**: Trong `embed_document` của `WordEmbedder`, sử dụng tokenizer đơn giản (split), bỏ qua OOV, tính trung bình vector.
- **Kết quả** (từ Evaluation):
  - Tài liệu: "The queen rules the country."
  - Vector nhúng: [0.0644, 0.4338, ...]

### Bonus Task: Huấn luyện Word2Vec từ đầu (CBOW)
- **File**: `test/lab4_embedding_training_demo.py`
- **Mô tả**: Stream dữ liệu từ UD English EWT (13,572 câu), huấn luyện Word2Vec CBOW (vector_size=100, window=5, min_count=2, epochs=15), lưu mô hình, kiểm tra tương đồng và analog.
- **Chạy**:
   ```bash
   python test/lab4_embedding_training_demo.py
   ```
- **Kết quả** (từ `results/lab4_training_log.txt`):
  - Thời gian huấn luyện: 0.85s
  - Kích thước từ vựng: 8,384
  - Từ tương tự với "good": nice (0.908), pretty (0.877), food (0.876)
  - Analog (man : woman :: king : ?): feathered (0.972), plastic (0.965), ...
  - Mô hình lưu tại: `results/word2vec_ewt.model`
  - Thời gian tổng: 0.91s

### Advanced Task: Word2Vec với Apache Spark
- **File**: `test/lab4_spark_word2vec_demo.py`
- **Mô tả**: Sử dụng PySpark để tải dữ liệu C4 (JSON), tiền xử lý (lowercase, loại bỏ dấu câu, split), huấn luyện Word2Vec (vectorSize=100, minCount=5), tìm từ đồng nghĩa.
- **Chạy**:
   ```bash
   spark-submit test/lab4_spark_word2vec_demo.py
   ```
- **Kết quả** (từ `results/lab4_spark_output.txt`):
  - Tài liệu: 30,000
  - Token tổng: 10,609,694
  - Token trung bình/tài liệu: 353.66
  - Kích thước từ vựng: 52,218
  - Từ đồng nghĩa với "computer": desktop (0.6618), computers (0.6405), ...

## Cấu trúc thư mục
```
Lab4/
│
├── src/
│   └── representations/
│       └── word_embedder.py             # Lớp WordEmbedder (GloVe embeddings)
│
├── test/
│   ├── Lab4_test.py                     # Evaluation cho Tasks 1-2
│   ├── lab4_embedding_training_demo.py  # Bonus Task – Huấn luyện Word2Vec (CBOW)
│   └── lab4_spark_word2vec_demo.py      # Advanced Task – Word2Vec bằng Spark
│
├── results/
│   ├── lab4_word_embedding_demo_log.txt # Log GloVe (Tasks 1-2)
│   ├── lab4_training_log.txt            # Log huấn luyện Word2Vec (Bonus)
│   ├── lab4_spark_output.txt            # Log Spark (Advanced)
│   └── word2vec_ewt.model               # Mô hình Word2Vec CBOW
│
├── requirements.txt                     # Thư viện cần cài đặt
└── README.md                            # Báo cáo Lab 4
```

## Đánh giá

- **Task 1 – Triển khai Word Embeddings với lớp `WordEmbedder`:**  
  Mô hình `glove-wiki-gigaword-50` được tải thành công từ Gensim, hoạt động ổn định.  
  Việc truy xuất vector, tính độ tương đồng giữa các từ (*king–queen*, *king-man*),  
  và tìm các từ gần nhất đều cho kết quả chính xác, thể hiện tốt ngữ nghĩa.


- **Task 2 – Tạo nhúng tài liệu (Document Embedding):**  
  Việc tính trung bình vector các từ trong văn bản giúp tạo embedding biểu diễn ý nghĩa tổng thể.  
  Cách tiếp cận đơn giản nhưng hiệu quả, phù hợp cho các ứng dụng cơ bản như phân loại văn bản hoặc so khớp ngữ nghĩa.  
  Hàm `embed_document()` hoạt động đúng, tính trung bình các vector để biểu diễn toàn câu,  
  cho kết quả nhúng tài liệu hợp lý và ổn định.


- **Bonus Task – Huấn luyện Word2Vec từ đầu (CBOW):**  
  Mô hình được huấn luyện thành công trên 13,572 câu từ tập EWT, với 8,384 từ vựng.  
  Các từ tương tự (good ~ *nice, pretty*) được phát hiện chính xác, thể hiện khả năng học ngữ nghĩa.  
  Tuy nhiên, kết quả tìm từ tương tự còn 1 số từ chưa hợp lý (good ~ food), hay **analogy** (*king - man + woman ≈ queen*) chưa tối ưu do dữ liệu nhỏ và số epoch thấp.


- **Advanced Task – Huấn luyện Word2Vec phân tán bằng Apache Spark:**  
  Mô hình Spark Word2Vec xử lý thành công 30,000 văn bản trong tập dữ liệu C4, tận dụng tốt khả năng đa luồng.  
  Kết quả thu được hợp lý với các từ đồng nghĩa (*computer → laptop, desktop, pc*),  
  chứng minh tính đúng đắn của mô hình và khả năng mở rộng khi áp dụng trên dữ liệu lớn.  
