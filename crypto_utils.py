import base64
import hashlib
from cryptography.fernet import Fernet

# 生成密钥
def generate_key(master_password):
    hash = hashlib.sha256(master_password.encode('utf-8')).digest()
    return base64.urlsafe_b64encode(hash[:32])

# 加密数据
def encrypt_data(data, key):
    f = Fernet(key)
    return f.encrypt(data.encode('utf-8')).decode('utf-8')

# 解密数据
def decrypt_data(data, key):
    f = Fernet(key)
    return f.decrypt(data.encode('utf-8')).decode('utf-8')
