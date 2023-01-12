import rsa, os


class MyRSA:
    def __init__(self):
        # 生成公钥，私钥
        self.public_key, self.private_key = rsa.newkeys(nbits=512)

    def save_rsa(self, public_key_filename, private_key_filename, save_path):
        """
        保存秘钥文件
        """
        with open(os.path.join(save_path, public_key_filename), "wb") as f:
            f.write(self.public_key.save_pkcs1())
        with open(os.path.join(save_path, private_key_filename), "wb") as f:
            f.write(self.private_key.save_pkcs1())

    def read_rsa_public(self, public_key_filename):
        """
        读取rsa公钥
        :param public_key_filename: rsa 公钥文件地址
        :return: 公钥
        """
        with open(public_key_filename, 'rb') as publickfile:
            pub = publickfile.read()
            pubkey = rsa.PublicKey.load_pkcs1(pub)
        return pubkey

    def read_rsa_private(self, private_key_filename):
        """
        读取rsa私钥
        :param private_key_filename: rsa 私钥文件地址
        :return: 私钥
        """
        with open(private_key_filename, 'rb') as privatefile:
            priv = privatefile.read()
            privkey = rsa.PrivateKey.load_pkcs1(priv)
        return privkey

    def encrypt(self, str, public_key=None):
        """
        使用公钥加密。如果传入了公钥，则使用传入的公钥加密；如果没有传入公钥，则使用初始化创建实例时的公钥加密。
        :param str: 待加密的字符串
        :param public_key: 公钥
        :return: 加密后的数据，bytes
        """
        if public_key:
            rsa.encrypt(message=str.encode("utf-8"), pub_key=public_key)
        return rsa.encrypt(message=str.encode("utf-8"), pub_key=self.public_key)

    def decrypt(self, str, private_key=None):
        """
        使用私钥解密. 如果传入了私钥，则使用传入的私钥解密；如果没有传入私钥，则使用初始化创建实例时的私钥解密。
        :param str: 待解密的数据
        :param private_key: 私钥
        :return: 解密后的数据，str
        """
        if private_key:
            return rsa.decrypt(str, priv_key=private_key).decode("utf-8")
        return rsa.decrypt(str, priv_key=self.private_key).decode("utf-8")

    def sign(self, message, private_key, hash_method="SHA-256"):
        """
        使用私钥进行签名. 默认hash算法为：'sha256'，也可以使用 md5 或其他hash算法
        :param message: 要签名的数据
        :param private_key: 私钥
        :param hash_method: hash算法
        :return: 签名后的数据
        """
        sign_result = rsa.sign(message=message, priv_key=private_key, hash_method=hash_method)
        return sign_result

    def verify(self, message, sign, public_key):
        """
        验签，使用公钥验证签名是否正确。如果正确，则返回签名算法,否则返回验证失败
        :param message: 已加密的数据
        :param sign: 已签名的数据
        :param public_key: 公钥
        :return: 验签正确：返回签名算法；验签错误：返回验证失败 False
        """
        try:
            verify = rsa.verify(message=message, signature=sign, pub_key=public_key)
            return verify
        except rsa.VerificationError:
            return False
