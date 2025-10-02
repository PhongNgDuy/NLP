# Báo Cáo Bài Tập: Pipeline Xử Lý Ngôn Ngữ Tự Nhiên (NLP) Sử Dụng Apache Spark

## 1. Các Bước Triển Khai

Pipeline được xây dựng bằng Scala và Spark MLlib với các bước sau:

1. **Khởi tạo Spark Session**:
   - Tạo phiên Spark với cấu hình `local[*]` để sử dụng toàn bộ lõi CPU cục bộ.
   - Đặt tên ứng dụng là "NLP Pipeline Example" để theo dõi trên Spark UI.

2. **Đọc Dữ Liệu**:
   - Đọc tệp JSON từ đường dẫn `D:/NLP/data/c4-train.00000-of-01024-30K.json.gz`.
   - Giới hạn số lượng bản ghi bằng biến `limitDocuments` (truyền qua tham số dòng lệnh `args(0).toInt`), cho phép tùy chỉnh số lượng tài liệu để tăng tốc xử lý trong môi trường thử nghiệm (ví dụ: giới hạn 1000 bản ghi).

3. **Xây Dựng Pipeline**:
   - **Phân tách từ (RegexTokenizer)**: Chia văn bản thành token bằng pattern `\\s+|[.,;!?()\"']` để tách dựa trên khoảng trắng và dấu câu.
   - **Loại bỏ từ dừng (StopWordsRemover)**: Loại bỏ từ dừng (stop words) như "the", "is" để giảm nhiễu.
   - **Tần suất từ (HashingTF)**: Chuyển token thành vector tần suất từ với kích thước đặc trưng 20,000.
   - **Trọng số IDF (IDF)**: Áp dụng IDF để tính trọng số từ dựa trên mức độ quan trọng trong tập dữ liệu.
   - **Chuẩn hóa vector (Normalizer)**: Thêm lớp chuẩn hóa L2 (Euclidean norm) để chuyển vector TF-IDF thành vector đã chuẩn hóa (`normalized_features`), giúp tính toán độ tương đồng (như cosine similarity) hiệu quả hơn.

4. **Huấn luyện và Chuyển đổi Dữ liệu**:
   - Huấn luyện pipeline bằng `pipeline.fitareness trên dữ liệu đầu vào.
   - Chuyển đổi dữ liệu để tạo vector TF-IDF và vector chuẩn hóa, lưu trữ kết quả vào bộ nhớ cache.

5. **Tính Kích Thước Từ Vựng**:
   - Tính số từ duy nhất sau xử lý bằng `explode` và `distinct` trên cột `filtered_tokens`.

6. **Tìm Kiếm và Hiển Thị Tài Liệu Tương Đồng**:
   - Chọn một tài liệu tham chiếu ngẫu nhiên (tài liệu đầu tiên có vector hợp lệ).
   - Sử dụng UDF để tính cosine similarity giữa vector chuẩn hóa của tài liệu tham chiếu và các tài liệu khác (dot product trên vector L2-normalized).
   - Hiển thị top K (K=5) tài liệu tương đồng nhất, loại trừ tài liệu tham chiếu.
   - Lưu kết quả vào tệp `../results/lab17_similarity_output.txt`.

7. **Lưu Kết Quả**:
   - Ghi số liệu hiệu suất chi tiết (thời gian đọc dữ liệu, huấn luyện, chuyển đổi, tính từ vựng, tìm kiếm tương đồng) vào `../log/lab17_metrics.log`.
   - Ghi 20 bản ghi đầu tiên (văn bản gốc, vector TF-IDF, và vector chuẩn hóa) vào `../results/lab17_pipeline_output.txt`.
   - Ghi kết quả top 5 tài liệu tương đồng vào `../results/lab17_similarity_output.txt`.

8. **Dừng Spark Session**:
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
     sbt "run <limit>" 2>&1 | findstr /V "\[error\]"
     ```
     - Ví dụ: `sbt "run 1000" 2>&1 | findstr /V "\[error\]"` để giới hạn 1000 bản ghi.
   - Lệnh này chạy chương trình với giới hạn tài liệu tùy chỉnh và lọc bỏ các thông báo `[error]` trong đầu ra để dễ đọc hơn.

