# receiver.py
# Người nhận: nhận ảnh, kiểm tra hash, chữ ký, giải mã DES, lưu ảnh

import socket
import json
import base64
import os
from utils import des_decrypt, verify_signature, sha512_hash, rsa_decrypt, load_rsa_private_key, load_rsa_public_key
import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading
from PIL import Image, ImageTk

def receive_image():
    HOST = '127.0.0.1'
    PORT = 65432
    OUTPUT = 'received_photo.jpg'
    RECEIVER_PRIV = 'receiver_private.pem'
    SENDER_PUB = 'sender_public.pem'

    private_key = load_rsa_private_key(RECEIVER_PRIV)
    sender_pub = load_rsa_public_key(SENDER_PUB)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        conn, addr = s.accept()
        with conn:
            if conn.recv(1024) != b'Hello!':
                conn.close()
                return "Handshake lỗi!", None
            conn.sendall(b'Ready!')
            packet = b''
            while True:
                part = conn.recv(4096)
                if not part:
                    break
                packet += part
            try:
                data = json.loads(packet.decode())
                metadata = base64.b64decode(data['metadata'])
                enc_session_key = base64.b64decode(data['enc_session_key'])
                iv = base64.b64decode(data['iv'])
                cipher = base64.b64decode(data['cipher'])
                hash_val = data['hash']
                sig = base64.b64decode(data['sig'])
                session_key = rsa_decrypt(private_key, enc_session_key)
                if sha512_hash(iv + cipher) != hash_val:
                    conn.sendall(b'NACK: integrity error')
                    return "Lỗi kiểm tra toàn vẹn!", None
                if not verify_signature(sender_pub, metadata, sig):
                    conn.sendall(b'NACK: signature error')
                    return "Lỗi kiểm tra chữ ký!", None
                img_data = des_decrypt(session_key, iv, cipher)
                with open(OUTPUT, 'wb') as f:
                    f.write(img_data)
                conn.sendall(b'ACK')
                return f"Đã nhận ảnh: {OUTPUT}", OUTPUT
            except Exception as e:
                conn.sendall(b'NACK: error')
                return f"Lỗi: {e}", None

def add_chat_message(msg, img_path=None):
    chat_box.config(state='normal')
    chat_box.insert(tk.END, f"Hệ thống: {msg}\n")
    chat_box.see(tk.END)
    if img_path and os.path.exists(img_path):
        img = Image.open(img_path)
        img.thumbnail((200, 200))
        img_tk = ImageTk.PhotoImage(img)
        img_label = tk.Label(chat_box, image=img_tk)
        img_label.image = img_tk  # giữ tham chiếu
        chat_box.window_create(tk.END, window=img_label)
        chat_box.insert(tk.END, "\n")
        chat_box.see(tk.END)
    chat_box.config(state='disabled')

def receive_image_loop():
    HOST = '127.0.0.1'
    PORT = 65432
    OUTPUT = 'received_photo.jpg'
    RECEIVER_PRIV = 'receiver_private.pem'
    SENDER_PUB = 'sender_public.pem'

    private_key = load_rsa_private_key(RECEIVER_PRIV)
    sender_pub = load_rsa_public_key(SENDER_PUB)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        while True:
            conn, addr = s.accept()
            with conn:
                try:
                    if conn.recv(1024) != b'Hello!':
                        conn.close()
                        add_chat_message("Handshake lỗi!")
                        continue
                    conn.sendall(b'Ready!')
                    packet = b''
                    while True:
                        part = conn.recv(4096)
                        if not part:
                            break
                        packet += part
                    data = json.loads(packet.decode())
                    metadata = base64.b64decode(data['metadata'])
                    enc_session_key = base64.b64decode(data['enc_session_key'])
                    iv = base64.b64decode(data['iv'])
                    cipher = base64.b64decode(data['cipher'])
                    hash_val = data['hash']
                    sig = base64.b64decode(data['sig'])
                    session_key = rsa_decrypt(private_key, enc_session_key)
                    if sha512_hash(iv + cipher) != hash_val:
                        conn.sendall(b'NACK: integrity error')
                        add_chat_message("Lỗi kiểm tra toàn vẹn!")
                        continue
                    if not verify_signature(sender_pub, metadata, sig):
                        conn.sendall(b'NACK: signature error')
                        add_chat_message("Lỗi kiểm tra chữ ký!")
                        continue
                    img_data = des_decrypt(session_key, iv, cipher)
                    with open(OUTPUT, 'wb') as f:
                        f.write(img_data)
                    conn.sendall(b'ACK')
                    add_chat_message(f"Đã nhận ảnh: {OUTPUT}", OUTPUT)
                except Exception as e:
                    conn.sendall(b'NACK: error')
                    add_chat_message(f"Lỗi: {e}")

def receive_action():
    threading.Thread(target=receive_image_loop, daemon=True).start()

def open_image():
    if os.path.exists("received_photo.jpg"):
        os.startfile("received_photo.jpg")
    else:
        messagebox.showerror("Lỗi", "Chưa có ảnh nhận được!")

root = tk.Tk()
root.title("Receiver Chat Box")

chat_box = scrolledtext.ScrolledText(root, width=60, height=20, state='disabled')
chat_box.grid(row=0, column=0, columnspan=2, padx=10, pady=10)


btn_open = tk.Button(root, text="Mở ảnh đã nhận", command=open_image)
btn_open.grid(row=1, column=1, pady=10)

receive_action()

root.mainloop()
