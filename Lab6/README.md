# Lab 5: Làm quen với PyTorch

File notebook thực hành: `pytorch_intro.ipynb`

## 1. Mục tiêu

Bài thực hành này là bước đệm để làm quen với PyTorch, một thư viện Deep Learning phổ biến. Các mục tiêu chính bao gồm:

* Hiểu và thao tác với **Tensor**, cấu trúc dữ liệu cốt lõi của PyTorch.
* Hiểu cách PyTorch tự động tính đạo hàm (gradient) thông qua **autograd**.
* Biết cách xây dựng một mạng nơ-ron đơn giản bằng cách kế thừa lớp `torch.nn.Module`.
* Làm quen với hai lớp cơ bản: `nn.Linear` và `nn.Embedding`.

## 2. Các phần thực hiện

Bài lab được chia thành 3 phần chính.

### Phần 1: Khám phá Tensor

Phần này thực hành các thao tác cơ bản nhất với Tensor:

* **Task 1.1:** Tạo Tensor từ list Python và NumPy array. Sử dụng `torch.ones_like` và `torch.rand_like` để tạo các tensor đặc biệt.
* **Task 1.2:** Thực hiện các phép toán cơ bản: cộng, nhân với vô hướng, và nhân ma trận.
* **Task 1.3:** Thực hành indexing và slicing để truy cập các phần tử của tensor.
* **Task 1.4:** Thay đổi hình dạng tensor bằng `view` hoặc `reshape`.

### Phần 2: Tự động tính Đạo hàm với autograd

Phần này khám phá tính năng tự động tính toán đạo hàm của PyTorch.

* **Task 2.1:** Tạo tensor `x` với `requires_grad=True`.
* Thực hiện các phép toán `y = x + 2` và `z = y * y * 3`.
* Gọi `z.backward()` để tính đạo hàm.
* Kiểm tra kết quả `x.grad`, kết quả trả về là `18` như tính toán lý thuyết (`dz/dx = 6(x+2)`).

### Phần 3: Xây dựng Mô hình đầu tiên với torch.nn

Phần này giới thiệu module `torch.nn` để xây dựng mạng nơ-ron.

* **Task 3.1:** Sử dụng lớp `nn.Linear` để thực hiện phép biến đổi tuyến tính.
* **Task 3.2:** Sử dụng lớp `nn.Embedding` để tạo bảng tra cứu (lookup table) cho các vector từ.
* **Task 3.3:** Định nghĩa một mô hình hoàn chỉnh (`MyFirstModel`) bằng cách kế thừa `nn.Module`. Mô hình này kết hợp `nn.Embedding`, `nn.Linear`, và hàm kích hoạt `nn.ReLU`. Luồng dữ liệu được định nghĩa trong phương thức `forward`.

## 3. Trả lời câu hỏi (Task 2.1)

> **Câu hỏi:** Chuyện gì xảy ra nếu bạn gọi `z.backward()` một lần nữa? Tại sao?

**Trả lời:**

Nếu gọi `z.backward()` một lần nữa ngay sau lần gọi đầu tiên, chương trình sẽ báo lỗi:
```
RuntimeError: Trying to backward through the graph a second time...
```
**Lý do là:**

Theo mặc định, để tiết kiệm bộ nhớ, PyTorch sẽ **tự động giải phóng (xóa) biểu đồ tính toán (computational graph)** ngay sau khi thực hiện xong phép tính `backward()`. Biểu đồ này chứa các thông tin trung gian cần thiết để tính đạo hàm.

Khi gọi `z.backward()` lần thứ hai, biểu đồ đó không còn tồn tại, nên PyTorch không thể tính toán đạo hàm một lần nữa và ném ra lỗi `RuntimeError`.

*Nếu cần giữ lại biểu đồ để thực hiện `backward()` nhiều lần (ví dụ: để tính đạo hàm bậc cao), phải chỉ định rõ điều này ở lần gọi đầu tiên:* `z.backward(retain_graph=True)`.

## 4. Kết quả đạt được
- Hiểu và thực hành thành công với Tensor, autograd, và nn.Module.
- Đã xây dựng mô hình PyTorch (MyModel) chạy đúng.
