<h1 align="center">- LuoguMsgNotifier -</h1>

<p align="center">
<img src="https://img.shields.io/github/v/release/xglight/LuoguMsgNotifier.svg">
<img src="https://img.shields.io/github/license/xglight/LuoguMsgNotifier" alt="License" />
<img src="https://img.shields.io/github/last-commit/xglight/LuoguMsgNotifier">
<img src="https://img.shields.io/github/downloads/xglight/LuoguMsgNotifier/total?label=Release%20Downloads">
<img src="https://img.shields.io/badge/support-Windows-blue?logo=Windows">
</p>

---

> 此项目由 [amakerlife](https://github.com/amakerlife) 的 [LuoguMsgNotifier](https://github.com/amakerlife/LuoguMsgNotifier) 项目 fork 而来，并进行了拓展。

## 介绍

在 Windows/Mail 上通知洛谷私信。

检测频率：10s - 1min

注意：**Windows 通知仅支持 Windows 10+ 且不保证对 Windows 10 早期版本的支持**。

## 使用方法

在 [Releases](https://github.com/xglight/LuoguMsgNotifier/releases) 页面下载最新版本的 `LuoguMsgNotifier.zip` 文件。

解压得到 `LuoguMsgNotifier.exe` 文件。

在 `config.json` 文件中填写相关信息，并保存。

> 若不存在 `config.json` 文件，请先运行 `LuoguMsgNotifier.exe`。

双击运行。

若出现 `INFO: 连接成功` 字样，则表示连接成功。

## 参数说明

### 登录信息

即 `config.json` 文件中的 `luogu` 字段。

关于 `_uid` 和 `__client_id` 请参考 [https://www.luogu.com/article/x6z3s5ri](https://www.luogu.com/article/x6z3s5ri)。

### 桌面通知

即 `config.json` 文件中的 `windows` 字段。

|  字段   |  类型  |                         说明                          |         默认值          |
| :-----: | :----: | :---------------------------------------------------: | :---------------------: |
| enable  |  bool  |                   是否启用桌面通知                    |          true           |
|  title  | string |                       通知标题                        |   "收到新的洛谷私信"    |
| content | string | 通知内容（`$user$` 为用户名，`$content$` 为私信内容） | "\$user\$: \$content\$" |

### 邮件通知

即 `config.json` 文件中的 `mail` 字段。

|     字段      |  类型  |                         说明                          |            默认值             |
| :-----------: | :----: | :---------------------------------------------------: | :---------------------------: |
|    enable     |  bool  |                   是否启用邮件通知                    |             false             |
|  smtp_server  | string |                    SMTP服务器地址                     |              ""               |
|   smtp_port   |  int   |                    SMTP服务器端口                     |               0               |
|   smtp_user   | string |                      SMTP用户名                       |              ""               |
| smtp_password | string |                       SMTP密码                        |              ""               |
|   receiver    | string |                      收件人邮箱                       |              ""               |
|     title     | string |                       通知标题                        | "来自 \$user\$ 的 Luogu 私信" |
|    content    | string | 通知内容（`$user$` 为用户名，`$content$` 为私信内容） |    "\$user\$: \$content\$"    |


## 手动编译

**请确保安装了 Python 3.x 及以上版本**

```bash
git clone https://github.com/xglight/LuoguMsgNotifier.git
cd LuoguMsgNotifier
pip install -r requirements.txt
pyinstaller LuoguMsgNotifier.spec
```

## 注意事项

1. 目前尚不能检验登录信息的有效性，请保证 `_uid` 和 `__client_id` 填写正确。
2. 由于 Outlook 于 2023 年关停了基本身份验证，因此 Outlook 邮箱的通知功能不可用。

## 改进？

- [ ] 增加登录信息有效性验证。
- [ ] 添加 `Helper.exe` 作为辅助程序，方便管理。
- [ ] 增加更多的通知方式，如邮件、微信、QQ 等。
- [x] 自定义通知内容。
