# Lab 7: RNNs cho Text Classification

## Tổng quan

Lab này thực hiện phân loại intent (ý định) từ văn bản sử dụng các mô hình RNN (Recurrent Neural Networks) và so sánh với các phương pháp baseline. Dataset được sử dụng là HWU (Home Assistant Understanding) với 64 lớp intent khác nhau.

## Cấu trúc file

```
Lab7/
├── rnns_text_classification.ipynb  # Notebook chứa toàn bộ code và experiments
└── README.md  # Labwork report
```

## Chạy code

1. Cài đặt dependencies:
```bash
pip install gensim tensorflow scikit-learn pandas numpy matplotlib
```

2. Chuẩn bị dữ liệu:
   - Giải nén file `hwu.tar.gz` vào thư mục `hwu/`
   - Đảm bảo có các file: `train.csv`, `val.csv`, `test.csv`

3. Chạy notebook:
   - Mở `rnns_text_classification.ipynb` trong Jupyter Notebook hoặc Google Colab
   - Chạy các cells theo thứ tự

---

## Dataset

- **Dataset**: HWU 
- **Số lớp**: 64 intent classes
- **Dữ liệu**:
  - Train: 8,954 mẫu
  - Validation: 1,076 mẫu
  - Test: 1,076 mẫu

Các intent bao gồm:
- `alarm_query`, `alarm_set`, `alarm_remove`
- `play_music`, `play_podcasts`, `play_audiobook`
- `email_query`, `email_sendemail`
- `iot_hue_lighton`, `iot_hue_lightoff`
- `general_affirm`, `general_negate`
- và nhiều intent khác...

## Các mô hình đã thực hiện

### 1. Baseline: TF-IDF + Logistic Regression

**Phương pháp**:
- Sử dụng TF-IDF vectorization với `max_features=5000`
- Classifier: Logistic Regression với `max_iter=1000`

**Kết quả**: 
- **Test Accuracy**: 84.0%
- **Macro Average**: Precision=0.85, Recall=0.83, F1-score=0.84
- **Weighted Average**: Precision=0.84, Recall=0.84, F1-score=0.84
- Nhiều lớp đạt F1-score cao (>0.9) như `general_affirm`, `general_commandstop`, `iot_cleaning`
- Một số lớp khó như `general_quirky` (F1=0.30), `qa_factoid` (F1=0.52), `calendar_query` (F1=0.49) có F1-score thấp hơn

### 2. Word2Vec Average Vectors + Dense Neural Network

**Kiến trúc**:
- Word2Vec embeddings: `vector_size=100`, `window=5`, `min_count=1`
- Chuyển đổi câu thành vector bằng cách lấy trung bình các word vectors
- Neural Network:
  - Dense(128, activation='relu')
  - Dropout(0.2)
  - Dense(64, activation='softmax')

**Hyperparameters**:
- Optimizer: Adam
- Loss: Categorical Crossentropy
- Batch size: 256
- Epochs: 200 (với EarlyStopping, patience=10)
- Callbacks: EarlyStopping (monitor='val_loss')

**Kết quả**: 
- **Epoch 200 (cuối cùng)**:
  - Train Accuracy: 39.36%
  - Validation Accuracy: 39.50%
  - Train Loss: 2.2458
  - Validation Loss: 2.2825
- Mô hình học được nhưng performance thấp hơn baseline do mất thông tin về thứ tự từ trong câu

### 3. LSTM với Pretrained Embeddings (Non-trainable)

**Kiến trúc**:
- Embedding layer: Sử dụng Word2Vec embeddings đã train, `trainable=False`
- LSTM layer: 128 units, dropout=0.2
- Dense output: 64 classes với softmax activation

**Hyperparameters**:
- Max sequence length: 50
- Embedding dimension: 100 (từ Word2Vec)
- Optimizer: Adam
- Batch size: 256
- Epochs: 200 (với EarlyStopping, patience=20)

**Kết quả**: 
- **Epoch 200 (cuối cùng)**:
  - Train Accuracy: 38.93%
  - Validation Accuracy: 40.89%
  - Train Loss: 2.1621
  - Validation Loss: 2.1614
- Mô hình LSTM với embeddings cố định cho thấy khả năng học tốt hơn so với average vectors (tăng ~1.4% validation accuracy)
- Validation accuracy tăng dần qua các epochs từ 2.23% (epoch 1) lên 40.89% (epoch 200)

### 4. LSTM với Pretrained Embeddings (Trainable)

