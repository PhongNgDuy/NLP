# Báo Cáo Bài Tập: Pipeline Xử Lý Ngôn Ngữ Tự Nhiên (NLP) Sử Dụng Apache Spark

## 1. Các Bước Triển Khai

Pipeline được xây dựng bằng Scala và Spark MLlib với các bước sau:

1. **Khởi tạo Spark Session**:
   - Tạo phiên Spark với cấu hình `local[*]` để sử dụng toàn bộ lõi CPU cục bộ.
   - Đặt tên ứng dụng là "NLP Pipeline Example" để theo dõi trên Spark UI.

2. **Đọc Dữ Liệu**:
   - Đọc tệp JSON từ đường dẫn `D:/NLP/data/c4-train.00000-of-01024-30K.json.gz`.
   - Giới hạn 1000 bản ghi để tăng tốc xử lý trong môi trường thử nghiệm.

3. **Xây Dựng Pipeline**:
   - **Phân tách từ (RegexTokenizer)**: Chia văn bản thành token bằng pattern `\\s+|[.,;!?()\"']` để tách dựa trên khoảng trắng và dấu câu.
   - **Loại bỏ từ dừng (StopWordsRemover)**: Loại bỏ từ dừng (stop words) như "the", "is" để giảm nhiễu.
   - **Tần suất từ (HashingTF)**: Chuyển token thành vector tần suất từ với kích thước đặc trưng 20,000.
   - **Trọng số IDF (IDF)**: Áp dụng IDF để tính trọng số từ dựa trên mức độ quan trọng trong tập dữ liệu.

4. **Huấn luyện và Chuyển đổi Dữ liệu**:
   - Huấn luyện pipeline bằng `pipeline.fit` trên dữ liệu đầu vào.
   - Chuyển đổi dữ liệu để tạo vector TF-IDF, lưu trữ kết quả vào bộ nhớ cache.

5. **Tính Kích Thước Từ Vựng**:
   - Tính số từ duy nhất sau xử lý bằng `explode` và `distinct` trên cột `filtered_tokens`.

6. **Lưu Kết Quả**:
   - Ghi số liệu hiệu suất (thời gian huấn luyện, chuyển đổi, kích thước từ vựng) vào `../log/lab17_metrics.log`.
   - Ghi 20 bản ghi đầu tiên (văn bản gốc và vector TF-IDF) vào `../results/lab17_pipeline_output.txt`.

7. **Dừng Spark Session**:
   - Dừng phiên Spark để giải phóng tài nguyên.

## 2. Cách Chạy Mã Nguồn và Ghi Log Kết Quả

### Yêu Cầu
- **Môi trường**: Scala 2.12.x, Apache Spark 3.5.0, Java 21.0.1.
- **Thư viện**: Các thư viện `spark-core`, `spark-sql`, `spark-mllib` đã được cấu hình sẵn trong môi trường dự án.
- **Dữ liệu**: Tệp `c4-train.00000-of-01024-30K.json.gz` trong thư mục `D:/NLP/data/`.

### Hướng Dẫn Chạy
1. **Kiểm tra môi trường**:
   - Đảm bảo các thư viện Spark cần thiết đã được cấu hình trong dự án (sử dụng `build.sbt` - môi trường đã được thiết lập sẵn).

2. **Chạy mã**:
   - Trong thư mục dự án (`D:\NLP\Lab2\spark_labs`), sử dụng lệnh:
     ```bash
     sbt run 2>&1 | findstr /V "\[error\]"
     ```
   - Lệnh này chạy chương trình và lọc bỏ các thông báo `[error]` trong đầu ra để dễ đọc hơn.

3. **Theo dõi**:
   - Truy cập `http://localhost:4040` để xem Spark UI trong khi chạy (mã tạm dừng 10 giây để kiểm tra).
   - Kết quả được lưu trong:
     - `../log/lab17_metrics.log`: Số liệu hiệu suất.
     - `../results/lab17_pipeline_output.txt`: Kết quả dữ liệu.

### Log Kết Quả
- **Tệp Log Hiệu Suất** (`lab17_metrics.log`):
  - Ghi thời gian huấn luyện, chuyển đổi, kích thước từ vựng, và thông tin va chạm hash.
  - Nội dung thực tế:
    ```
    --- Performance Metrics ---
    Pipeline fitting duration: 2.58 seconds
    Data transformation duration: 0.91 seconds
    Actual vocabulary size (after preprocessing): 31355 unique terms
    HashingTF numFeatures set to: 20000
    Note: numFeatures (20000) is smaller than actual vocabulary size (31355). Hash collisions are expected.
    ...
    ```

