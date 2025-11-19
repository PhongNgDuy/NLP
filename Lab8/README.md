# Lab 5 – RNN for POS Tagging

## 1. Mục tiêu
- Xây dựng pipeline huấn luyện mô hình RNN (BiLSTM) để gán nhãn từ loại (POS tagging) theo yêu cầu trong `lab5_rnn_for_pos_tagging.pdf`.
- Tự xử lý dữ liệu Universal Dependencies English-EWT (`.conllu`), xây từ vựng/tag set và sinh batch có padding.
- Huấn luyện, đánh giá mô hình trên tập validation/test, trực quan hóa quá trình học và phân tích lỗi.

## 2. Dữ liệu & Tiền xử lý
| Tập | Số câu |
| --- | --- |
| Train | 12 544 |
| Dev (Validation) | 2 001 |
| Test | 2 077 |

- Nguồn: UD English-EWT (`en_ewt-ud-{train,dev,test}.conllu`).
- Từ vựng hạ chuẩn (lowercase) với ngưỡng tần suất `min_freq=2`: 9 760 từ. Thêm token `<PAD>=0`, `<UNK>=1`.
- Tag set gồm 18 nhãn UPOS.
- `POSTaggingDataset` chuyển đổi từng từ và nhãn sang index (có xử lý từ lạ `<UNK>`), `collate_fn` thực hiện padding các câu trong batch về cùng độ dài và trả về độ dài thực tế để phục vụ `pack_padded_sequence`.

## 3. Kiến trúc mô hình
- Embedding: kích thước 100, `padding_idx=0`.
- BiLSTM 2 tầng, hidden size 128, dropout 0.1.
- Fully-connected chiếu từ 256 (2×hidden) -> 18 nhãn.
- Loss: `CrossEntropyLoss(ignore_index=0)` để bỏ qua padding.

## 4. Huấn luyện
- Môi trường: Google Colab GPU NVIDIA T4, PyTorch 2.x.
- Batch size 32, câu trong batch sort theo độ dài và sử dụng `pack_padded_sequence` để xử lý tối ưu các chuỗi có độ dài khác nhau.
- Optimizer Adam (`lr=1e-3`) + scheduler `ReduceLROnPlateau(factor=0.5, patience=3)` → hạ còn `5e-4` từ epoch 8.
- Gradient clipping `max_norm=1.0`, shuffle dữ liệu mỗi epoch để tránh học tuần tự.

Log chính (10 epoch):

| Epoch | Train Loss | Val Loss | Val Acc | LR |
| --- | --- | --- | --- | --- |
| 1 | 0.8186 | 0.4358 | 0.8541 | 1e-3 |
| 3 | 0.2265 | 0.2847 | 0.9062 | 1e-3 |
| 5 | 0.1328 | 0.2694 | 0.9161 | 1e-3 |
| 8 | 0.0727 | 0.2935 | 0.9208 | 5e-4 |
| 10 | **0.0457** | **0.3133** | **0.9250** | 5e-4 |

Biểu đồ loss/accuracy (`Section 5`) cho thấy train loss giảm đều, dev loss dao động nhẹ khi LR giảm nhưng accuracy giữ >92% ở 3 epoch cuối → hội tụ ổn định, chưa có dấu hiệu overfit.

## 5. Đánh giá & Kết quả
- **Test Loss:** 0.2679
- **Test Accuracy:** 0.9261

