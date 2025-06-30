
from Crypto.Cipher import DES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes
import base64
import hashlib
import time

# Thêm watermark vào ảnh
def add_watermark(input_path, output_path, watermark_text):
    from PIL import Image, ImageDraw, ImageFont
 
    image = Image.open(input_path).convert("RGBA")
    watermark_layer = Image.new("RGBA", image.size, (0,0,0,0))
    draw = ImageDraw.Draw(watermark_layer)

    # Chọn font và kích thước phù hợp
    font_size = int(min(image.size) / 10)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()

    # Sử dụng textbbox thay cho textsize
    bbox = draw.textbbox((0, 0), watermark_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Tính toán vị trí để watermark nằm chéo giữa ảnh
    x = (image.width - text_width) // 2
    y = (image.height - text_height) // 2

    # Vẽ watermark chéo (góc 45 độ)
    # Tạo một layer text riêng để xoay
    text_layer = Image.new("RGBA", (text_width, text_height), (0,0,0,0))
    text_draw = ImageDraw.Draw(text_layer)
    text_draw.text((0, 0), watermark_text, font=font, fill=(255, 0, 0, 255))

    rotated_text = text_layer.rotate(45, expand=1)
    # Tính lại vị trí để dán vào giữa ảnh
    rx = (image.width - rotated_text.width) // 2
    ry = (image.height - rotated_text.height) // 2
    watermark_layer.paste(rotated_text, (rx, ry), rotated_text)

    # Kết hợp watermark với ảnh gốc
    watermarked = Image.alpha_composite(image, watermark_layer)
    watermarked = watermarked.convert("RGB")
    watermarked.save(output_path)

# Mã hóa DES
def des_encrypt(key, iv, data):
    cipher = DES.new(key, DES.MODE_CBC, iv)
    pad_len = 8 - len(data) % 8
    data += bytes([pad_len]) * pad_len
    return cipher.encrypt(data)

def des_decrypt(key, iv, data):
    cipher = DES.new(key, DES.MODE_CBC, iv)
    decrypted = cipher.decrypt(data)
    pad_len = decrypted[-1]
    return decrypted[:-pad_len]

# Sinh cặp khóa RSA
def generate_rsa_keypair():
    key = RSA.generate(2048)
    return key, key.publickey()

# Ký số
def sign_data(private_key, data):
    h = SHA512.new(data)
    signature = pkcs1_15.new(private_key).sign(h)
    return signature

# Kiểm tra chữ ký
def verify_signature(public_key, data, signature):
    h = SHA512.new(data)
    try:
        pkcs1_15.new(public_key).verify(h, signature)
        return True
    except (ValueError, TypeError):
        return False

# Hash SHA-512
def sha512_hash(data):
    return hashlib.sha512(data).hexdigest()

# Mã hóa/giải mã RSA

def rsa_encrypt(public_key, data):
    cipher = PKCS1_OAEP.new(public_key)
    return cipher.encrypt(data)

def rsa_decrypt(private_key, data):
    cipher_rsa = PKCS1_OAEP.new(private_key)
    return cipher_rsa.decrypt(data)

def save_rsa_keypair(private_key, public_key, priv_path, pub_path):
    with open(priv_path, 'wb') as f:
        f.write(private_key.export_key('PEM'))
    with open(pub_path, 'wb') as f:
        f.write(public_key.export_key('PEM'))

def load_rsa_private_key(path):
    from Crypto.PublicKey import RSA
    with open(path, 'rb') as f:
        return RSA.import_key(f.read())

def load_rsa_public_key(path):
    from Crypto.PublicKey import RSA
    with open(path, 'rb') as f:
        return RSA.import_key(f.read())