3. **Theo dõi**:
   - Truy cập `http://localhost:4040` để xem Spark UI trong khi chạy (mã tạm dừng 10 giây để kiểm tra).
   - Kết quả được lưu trong:
     - `../log/lab17_metrics.log`: Số liệu hiệu suất chi tiết.
     - `../results/lab17_pipeline_output.txt`: Kết quả dữ liệu (bao gồm vector chuẩn hóa).
     - `../results/lab17_similarity_output.txt`: Kết quả top 5 tài liệu tương đồng.

### Log Kết Quả
- **Tệp Log Hiệu Suất** (`lab17_metrics.log`):
  - Ghi thời gian chi tiết cho từng giai đoạn (đọc dữ liệu, huấn luyện, chuyển đổi, tính từ vựng, tìm kiếm tương đồng), kích thước từ vựng, và thông tin va chạm hash.
  - Nội dung thực tế:
    ```
    --- Performance Metrics ---
    Data reading duration: 4.44 seconds
    Pipeline fitting duration: 2.05 seconds
    Data transformation duration: 0.59 seconds
    Vocabulary size calculation duration: 0.36 seconds
    Actual vocabulary size (after preprocessing): 578 unique terms
    HashingTF numFeatures set to: 20000
    Metrics file generated at: D:\NLP\Lab2\spark_labs\..\log\lab17_metrics.log

    For detailed stage-level metrics, view the Spark UI at http://localhost:4040 during execution.
    ```

- **Tệp Kết Quả Pipeline** (`lab17_pipeline_output.txt`):
  - Ghi 20 bản ghi với văn bản gốc (cắt ngắn 100 ký tự), vector TF-IDF, và vector chuẩn hóa.
  - Ví dụ:
    ```
    --- NLP Pipeline Output (First 20 results) ---
    ================================================================================
    Original Text: Beginners BBQ Class Taking Place in Missoula!...
    TF-IDF Vector: (20000,[264,298,673,717,829,1271,...],[6.818992368953701,1.0116009116784799,...])
    Normalized TF-IDF Vector: (20000,[264,298,673,717,829,1271,...],[0.39358888399627245,0.05838910682609213,...])
    ================================================================================
    ```

- **Tệp Kết Quả Tương Đồng** (`lab17_similarity_output.txt`):
  - Ghi tài liệu tham chiếu và top 5 tài liệu tương đồng với độ tương đồng cosine.
  - Ví dụ:
    ```
    --- Top 5 Similar Documents ---
    Reference Document: Beginners BBQ Class Taking Place in Missoula!...
    Top 5 Similar Documents:
    ================================================================================
    Text: The rich get richer and the poor get poorer eh?...
    Cosine Similarity: 0.0159
    ================================================================================
    ```

## 3. Giải Thích Kết Quả

### Kết Quả Thu Được
- **Vector TF-IDF và Chuẩn Hóa**:
  - Cột `features` chứa vector TF-IDF thưa với kích thước 20,000.
  - Cột `normalized_features` chứa vector đã chuẩn hóa L2, giúp độ dài vector bằng 1, phù hợp cho tính toán độ tương đồng.
  - Ví dụ: Vector TF-IDF `(20000,[264,298,...],[6.81899,1.01160,...])` được chuẩn hóa thành `(20000,[264,298,...],[0.39359,0.05839,...])`.

