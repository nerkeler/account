## 本地密码管理器2.0

`github`地址：https://github.com/nerkeler/account.git

最新版本蓝奏：https://wwtf.lanzoul.com/ij5vi0rhcywd

#### 修改点

- 新增了随机密码界面，可以按需求生成随机密码
- 更新账户bug修复
- 界面小小修改
- 查询默认为名称

#### 备份

将原始目录下 `dao`和`resource` 文件夹复制，覆盖新程序再目录下，即可完成导入数据

![](https://pic.imgdb.cn/item/6424f761a682492fcca3db19.png)

#### 新增随机密码

可以按照自己的需求生成相应的密码规则，`ABC`/`123`/`abc`/`#$&`

*注：在密码长度>字符类型数的时候会补数字  如  密码长度选30  规则选`abc`  会在26个字符后再补几个数字构成随机字符*

![](https://pic.imgdb.cn/item/6424f580a682492fcc9f685c.png)

#### 前言

闲来无事，看到自己有很多网站的账户密码，有些网站可能打开一两次也就忘记了，下一次在输入账户密码就想不起来，这样很容易丢失账号（当然也可以保存在浏览器自带的密码管理器中），虽然市面上也有很多优秀的账户密码管理软件，一来是这些程序大都是联网运行，在提供了多端存档的同时，也将密码和账户在网络上传输，虽然实际上很安全，但是并不是绝对的安全，二来，部分优秀的程序都是订阅付费机制，就想着自己干脆写个简单的本地的账户管理器，于是就有了这个小程序

先说一下优点吧，同市面上的程序比较，一个最突出的优点就是完全运行在本地，账户密码经过`AES`加密，在逻辑上可以说是非常安全的，因为你的密码不会暴漏在网络上，本地也进行了加密处理。

当然缺点也很明显，一是功能不是十分完善，二是该程序使用`tkinter` 模块编写，在布局和界面展示上都显得十分简陋，好在基本的功能没有问题

#### 启动

![](https://pic.imgdb.cn/item/6415d339a682492fcc119a5f.png)

首次启动会生成一个本地密钥，这个密钥就是AES的加密密钥，也是保存在程序目录/resource 下，在忘记登录密码的时候，可以按照程序的加密规则对数据库里的密码进行解密。

#### 登录

![](https://pic.imgdb.cn/item/6415d3c2a682492fcc12ae16.png)

第一次登陆密钥弹出框被关闭时，就进入了程序的登录界面，默认账户名admin 不可修改，默认密码为 ：**`password`**，建议第一次登陆时修改密码

#### 修改密码

![](https://pic.imgdb.cn/item/6415d44da682492fcc13b421.png)

在登陆界面 点击   **改密**  进入修改密码界面，新密码要求字符数大于8位，点击**确定** 按钮即可进行密码修改，修改成功后会提示修改成功，重新登陆，如下图所示

![](https://pic.imgdb.cn/item/6415d527a682492fcc1573f4.png)

#### 主页面

主界面略作修改

![](https://pic.imgdb.cn/item/6424f65aa682492fcca18f0d.png)

主界面共分为两个区域：

- 一个是上方的功能区，提供了查询、查看、新增、删除（软删除）功能，
- 一个是下方的账户展示区域，默认打开时按照列表展示所有账户信息

##### 相关操作

- 下拉框提供了  账户编号（对应下方序号列）、网站名称（对应下方网站列）、网站网址（对应下方网址列）查询条件转换
- 文本框接受  下拉框的对应字段，**为空时默认查询所有**
- 点击某一项账户时，**点击查看/双击当前项**  可进入当前账户查看界面，如图所示，当前页面也可以更新账户信息

![](https://pic.imgdb.cn/item/6415d77da682492fcc19f7db.png)

- 新增按钮会弹出新增界面，按照规定指示填写字段即可新增一条记录
- 删除按钮  在点击某一项账户时，点击删除，即可删除当前记录（软删除，更改了当前的状态）

#### 数据库

数据库方面使用的时`sqlite`,一共有两张表 `account.db`(保存账户信息)、`user.db`(程序账号信息)

结构如下：

```
account.db
CREATE TABLE account
           (id INTEGER primary key AUTOINCREMENT,
            web_name TEXT,
            account TEXT,
            password TEXT,
            url TEXT,
            note TEXT,
            create_time DATETIME not null,
            update_time DATETIME not null,
            state INTEGER DEFAULT 1
           )
```

```
user.db
CREATE TABLE user
                   (id INTEGER primary key AUTOINCREMENT,
                    username TEXT,
                    password TEXT,
                    create_time DATETIME not null,
                    update_time DATETIME not null,
                    state INTEGER DEFAULT 1
                   )
```

#### 补充说明

忘记登陆账户密码时，可将`account.db` 文件使用数据库可视化工具打开，取出当前账户的相关信息和密码，根据密钥和加密逻辑解密当前账户的密码明文

加密逻辑如下：

```python
import hashlib
from Crypto.Cipher import AES


def encode_password(password):
	key = yourkey			# key 表示你的密钥 
    
	slot = "nerkeler"
    encode = key + slot
    myKey = hashlib.md5(encode.encode("utf-8")).hexdigest().__str__()[:24]
    return aes_encode(myKey, password)
	
	
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
```





#### 总结

这个小程序不难，唯一复杂点的就是对密码的加密和解密了，代码写的也比较乱，有什么优化的地方大家交流一下

#### 欢迎大家提出使用建议！