**Kiến trúc**:
- Embedding layer: Sử dụng Word2Vec embeddings đã train, `trainable=True` (fine-tuning)
- LSTM layer: 128 units, dropout=0.3
- Dense output: 64 classes với softmax activation

**Hyperparameters**:
- Max sequence length: 50
- Embedding dimension: 100
- Optimizer: Adam
- Batch size: 256
- Epochs: 200 (với EarlyStopping, patience=10)

**Kết quả**: 
- **Epoch 139 (cuối cùng)**:
  - Train Accuracy: 93.89%
  - Validation Accuracy: 74.91%
  - Train Loss: 0.2373
  - Validation Loss: 1.4383
- Mô hình bắt đầu học từ epoch 27 (val_accuracy tăng từ 0.0177 lên 0.0204)
- Validation accuracy tăng dần và đạt đỉnh ở epoch 137 với 76.02%
- **Nhận xét**: Fine-tuning embeddings cho kết quả tốt nhất trong các mô hình neural network, vượt xa mô hình non-trainable embeddings (tăng ~34% validation accuracy)

## Kỹ thuật xử lý dữ liệu

1. **Label Encoding**: Sử dụng `LabelEncoder` để chuyển đổi intent labels thành số
2. **Text Tokenization**: Sử dụng Keras `Tokenizer` với `oov_token="<UNK>"`
3. **Sequence Padding**: Padding sequences về độ dài cố định (max_len=50) với `padding='post'`
4. **Word Embeddings**: 
   - Train Word2Vec trên training data
   - Tạo embedding matrix cho Keras Embedding layer

## Công cụ và thư viện

- **Python packages**:
  - `pandas`: Xử lý dữ liệu
  - `scikit-learn`: TF-IDF, Logistic Regression, LabelEncoder
  - `gensim`: Word2Vec
  - `tensorflow/keras`: Neural Networks, LSTM, Embeddings
  - `numpy`: Tính toán số học
  - `matplotlib`: Visualization

## So sánh kết quả

| Mô hình | Test/Val Accuracy | F1-score (Macro) | Ghi chú |
|--------|------------------|------------------|---------|
| TF-IDF + Logistic Regression | **84.0%** | 0.84 | Baseline tốt nhất |
| Word2Vec Average + Dense | 39.50% | - | Mất thông tin thứ tự từ |
| LSTM (Non-trainable embeddings) | 40.89% | - | Tốt hơn average vectors |
| LSTM (Trainable embeddings) | **74.91%** | - | Tốt nhất trong các mô hình neural network |

## Kết luận

1. **Baseline (TF-IDF + LR)**: 
    - TF-IDF giúp mô hình tuyến tính dễ dàng phát hiện từ khóa đặc trưng của từng lớp, trong khi Logistic Regression có ít tham số, phù hợp với tập dữ liệu nhỏ và tránh overfitting.

    - Mặc dù không học ngữ cảnh, TF-IDF lại tận dụng rất tốt đặc trưng bề mặt — điều đặc biệt hữu ích trong bài toán có nhiều lớp và số mẫu hạn chế.

2. **Word2Vec Average + Dense**: Đơn giản nhưng mất thông tin về thứ tự từ trong câu, chỉ đạt 39.5% validation accuracy.

3. **LSTM với Pretrained Embeddings (Non-trainable)**: 
   - Mô hình có khả năng học thứ tự và ngữ cảnh, tuy nhiên embeddings cố định không thích ứng với miền dữ liệu cụ thể.
   - Đạt 40.89% validation accuracy, tốt hơn average vectors nhưng vẫn thấp hơn baseline rất nhiều

4. **LSTM với Pretrained Embeddings (Trainable)**: 
   - Fine-tuning embeddings cho kết quả tốt nhất trong các mô hình neural network
   - Mô hình bắt đầu học từ epoch 27 và đạt đỉnh ở epoch 137 (76.02%). Cho thấy việc fine-tuning embeddings có thể cải thiện đáng kể performance so với embeddings cố định
   - Tuy nhiên, do dữ liệu còn hạn chế (chỉ 8k mẫu, 64 lớp), mô hình vẫn chưa thể vượt qua baseline tuyến tính.

## Hướng phát triển

- Thử nghiệm với các kiến trúc RNN khác: GRU, Bidirectional LSTM
- Sử dụng pre-trained embeddings lớn hơn: GloVe, FastText, hoặc transformer-based embeddings
- Tăng độ dài sequence nếu cần
- Tinh chỉnh hyperparameters: learning rate, dropout, LSTM units
- Thử các kỹ thuật regularization khác: batch normalization, layer normalization
- Ensemble các mô hình để cải thiện performance



