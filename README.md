# 📷 Secure Image Transfer with Watermark

## 🚀 Giới thiệu

**Secure Image Transfer with Watermark** là một hệ thống truyền nhận ảnh an toàn, bảo vệ bản quyền và đảm bảo tính toàn vẹn, xác thực của dữ liệu hình ảnh khi truyền qua mạng. Hệ thống sử dụng các kỹ thuật mã hóa, ký số, kiểm tra toàn vẹn hiện đại, đồng thời cung cấp **giao diện web hiện đại, thân thiện, chuyên nghiệp** cho cả người gửi và người nhận.

---

## 🖼️ Mô tả giao diện chương trình

### **Giao diện gửi ảnh (Sender)**
- **Thiết kế hiện đại, chuyên nghiệp:** Sử dụng màu sắc gradient, icon, bố cục rõ ràng, thân thiện với người dùng.
- **Thanh điều hướng:** Có logo, các liên kết nhanh như Trang chủ, Gán Watermark, Lịch sử watermark.
- **Khu vực tải ảnh:**  
  - Nút tải ảnh lên với icon nổi bật.
  - Hỗ trợ kéo-thả ảnh hoặc chọn từ thiết bị.
  - Có thể nhập watermark trực tiếp.
  - Nút gửi ảnh rõ ràng, dễ thao tác.
- **Ảnh mẫu:** Hiển thị các ảnh mẫu để người dùng thử nghiệm nhanh.
- **Hướng dẫn sử dụng:**  
  - Các bước chèn watermark minh họa bằng hình ảnh và mô tả chi tiết.
- **Thông tin tính năng:**  
  - Các box mô tả tính năng nổi bật như: tùy chỉnh watermark, xử lý hàng loạt, bảo mật, giao diện thân thiện.
- **Footer:**  
  - Thông tin thương hiệu, liên kết hỗ trợ, mạng xã hội, bản quyền.

### **Giao diện nhận ảnh (Receiver)**
- **Hiển thị ảnh nhận được:** Ảnh sẽ được hiển thị trực tiếp trên giao diện sau khi nhận thành công.
- **Nút tải ảnh về:** Cho phép người dùng tải ảnh đã nhận về máy.
- **Thông báo trạng thái:** Hiển thị thông báo khi nhận thành công hoặc có lỗi.
- **Thiết kế đồng bộ với giao diện gửi:** Sử dụng Bootstrap, màu sắc hài hòa, dễ sử dụng.


---

## 🗂️ Cấu trúc dự án

```
BMTT/
│
├── web_sender.py          # Flask app cho giao diện gửi ảnh (web)
├── web_receiver.py        # Flask app cho giao diện nhận ảnh (web)
├── utils.py               # Hàm tiện ích: watermark, mã hóa, ký số, hash
├── templates/
│   ├── sender.html        # Giao diện web gửi ảnh (hiện đại, chuyên nghiệp)
│   └── receiver.html      # Giao diện web nhận ảnh (hiện đại, chuyên nghiệp)
├── static/                # Chứa ảnh, css, js, icon, v.v.
├── sender_private.pem     # Khóa riêng của sender (tự sinh lần đầu)
├── sender_public.pem      # Khóa công khai của sender
├── receiver_private.pem   # Khóa riêng của receiver (tự sinh lần đầu)
├── receiver_public.pem    # Khóa công khai của receiver
├── README.md
└── ...
```

---

## 🛠️ Cài đặt môi trường

**Yêu cầu:**  
- Python 3.7 trở lên

**Cài đặt các thư viện cần thiết:**
```bash
pip install pillow pycryptodome flask requests
```

---

## ⚡ Hướng dẫn sử dụng

### 1. **Khởi tạo khóa RSA**
- Khi chạy lần đầu, chương trình sẽ tự động sinh cặp khóa RSA cho cả sender và receiver.
- Nếu chạy trên hai máy, hãy copy file public key giữa hai bên để xác thực.

### 2. **Chạy chương trình**

#### **Chạy trên cùng một máy (test nội bộ):**
- **Bước 1:** Mở terminal, chạy receiver (máy nhận):
    ```bash
    python web_receiver.py
    ```
    - Mặc định chạy trên `http://localhost:5001`
