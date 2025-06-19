from flask import Flask, request, render_template, send_file, flash
import os
from utils import des_decrypt, verify_signature, sha512_hash, rsa_decrypt, load_rsa_private_key, load_rsa_public_key
import base64
import json



app = Flask(__name__)
app.secret_key = 'supersecretkey'
folder_receiver = 'Img_Receiver'
file_count =len([f for f in os.listdir(folder_receiver) if os.path.isfile(os.path.join(folder_receiver, f))])
OUTPUT = f'Img_Receiver/received_photo{file_count + 1}.jpg'

@app.route('/receive', methods=['POST'])
def receive():
    try:
        data = request.get_json()
        RECEIVER_PRIV = 'receiver_private.pem'
        SENDER_PUB = 'sender_public.pem'
        private_key = load_rsa_private_key(RECEIVER_PRIV)
        sender_pub = load_rsa_public_key(SENDER_PUB)
        metadata = base64.b64decode(data['metadata'])
        enc_session_key = base64.b64decode(data['enc_session_key'])
        iv = base64.b64decode(data['iv'])
        cipher = base64.b64decode(data['cipher'])
        hash_val = data['hash']
        sig = base64.b64decode(data['sig'])
        session_key = rsa_decrypt(private_key, enc_session_key)
        if sha512_hash(iv + cipher) != hash_val:
            return 'Lỗi kiểm tra toàn vẹn!', 400
        if not verify_signature(sender_pub, metadata, sig):
            return 'Lỗi kiểm tra chữ ký!', 400
        img_data = des_decrypt(session_key, iv, cipher)
        with open(OUTPUT, 'wb') as f:
            f.write(img_data)
        return 'OK', 200
    except Exception as e:
        return f'Lỗi: {e}', 400

@app.route('/', methods=['GET'])
def index():
    img_exists = os.path.exists(OUTPUT)
    return render_template('receiver.html', img_exists=img_exists)

@app.route('/show')
def show():
    if os.path.exists(OUTPUT):
        return send_file(OUTPUT, mimetype='image/jpeg')
    return 'Chưa có ảnh nhận được!', 404

def run_flask():
    app.run(host='127.0.0.1', port=5001, debug=True, use_reloader=False)

if __name__ == '__main__':
    run_flask()
    app.run(port=5001)
