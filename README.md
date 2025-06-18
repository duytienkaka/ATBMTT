# Secure Image Transfer with Watermark

## Mô tả
- Gửi ảnh có watermark, mã hóa DES, trao đổi khóa & ký số RSA 2048-bit, kiểm tra toàn vẹn SHA-512.
- Gồm các file: sender.py, receiver.py, utils.py, sample photo.jpg (placeholder).

## Cài đặt thư viện
```bash
pip install pillow pycryptodome
```

## Chạy thử
- Chạy `receiver.py` trước, sau đó chạy `sender.py` để gửi ảnh.

## Lưu ý
- Thay thế `photo.jpg` bằng ảnh thật khi sử dụng.
