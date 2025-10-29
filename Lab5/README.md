# Lab 5: Phân loại Văn bản (Text Classification)

## 1. Mục tiêu

Mục tiêu của bài tập này là xây dựng một quy trình (pipeline) phân loại văn bản hoàn chỉnh, từ văn bản thô đến một mô hình học máy đã được huấn luyện, áp dụng các kỹ thuật tokenization và vector hóa, sử dụng scikit-learn và pyspark.

## 2. Cấu trúc thư mục 
````
NLP/Lab5/
├── src/
│ └── models/
│ └── text_classifier.py # Task 1 – class TextClassifier (sklearn)
│
├── test/
│ ├── lab5_test.py # Task 2 – TF-IDF + LogisticRegression baseline
│ └── lab5_improvement_test.py # Task 3–4 – Spark LogisticRegression + Word2Vec
│
├── results/
│ ├── lab5_sklearn_output.txt # Kết quả baseline (TF-IDF)
│ └── lab5_sentiment_output.txt # Kết quả cải tiến (Spark Word2Vec)
│
NLP/ data/
└── sentiments.csv # Dữ liệu dùng cho phần Spark
````
## 3. Cài đặt môi trường

Các thư viện chính gồm:
- `scikit-learn`: huấn luyện Logistic Regression cho mô hình baseline (TF-IDF).
- `pyspark`: xây dựng pipeline và mô hình cải tiến với Word2Vec.
- `pandas`, `numpy`: xử lý và thao tác dữ liệu.
- `re`, `os`: tiền xử lý văn bản và quản lý file.

## 4. Hướng dẫn chạy

Các script sẽ tự động tạo thư mục `results/` và lưu kết quả đầu ra vào đó.

1.  **Chạy mô hình Baseline (Task 1-2):**
    Script này chạy mô hình `LogisticRegression` của scikit-learn với `TfidfVectorizer`.
    ```bash
    python test/lab5_test.py
    ```
    * **Kết quả:** Sẽ được lưu tại `results/lab5_sklearn_output.txt`.

2.  **Chạy mô hình Cải tiến (Task 3-4):**
    Script này chạy pipeline PySpark sử dụng `Word2Vec` và `LogisticRegression` trên bộ dữ liệu `sentiments.csv`.
    ```bash
    python test/lab5_spark_improvement_test.py
    ```
    * **Kết quả:** Sẽ được lưu tại `results/lab5_sentiment_output.txt`.

---

## 5. Báo cáo và Phân tích

### 5.1. Giải thích các bước triển khai

#### a. `src/models/text_classifier.py` (Task 1)
File này định nghĩa lớp `TextClassifier` theo yêu cầu:
* `__init__(self, vectorizer)`: Nhận một `vectorizer` (ví dụ: `TfidfVectorizer`).
* `fit(self, texts, labels)`: Huấn luyện mô hình. Bên trong, nó `fit_transform` văn bản bằng `vectorizer` và `fit` dữ liệu bằng `LogisticRegression` của scikit-learn.
* `predict(self, texts)`: Dự đoán nhãn cho văn bản mới, chỉ sử dụng `transform` của `vectorizer`.
* `evaluate(self, y_true, y_pred)`: Tính toán các chỉ số Accuracy, Precision, Recall, và F1-score.

#### b. `test/lab5_test.py` (Task 2)
Đây là script kiểm thử cho mô hình baseline:
1.  Định nghĩa một bộ dữ liệu nhỏ (6 câu).
2.  Sử dụng `train_test_split` để chia dữ liệu (test_size=0.2, 80% train, 20% test).
3.  Khởi tạo `TfidfVectorizer` của scikit-learn.
4.  Khởi tạo, huấn luyện (`.fit()`), và dự đoán (`.predict()`) bằng `TextClassifier`.
5.  Đánh giá và ghi kết quả ra file `results/lab5_sklearn_output.txt`.

#### c. `test/lab5_spark_improvement_test.py` (Pyspark pipeline + cải tiến bằng Word2Vec - Task 3 & 4)
Đây là script chạy pipeline Spark và cũng là thử nghiệm cải tiến mô hình:
1.  **Khởi tạo:** Bắt đầu một `SparkSession`.
2.  **Tải và Tiền xử lý:**
    * Tải dữ liệu từ `data/sentiments.csv`.
    * Thực hiện các bước làm sạch: chuyển sang chữ thường, loại bỏ ký tự đặc biệt, và tách từ (tokenize).
    * Chuyển đổi nhãn `sentiment` từ -1/1 sang 0/1.
