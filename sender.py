from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import os
from utils import add_watermark, des_encrypt, sign_data, sha512_hash, load_rsa_private_key, load_rsa_public_key, rsa_encrypt
from Crypto.Random import get_random_bytes
import base64
import json
import time

app = Flask(__name__)
app.secret_key = 'supersecretkey'

RECEIVER_URL = 'https://big-onions-attack.loca.lt/receive'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        photo = request.files['photo']
        watermark = request.form['watermark']
        if not photo or not watermark:
            flash('Vui lòng chọn ảnh và nhập watermark!', 'danger')
            return redirect(url_for('index'))
        photo_path = 'temp_upload.jpg'
        photo.save(photo_path)

        # Xử lý bảo mật như sender.py
        SENDER_PRIV = 'sender_private.pem'
        RECEIVER_PUB = 'receiver_public.pem'
        WATERMARKED = 'photo_watermarked.jpg'
        private_key = load_rsa_private_key(SENDER_PRIV)
        receiver_pub = load_rsa_public_key(RECEIVER_PUB)
        timestamp = str(int(time.time()))
        metadata = f'{os.path.basename(photo_path)}|{timestamp}|{watermark}'.encode()
        sig = sign_data(private_key, metadata)
        session_key = get_random_bytes(8)
        enc_session_key = rsa_encrypt(receiver_pub, session_key)
        add_watermark(photo_path, WATERMARKED, watermark)
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
        # Gửi sang receiver qua HTTP POST
        try:
            resp = requests.post(RECEIVER_URL, json=packet)
            if resp.status_code == 200:
                flash('Gửi thành công!', 'success')
            else:
                flash(f'Lỗi phía nhận: {resp.text}', 'danger')
        except Exception as e:
            flash(f'Lỗi kết nối: {e}', 'danger')
        return redirect(url_for('index'))
    return render_template('sender.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
