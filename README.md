# 密码管理器

***图文使用介绍：[https://nerkeler.xyz/2023/03/20/windows%E5%AF%86%E7%A0%81%E7%AE%A1%E7%90%86%E5%99%A8/](https://nerkeler-hexo.netlify.app/2023/03/20/windows%E5%AF%86%E7%A0%81%E7%AE%A1%E7%90%86%E5%99%A8/)**<br>
该密码管理器是一个离线本地使用的工具，采用`AES`对称加密，保证了用户数据的安全性。它支持导入导出，也可方便地管理Chrome/Edge浏览器的密码本。

## 重要提示

- **程序初始密码**：`password`

## 功能

- 添加、删除、编辑账号信息
- 导入、导出账号信息
- 采用AES对称加密，确保数据安全
- 支持管理Chrome/Edge浏览器密码本
- 随机密码生成器

## 运行环境

- Python 3.8
- Windows 7+
- SQLite3数据库
- Tkinter GUI框架

## 特点

- 离线本地使用，安全性高
- 支持导入导出数据
- 使用AES对称加密算法保证密码安全
- 管理Chrome/Edge浏览器密码本
- 简单易用，操作便捷

## 使用说明

1. 下载解压程序文件
2. 运行`account.exe`文件
3. 点击`新建账号`按钮添加新的账号密码信息
4. 双击表格中的数据进行编辑或删除
5. 点击`导出`按钮将数据导出为CSV格式文件
6. 点击`导入`按钮选择CSV文件进行导入数据
7. 可按需求导入并管理`Chrome/Edge密码本`浏览器密码

## 注意事项

- 密码管理工具涉及到您的个人隐私，务必注意保护好您的密码库文件。
- 密码库文件默认保存在程序所在文件夹下的`dao、resource`文件夹中，请不要删除或移动该文件夹。
- 如果您的密码库文件意外丢失或损坏，您将无法找回里面的数据，请务必做好备份工作。



## 更新日志

### v1.0

- 实现基本的账号密码增删改查功能
- 使用AES对称加密算法保证密码安全

### v2.0

- 新增随机密码功能
- 界面样式更改

### v3.0

- 优化程序性能，提高运行速度
- 支持导入导出数据
- 修复若干已知Bug

### v4.0

- 增加chrome/edge浏览器密码导入
- 导出逻辑更改
- 增加关于页面介绍

### v4.2

- 本地密码导出中文乱码修复
- 引入日志记录
- 优化edge/chrome 浏览器导出适配管理

## 未来计划

- 支持更多浏览器的密码导入
- 支持多用户管理

## 联系方式

如有任何问题或建议，欢迎发送电子邮件至：[2739038007@qq.com](2739038007@qq.com)。

QQ讨论群：703300124
