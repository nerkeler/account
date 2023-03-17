from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import base64


def generate_key_pair():
    """生成RSA密钥对"""
    key_pair = RSA.generate(2048)
    private_key = key_pair.export_key()
    public_key = key_pair.publickey().export_key()
    return private_key, public_key


def encrypt(public_key, plaintext):
    """RSA加密"""
    key = RSA.import_key(public_key)
    cipher = PKCS1_v1_5.new(key)
    ciphertext = cipher.encrypt(plaintext.encode('utf-8'))
    return base64.b64encode(ciphertext).decode('utf-8')


def decrypt(private_key, ciphertext):
    """RSA解密"""
    key = RSA.import_key(private_key)
    cipher = PKCS1_v1_5.new(key)
    ciphertext = base64.b64decode(ciphertext.encode('utf-8'))
    plaintext = cipher.decrypt(ciphertext, None).decode('utf-8')
    return plaintext


if __name__ == '__main__':
    # 生成RSA密钥对
    private_key, public_key = generate_key_pair()

    # unicode 转str
    print(private_key.decode("utf-8"))
    print(public_key.decode("utf-8"))
    # 加密消息
    message = 'Hello, world!'
    ciphertext = encrypt(public_key, message)
    print('加密后的消息：', ciphertext)
    # 解密消息
    plaintext = decrypt(private_key, ciphertext)
    print('解密后的消息：', plaintext)
