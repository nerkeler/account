# -*- coding: utf-8 -*-
import base64
import hashlib
import uuid

from Crypto.Cipher import AES


def aes_decode(key, ciphertext):
    # 将密钥填充到16的倍数
    key = key + (16 - len(key) % 16) * '\0'
    # 创建AES密码器对象
    cipher = AES.new(key.encode(), AES.MODE_ECB)
    # 解码Base64编码的密文
    ciphertext = base64.b64decode(ciphertext)
    # 解密
    plaintext = cipher.decrypt(ciphertext)
    # 去除填充字符
    plaintext = plaintext.rstrip(b'\0')
    return plaintext.decode()


def aes_encode(key, password):
    # 将密钥填充到16的倍数
    key = key + (16 - len(key) % 16) * '\0'
    # 创建AES密码器对象
    cipher = AES.new(key.encode(), AES.MODE_ECB)
    # 将明文填充到16的倍数
    password = password + (16 - len(password) % 16) * '\0'
    # 加密
    ciphertext = cipher.encrypt(password.encode())
    # 将密文进行Base64编码
    ciphertext = base64.b64encode(ciphertext)
    return ciphertext.decode()


def md5_mix(key):
    slot = "nerkeler"
    encode = key + slot
    myKey = hashlib.md5(encode.encode("utf-8")).hexdigest().__str__()[:24]
    return myKey


def decode_password(encode):
    myKey = gen_key()
    return aes_decode(myKey, encode)


def encode_password(password):
    myKey = gen_key()
    return aes_encode(myKey, password)


def gen_key():
    with open("resource/aesKey", encoding='utf-8') as f:
        key = f.read().strip()
        myKey = md5_mix(key)
    return myKey