- **Tệp Kết Quả** (`lab17_pipeline_output.txt`):
  - Ghi 20 bản ghi với văn bản gốc (cắt ngắn 100 ký tự) và vector TF-IDF.
  - Ví dụ:
    ```
    ================================================================================
    Original Text: Beginners BBQ Class Taking Place in Missoula!...
    TF-IDF Vector: (20000,[264,298,673,717,829,1271,...],[0.231,0.456,...])
    ================================================================================
    ```

## 3. Giải Thích Kết Quả

### Kết Quả Thu Được
- **Vector TF-IDF**:
  - Cột `features` chứa vector thưa với kích thước 20,000, biểu diễn trọng số TF-IDF của các từ. Ví dụ:
    ```
    (20000,[264,298,673,717,829,...],[0.231,0.456,...])
    ```
    - Chỉ số (index) như 264, 298 là vị trí của từ sau khi ánh xạ qua HashingTF.
    - Giá trị như 0.231, 0.456 là trọng số TF-IDF, cho thấy tầm quan trọng của từ trong tài liệu so với tập dữ liệu.

- **Hiệu Suất**:
  - **Thời gian huấn luyện**: 2.58 giây để fit pipeline trên 1000 bản ghi.
  - **Thời gian chuyển đổi**: 0.91 giây để tạo vector TF-IDF cho 1000 bản ghi.
  - **Kích thước từ vựng**: 31,355 từ duy nhất, lớn hơn `numFeatures` (20,000), dẫn đến va chạm hash nhưng không ảnh hưởng nghiêm trọng.

- **Mẫu dữ liệu**:
  - Dữ liệu đầu vào gồm các văn bản như quảng cáo BBQ, bài đăng diễn đàn, mô tả sản phẩm. Sau xử lý, chúng được chuyển thành vector TF-IDF, phù hợp cho các tác vụ như phân loại hoặc tìm kiếm.

### Phân Tích
- Pipeline xử lý 1000 bản ghi trong khoảng 3.5 giây, cho thấy hiệu suất tốt trên môi trường cục bộ.
- Kích thước từ vựng 31,355 cho thấy tập dữ liệu có từ vựng phong phú. Va chạm hash xảy ra do `numFeatures` nhỏ hơn, nhưng IDF giúp duy trì chất lượng biểu diễn.
- Kết quả TF-IDF có thể dùng cho các tác vụ như phân cụm hoặc phân loại văn bản.

## 4. Khó Khăn Gặp Phải và Giải Pháp

1. **Nhiều thông báo lỗi trong đầu ra**:
   - **Vấn đề**: Đầu ra của `sbt run` chứa nhiều thông báo `[error]` không liên quan, gây khó đọc.
   - **Giải pháp**: Sử dụng lệnh `sbt run 2>&1 | findstr /V "\[error\]"` để lọc bỏ thông báo lỗi, chỉ hiển thị thông tin hữu ích.


2. **Va chạm hash trong HashingTF**:
   - **Vấn đề**: Kích thước từ vựng (31,355) lớn hơn `numFeatures` (20,000), gây va chạm hash.
   - **Giải pháp**: Tăng `numFeatures` (ví dụ: 50,000) hoặc thử `CountVectorizer`:
     ```scala
     import org.apache.spark.ml.feature.CountVectorizer
     val countVectorizer = new CountVectorizer()
       .setInputCol("filtered_tokens")
       .setOutputCol("raw_features")
       .setVocabSize(50000)
     ```

4. **Hiệu suất với dữ liệu lớn**:
   - **Vấn đề**: Xử lý toàn bộ tập dữ liệu có thể chậm.
   - **Giải pháp**: Tiếp tục sử dụng `cache()` và giới hạn 1000 bản ghi trong thử nghiệm. Với dữ liệu lớn, cân nhắc chạy trên cụm Spark.

## 5. Tham Khảo

- Có sử dụng hỗ trợ của Grok chatbot
- Apache Spark MLlib Guide: https://spark.apache.org/docs/latest/ml-guide.html
- Spark SQL, DataFrames Guide: https://spark.apache.org/docs/latest/sql-programming-guide.html
- Scala Documentation: https://www.scala-lang.org/documentation/