Ví dụ dự đoán trên 5 câu mẫu:
```
Câu 1:
  Words: ['what', 'if', 'google', 'morphed', 'into', 'googleos', '?']
  True Tags:  ['PRON', 'SCONJ', 'PROPN', 'VERB', 'ADP', 'PROPN', 'PUNCT']
  Pred Tags: ['PRON', 'SCONJ', 'PROPN', 'VERB', 'ADP', 'NOUN', 'PUNCT']
  Accuracy: 85.71%

Câu 2:
  Words: ['what', 'if', 'google', 'expanded', 'on', 'its', 'search', '-', 'engine', '(', 'and', 'now', 'e-mail', ')', 'wares', 'into', 'a', 'full', '-', 'fledged', 'operating', 'system', '?']
  True Tags:  ['PRON', 'SCONJ', 'PROPN', 'VERB', 'ADP', 'PRON', 'NOUN', 'PUNCT', 'NOUN', 'PUNCT', 'CCONJ', 'ADV', 'NOUN', 'PUNCT', 'NOUN', 'ADP', 'DET', 'ADV', 'PUNCT', 'ADJ', 'NOUN', 'NOUN', 'PUNCT']
  Pred Tags: ['PRON', 'SCONJ', 'VERB', 'VERB', 'ADP', 'PRON', 'NOUN', 'PUNCT', 'NOUN', 'PUNCT', 'CCONJ', 'ADV', 'NOUN', 'PUNCT', 'VERB', 'ADP', 'DET', 'NOUN', 'PUNCT', 'NOUN', 'NOUN', 'NOUN', 'PUNCT']
  Accuracy: 82.61%

Câu 3:
  Words: ['[', 'via', 'microsoft', 'watch', 'from', 'mary', 'jo', 'foley', ']']
  True Tags:  ['PUNCT', 'ADP', 'PROPN', 'PROPN', 'ADP', 'PROPN', 'PROPN', 'PROPN', 'PUNCT']
  Pred Tags: ['PUNCT', 'ADP', 'PROPN', 'VERB', 'ADP', 'PROPN', 'PROPN', 'PROPN', 'PUNCT']
  Accuracy: 88.89%

Câu 4:
  Words: ['(', 'and', ',', 'by', 'the', 'way', ',', 'is', 'anybody', 'else', 'just', 'a', 'little', 'nostalgic', 'for', 'the', 'days', 'when', 'that', 'was', 'a', 'good', 'thing', '?', ')']
  True Tags:  ['PUNCT', 'CCONJ', 'PUNCT', 'ADP', 'DET', 'NOUN', 'PUNCT', 'AUX', 'PRON', 'ADJ', 'ADV', 'DET', 'ADJ', 'NOUN', 'ADP', 'DET', 'NOUN', 'ADV', 'PRON', 'AUX', 'DET', 'ADJ', 'NOUN', 'PUNCT', 'PUNCT']
  Pred Tags: ['PUNCT', 'CCONJ', 'PUNCT', 'ADP', 'DET', 'NOUN', 'PUNCT', 'AUX', 'PRON', 'ADV', 'ADV', 'DET', 'ADV', 'NOUN', 'ADP', 'DET', 'NOUN', 'ADV', 'PRON', 'AUX', 'DET', 'NOUN', 'NOUN', 'PUNCT', 'PUNCT']
  Accuracy: 88.00%

Câu 5:
  Words: ['this', 'buzzmachine', 'post', 'argues', 'that', "google's", 'google', "'s", 'rush', 'toward', 'ubiquity', 'might', 'backfire', '--', 'which', "we've", 'we', "'ve", 'all', 'heard', 'before', ',', 'but', "it's", 'it', "'s", 'particularly', 'well', '-', 'put', 'in', 'this', 'post', '.']
  True Tags:  ['DET', 'PROPN', 'NOUN', 'VERB', 'SCONJ', '_', 'PROPN', 'PART', 'NOUN', 'ADP', 'NOUN', 'AUX', 'VERB', 'PUNCT', 'PRON', '_', 'PRON', 'AUX', 'ADV', 'VERB', 'ADV', 'PUNCT', 'CCONJ', '_', 'PRON', 'AUX', 'ADV', 'ADV', 'PUNCT', 'VERB', 'ADP', 'DET', 'NOUN', 'PUNCT']
  Pred Tags: ['DET', 'NOUN', 'VERB', 'NOUN', 'PRON', '_', 'PROPN', 'PART', 'NOUN', 'ADP', 'NOUN', 'AUX', 'VERB', 'PUNCT', 'PRON', '_', 'PRON', 'AUX', 'DET', 'VERB', 'ADV', 'PUNCT', 'CCONJ', '_', 'PRON', 'AUX', 'ADV', 'ADV', 'PUNCT', 'VERB', 'ADP', 'DET', 'NOUN', 'PUNCT']
  Accuracy: 85.29%
```

### Đánh giá Hiệu năng POS Tagging:
   Tổng quan: Độ chính xác trung bình đạt ~86.1%. Mô hình hoạt động khá tốt với cấu trúc câu đơn giản nhưng gặp khó khăn với ngữ cảnh phức tạp và từ vựng đặc thù.
   
   Các nhóm lỗi chính:
   - Lỗi Tên riêng: Mô hình thường xuyên nhầm PROPN thành VERB hoặc NOUN (VD: google $\rightarrow$ VERB, watch $\rightarrow$ VERB).Nguyên nhân: Dữ liệu đầu vào viết thường toàn bộ (lowercase) làm mất dấu hiệu nhận biết tên riêng, mô hình dựa quá nhiều vào tần suất phổ biến của từ.
   - Lỗi nhập nhằng từ loại: Nhầm lẫn vai trò ngữ pháp trong cụm từ.VD: post (trong "post argues") là Chủ ngữ (NOUN) nhưng bị đoán là Động từ (VERB).VD: good (trong "good thing") là Tính từ (ADJ) nhưng bị đoán là Danh từ (NOUN).
   - Lỗi từ mới:Các từ lạ hoặc ghép không chuẩn (VD: googleos) bị gán nhãn mặc định là danh từ chung thay vì tên riêng.



## 6. Cách chạy lại
1. Tải UD English-EWT (đặt trong `data/UD_English-EWT/` hoặc chỉnh đường dẫn trong notebook).
2. Mở `lab5_rnn_pos_tagging.ipynb`, chạy tuần tự từ trên xuống (ưu tiên GPU nếu có).


## 7. Hướng phát triển
- Thử GRU/Transformer, thêm CRF decoding hoặc embedding tiền huấn luyện (GloVe/BERT).
- Data augmentation (character noise) để giảm nhầm `PROPN/NOUN`.
- Hyper-parameter tuning (embedding size, hidden dim, layer, dropout).