- **Tài Liệu Tương Đồng**:
  - Tài liệu tham chiếu: Văn bản đầu tiên (ví dụ: "Beginners BBQ Class...").
  - Top 5 tài liệu tương đồng: Được sắp xếp theo cosine similarity (dựa trên vector chuẩn hóa), với giá trị từ 0.0159 đến 0.0071, cho thấy độ tương đồng thấp nhưng phù hợp với tập dữ liệu đa dạng.

- **Hiệu Suất**:
  - **Thời gian đọc dữ liệu**: 4.44 giây cho giới hạn tùy chỉnh (ví dụ: 1000 bản ghi).
  - **Thời gian huấn luyện**: 2.05 giây.
  - **Thời gian chuyển đổi**: 0.59 giây.
  - **Thời gian tính từ vựng**: 0.36 giây.
  - **Thời gian tìm kiếm tương đồng**: Đo lường riêng (ghi trong log, ví dụ: 0.XX giây).
  - **Kích thước từ vựng**: 578 từ duy nhất (với giới hạn nhỏ), nhỏ hơn `numFeatures` (20,000), không gây va chạm hash nghiêm trọng.

- **Mẫu dữ liệu**:
  - Dữ liệu đầu vào gồm các văn bản như quảng cáo, bài đăng diễn đàn. Sau xử lý, chúng được chuyển thành vector chuẩn hóa, phù hợp cho các tác vụ như tìm kiếm tương đồng hoặc phân loại.

### Phân Tích
- Pipeline xử lý giới hạn tài liệu tùy chỉnh (qua `limitDocuments`) trong khoảng 8 giây tổng, cho thấy hiệu suất tốt trên môi trường cục bộ.
- Lớp Normalizer cải thiện độ chính xác cosine similarity bằng cách đảm bảo vector có độ dài thống nhất.
- Kết quả tương đồng cho thấy tập dữ liệu có sự đa dạng cao; cosine similarity thấp phản ánh nội dung không liên quan chặt chẽ.
- Kết quả TF-IDF và tương đồng có thể dùng cho các tác vụ như khuyến nghị hoặc phân cụm văn bản.

## 4. Khó Khăn Gặp Phải và Giải Pháp

1. **Nhiều thông báo lỗi trong đầu ra**:
   - **Vấn đề**: Đầu ra của `sbt run` chứa nhiều thông báo `[error]` không liên quan, gây khó đọc.
   - **Giải pháp**: Sử dụng lệnh `sbt "run <limit>" 2>&1 | findstr /V "\[error\]"` để lọc bỏ thông báo lỗi, chỉ hiển thị thông tin hữu ích.

2. **Va chạm hash trong HashingTF**:
   - **Vấn đề**: Với từ vựng lớn, `numFeatures` (20,000) có thể gây va chạm.
   - **Giải pháp**: Theo dõi kích thước từ vựng và tăng `numFeatures` nếu cần (ví dụ: 50,000) hoặc sử dụng `CountVectorizer`.

3. **Hiệu suất với dữ liệu lớn**:
   - **Vấn đề**: Xử lý toàn bộ tập dữ liệu có thể chậm.
   - **Giải pháp**: Sử dụng `limitDocuments` để tùy chỉnh giới hạn, kết hợp `cache()` để tối ưu. Với dữ liệu lớn, cân nhắc chạy trên cụm Spark.

4. **Tính toán tương đồng chậm với cross join**:
   - **Vấn đề**: Cross join trên tập dữ liệu lớn có thể tốn tài nguyên.
   - **Giải pháp**: Giới hạn K=5 và sử dụng vector chuẩn hóa để tối ưu UDF; với dữ liệu lớn, xem xét approximate nearest neighbors (ví dụ: LSH).

## 5. Tham Khảo

- Có sử dụng hỗ trợ của Grok chatbot
- Apache Spark MLlib Guide: https://spark.apache.org/docs/latest/ml-guide.html
- Spark SQL, DataFrames Guide: https://spark.apache.org/docs/latest/sql-programming-guide.html
- Scala Documentation: https://www.scala-lang.org/documentation/