- **Bước 2:** Mở terminal khác, chạy sender (máy gửi):
    ```bash
    python web_sender.py
    ```
    - Mặc định chạy trên `http://localhost:5000`

#### **Chạy trên hai máy khác nhau (mạng LAN):**
- Máy A chạy `web_receiver.py`, lấy địa chỉ IP nội bộ (ví dụ: `192.168.1.10`).
- Máy B chạy `web_sender.py`, sửa biến `RECEIVER_URL` trong file `web_sender.py` thành:
    ```python
    RECEIVER_URL = 'http://192.168.1.10:5001/receive'
    ```
- Đảm bảo hai máy cùng mạng và không bị chặn bởi firewall.

### 3. **Sử dụng giao diện web**

- **Sender:** Truy cập `http://localhost:5000` trên trình duyệt để gửi ảnh.
    - Chọn ảnh cần gửi.
    - Nhập watermark (chữ sẽ in chéo lên ảnh).
    - Nhấn "Gửi" để truyền ảnh đi.
    - Xem thông báo trạng thái gửi thành công/thất bại.

- **Receiver:** Truy cập `http://localhost:5001` để xem ảnh đã nhận.
    - Ảnh nhận được sẽ hiển thị trực tiếp trên giao diện.
    - Có thể tải ảnh về máy.

- **Chat:**  
    - Nhắn tin realtime, gửi ảnh có watermark trực tiếp trong khung chat.
    - Tin nhắn của mình sẽ nằm bên phải, đối phương bên trái, hiển thị rõ ràng như Facebook Messenger.

---

## 💡 Tính năng nổi bật

- **Watermark chéo:** Bảo vệ bản quyền, chống sao chép ảnh.
- **Mã hóa & xác thực:** Đảm bảo an toàn, toàn vẹn, chống giả mạo.
- **Giao diện web hiện đại:** Sử dụng Bootstrap, gradient, icon, preview ảnh gửi và hiển thị ảnh nhận trực tiếp.
- **Trò chuyện realtime:** Chat hai chiều, gửi ảnh có watermark ngay trong khung chat.
- **Dễ sử dụng:** Chỉ cần trình duyệt, không cần cài đặt thêm phần mềm ngoài Python.
- **Có thể mở rộng:** Hỗ trợ nhiều ảnh, lịch sử gửi/nhận, xác thực nâng cao...

---

## 📸 Demo giao diện

| Giao diện gửi ảnh (Sender) | Giao diện nhận ảnh (Receiver) |
|---------------------------|-------------------------------|----------------|
| ![Sender GUI](assets/sender_gui.png) | ![Receiver GUI](assets/receiver_gui.png) |

> *Bạn có thể thay thế `photo.jpg` bằng bất kỳ ảnh nào bạn muốn gửi.*

---

## 📝 Ghi chú

- Nếu chạy trên 2 máy, hãy copy file public key giữa hai bên.
- Nếu gặp lỗi font khi watermark, hãy cài đặt font `arial.ttf` hoặc chỉnh lại tên font trong `utils.py`.
- Có thể mở rộng thêm các tính năng như: gửi nhiều ảnh, chat, xác thực 2 lớp, lưu lịch sử, v.v.

---

## ❓ Câu hỏi thường gặp

**Q:** Không gửi được ảnh, báo lỗi kết nối?  
**A:** Kiểm tra lại địa chỉ IP, port, firewall và đảm bảo receiver đang chạy trước sender.

**Q:** Ảnh nhận được không có watermark?  
**A:** Kiểm tra lại hàm `add_watermark` trong `utils.py` và font chữ.

**Q:** Muốn mở rộng giao diện hoặc thêm tính năng?  
**A:** Bạn có thể chỉnh sửa file HTML trong thư mục `templates/` hoặc liên hệ nhóm phát triển để được hỗ trợ.

---

## 📧 Liên hệ & đóng góp

Mọi ý kiến đóng góp, vui lòng tạo issue hoặc pull request tại:  
[https://github.com/duytienkaka/ATBMTT](https://github.com/duytienkaka/ATBMTT)

---

**© 2025 - Nhóm Nhập môn An toàn bảo mật thông tin**

**👨‍💻 Thành viên nhóm:**
> **Phạm Đức Duy Tiến**  
> **Nguyễn Quang Thịnh**  
> **Dương Văn Việt**
