# sender.py
# Người gửi: gửi ảnh có watermark, mã hóa DES, ký số RSA, kiểm tra toàn vẹn SHA-512

import socket
import json
import base64
import time
from utils import add_watermark, des_encrypt, sign_data, sha512_hash, generate_rsa_keypair, rsa_encrypt, save_rsa_keypair, load_rsa_private_key, load_rsa_public_key
from Crypto.Random import get_random_bytes
import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import threading

# Cấu hình
HOST = '127.0.0.1'
PORT = 65432
PHOTO = 'photo.jpg'
WATERMARKED = 'photo_watermarked.jpg'
WATERMARK_TEXT = 'Copyright 2025'

# Đường dẫn khóa
SENDER_PRIV = 'sender_private.pem'
SENDER_PUB = 'sender_public.pem'
RECEIVER_PUB = 'receiver_public.pem'

# Sinh hoặc load khóa RSA
if not (os.path.exists(SENDER_PRIV) and os.path.exists(SENDER_PUB)):
    priv, pub = generate_rsa_keypair()
    save_rsa_keypair(priv, pub, SENDER_PRIV, SENDER_PUB)
private_key = load_rsa_private_key(SENDER_PRIV)
public_key = load_rsa_public_key(SENDER_PUB)
receiver_pub = load_rsa_public_key(RECEIVER_PUB)

def send_image_with_watermark(photo_path, watermark_text):
    HOST = '127.0.0.1'
    PORT = 65432
    SENDER_PRIV = 'sender_private.pem'
    RECEIVER_PUB = 'receiver_public.pem'
    WATERMARKED = 'photo_watermarked.jpg'

    private_key = load_rsa_private_key(SENDER_PRIV)
    receiver_pub = load_rsa_public_key(RECEIVER_PUB)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b'Hello!')
        if s.recv(1024) != b'Ready!':
            return "Receiver không sẵn sàng!"
        timestamp = str(int(time.time()))
        metadata = f'{os.path.basename(photo_path)}|{timestamp}|{watermark_text}'.encode()
        sig = sign_data(private_key, metadata)
        session_key = get_random_bytes(8)
        enc_session_key = rsa_encrypt(receiver_pub, session_key)
        add_watermark(photo_path, WATERMARKED, watermark_text)
        with open(WATERMARKED, 'rb') as f:
            img_data = f.read()
        iv = get_random_bytes(8)
        cipher = des_encrypt(session_key, iv, img_data)
        hash_val = sha512_hash(iv + cipher)
        packet = {
            'metadata': base64.b64encode(metadata).decode(),
            'enc_session_key': base64.b64encode(enc_session_key).decode(),
            'iv': base64.b64encode(iv).decode(),
            'cipher': base64.b64encode(cipher).decode(),
            'hash': hash_val,
            'sig': base64.b64encode(sig).decode()
        }
        s.sendall(json.dumps(packet).encode())
        s.shutdown(socket.SHUT_WR)
        resp = s.recv(1024)
        if resp.startswith(b'ACK'):
            return "Gửi thành công!"
        else:
            return f"Lỗi: {resp.decode()}"

def browse_file():
    filename = filedialog.askopenfilename(filetypes=[("JPEG files", "*.jpg;*.jpeg"), ("All files", "*.*")])
    if filename:
        entry_file.delete(0, tk.END)
        entry_file.insert(0, filename)

def send_action():
    img_path = entry_file.get()
    watermark = entry_watermark.get()
    if not os.path.isfile(img_path):
        messagebox.showerror("Lỗi", "Chọn file ảnh hợp lệ!")
        return
    if not watermark:
        messagebox.showerror("Lỗi", "Nhập watermark!")
        return
    btn_send.config(state=tk.DISABLED)
    chat_box.insert(tk.END, f"Bạn: Đang gửi ảnh '{os.path.basename(img_path)}' với watermark '{watermark}'...\n")
    chat_box.see(tk.END)
    def run():
        try:
            result = send_image_with_watermark(img_path, watermark)
            chat_box.insert(tk.END, f"Bạn: {result}\n")
            chat_box.see(tk.END)
        except Exception as e:
            chat_box.insert(tk.END, f"Bạn: Lỗi: {e}\n")
            chat_box.see(tk.END)
        btn_send.config(state=tk.NORMAL)
    threading.Thread(target=run).start()

root = tk.Tk()
root.title("Sender Chat Box")

chat_box = scrolledtext.ScrolledText(root, width=60, height=15, state='normal')
chat_box.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

tk.Label(root, text="Chọn file ảnh:").grid(row=1, column=0, sticky="e")
entry_file = tk.Entry(root, width=30)
entry_file.grid(row=1, column=1)
tk.Button(root, text="Browse", command=browse_file).grid(row=1, column=2)

tk.Label(root, text="Watermark:").grid(row=2, column=0, sticky="e")
entry_watermark = tk.Entry(root, width=30)
entry_watermark.grid(row=2, column=1, columnspan=2)

btn_send = tk.Button(root, text="Gửi", command=send_action)
btn_send.grid(row=3, column=1, pady=10)

root.mainloop()
