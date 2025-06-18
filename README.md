# 📷 Secure Image Transfer with Watermark

## 🚀 Giới thiệu

**Secure Image Transfer with Watermark** là một hệ thống truyền nhận ảnh an toàn, được thiết kế nhằm bảo vệ bản quyền và đảm bảo tính toàn vẹn, xác thực của dữ liệu hình ảnh khi truyền qua mạng. Hệ thống sử dụng các kỹ thuật mã hóa, ký số và kiểm tra toàn vẹn hiện đại, đồng thời cung cấp giao diện web thân thiện, dễ sử dụng cho cả người gửi và người nhận.

**Các công nghệ bảo mật sử dụng:**
- **Mã hóa ảnh:** DES (Data Encryption Standard) – đảm bảo chỉ người nhận hợp lệ mới giải mã được ảnh.
- **Trao đổi khóa & ký số:** RSA 2048-bit (PKCS#1 v1.5 + SHA-512) – xác thực nguồn gửi và bảo vệ khóa phiên.
- **Kiểm tra toàn vẹn:** SHA-512 – phát hiện mọi thay đổi dữ liệu trong quá trình truyền.
- **Bảo vệ bản quyền:** Thêm watermark chéo lên ảnh – chống sao chép, khẳng định quyền sở hữu.

---

## 🗂️ Cấu trúc dự án

```
BMTT/
│
├── web_sender.py          # Flask app cho giao diện gửi ảnh (web)
├── web_receiver.py        # Flask app cho giao diện nhận ảnh (web)
├── utils.py               # Hàm tiện ích: watermark, mã hóa, ký số, hash
├── templates/
│   ├── sender.html        # Giao diện web gửi ảnh (Bootstrap)
│   └── receiver.html      # Giao diện web nhận ảnh (Bootstrap)
├── static/                # (tuỳ chọn) Chứa ảnh, css, js nếu mở rộng
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

---

## 🔒 Quy trình bảo mật

1. **Người gửi (Sender):**
    - Chọn ảnh và nhập watermark.
    - Thêm watermark chéo lên ảnh.
    - Sinh khóa phiên (session key) cho DES.
    - Mã hóa ảnh bằng DES với session key và IV ngẫu nhiên.
    - Ký số metadata (tên file, thời gian, watermark) bằng RSA private key.
    - Mã hóa session key bằng RSA public key của receiver.
    - Tính hash SHA-512 cho IV và ciphertext.
    - Đóng gói tất cả thông tin vào một gói JSON, gửi qua HTTP POST tới receiver.

2. **Người nhận (Receiver):**
    - Nhận gói tin, giải mã session key bằng RSA private key.
    - Kiểm tra hash và xác thực chữ ký.
    - Nếu hợp lệ, giải mã ảnh bằng DES, lưu và hiển thị ảnh.
    - Nếu không hợp lệ, báo lỗi toàn vẹn hoặc chữ ký.

---

## 💡 Tính năng nổi bật

- **Watermark chéo:** Bảo vệ bản quyền, chống sao chép ảnh.
- **Mã hóa & xác thực:** Đảm bảo an toàn, toàn vẹn, chống giả mạo.
- **Giao diện web hiện đại:** Sử dụng Bootstrap, có preview ảnh gửi và hiển thị ảnh nhận trực tiếp.
- **Dễ sử dụng:** Chỉ cần trình duyệt, không cần cài đặt thêm phần mềm ngoài Python.
- **Có thể mở rộng:** Hỗ trợ nhiều ảnh, lịch sử gửi/nhận, chat box, xác thực nâng cao...

---

## 📸 Demo giao diện

| Giao diện gửi ảnh (Sender) | Giao diện nhận ảnh (Receiver) |
|---------------------------|-------------------------------|
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