3.  **Vector hóa (Cải tiến):**
    * Sử dụng **`Word2Vec`** để chuyển đổi các token (`words`) thành các vector đặc trưng (`features`) có kích thước 100. Đây là kỹ thuật cải tiến so với TF-IDF, vì `Word2Vec` có khả năng nắm bắt ngữ nghĩa của từ.
4.  **Huấn luyện và Đánh giá:**
    * Chia dữ liệu thành 80% train và 20% test.
    * Huấn luyện mô hình `LogisticRegression` của Spark ML.
    * Sử dụng `MulticlassClassificationEvaluator` để tính toán `accuracy` và `f1`.
    * Ghi kết quả ra file `results/lab5_sentiment_output.txt`.

### 5.2. Phân tích kết quả (Result Analysis)

Dưới đây là bảng so sánh hiệu suất giữa hai mô hình, dựa trên các file kết quả.

#### Bảng so sánh hiệu suất

| Chỉ số (Metric) | Mô hình Baseline (TF-IDF + Sklearn) | Mô hình Cải tiến (Word2Vec + Spark) |
| :--- |:-----------------------------------:|:-----------------------------------:|
| **Accuracy** |               0.5000                |             **0.6979**              |
| **F1-score** |               0.6667                |             **0.6800**              |


---

#### Phân tích

1. **Mô hình Baseline (TF-IDF + Logistic Regression)**  
   Mô hình được huấn luyện trên tập dữ liệu rất nhỏ (6 mẫu, trong đó 4 train và 2 test).  
   Kết quả cho thấy chỉ dự đoán đúng một nửa mẫu kiểm thử, với **Accuracy = 0.50** và **F1 = 0.67**.  
   Do dữ liệu quá ít, kết quả này chỉ mang tính minh họa, chưa thể đánh giá đúng hiệu suất thực tế.

2. **Mô hình Cải tiến (Spark + Word2Vec + Logistic Regression)**  
   Mô hình được huấn luyện trên tập dữ liệu lớn hơn nhiều (≈ 5.8k mẫu), nên kết quả đáng tin cậy hơn.  
   Kết quả đạt **Accuracy = 0.6979** và **F1 = 0.6800**.  
   Sự cải thiện đến từ việc sử dụng **Word2Vec** – kỹ thuật biểu diễn từ dạng vector dense, giúp mô hình học được mối quan hệ ngữ nghĩa giữa các từ.  
   So với TF-IDF (chỉ dựa vào tần suất xuất hiện từ), Word2Vec thể hiện tốt hơn ở khả năng tổng quát hóa và nắm bắt ngữ cảnh.

3. **Kết luận so sánh**  
   Mặc dù chênh lệch F1-score giữa hai mô hình không lớn (0.667 → 0.680),  
   nhưng mô hình cải tiến (Word2Vec + Spark) vượt trội hơn rõ rệt nhờ:
    - Huấn luyện trên dữ liệu thực tế và quy mô lớn.
    - Vector đặc trưng giàu ngữ nghĩa hơn.
    - Pipeline Spark có khả năng mở rộng tốt hơn cho các bài toán lớn.

---

### 5.3. Thách thức và Giải pháp

- **Hiểu cấu trúc Pipeline của Spark ML:**  
  Không giống scikit-learn (xử lý tuần tự), Spark ML sử dụng khái niệm *Pipeline* gồm nhiều *stages* như `Tokenizer`, `Word2Vec`, `LogisticRegression`.  
  → *Giải pháp:* Nghiên cứu tài liệu chính thức của Spark ML để hiểu cách dữ liệu được truyền qua các cột `inputCol` và `outputCol`, đảm bảo pipeline hoạt động trơn tru từ đầu đến cuối.

- **Lỗi import module 'src':**  
  Khi chạy file test trực tiếp, Python không tìm thấy module `src`.  
  → *Giải pháp:* thêm đoạn `sys.path.insert(...)` vào đầu script để thêm thư mục gốc vào đường dẫn tìm kiếm.

### 5.4. Tài liệu tham khảo

* Tài liệu chính thức của [Scikit-learn](https://scikit-learn.org/stable/documentation.html).
* Tài liệu chính thức của [Apache Spark MLlib](https://spark.apache.org/docs/latest/ml-guide.html).
