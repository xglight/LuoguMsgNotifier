import json
import time
import websocket
from win11toast import toast
import logging
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

enable_windows_notifier = True
enable_email_notifier = False
email_notifier = None

windows_title = "收到新的洛谷私信"
windows_content = "$user$: $content$"

email_title = "来自 $user$ 的 Luogu 私信"
email_content = "$user$: $content$"


def init():
    global email_notifier
    global enable_email_notifier
    global enable_windows_notifier
    global windows_title
    global windows_content
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s: %(message)s')

    if not os.path.exists("config.json"):
        logging.error("请先填入登录信息")
        board_config = {
            "luogu": {
                "_uid": "",
                "__client_id": ""
            },
            "windows": {
                "enable": "true",
                "title": "收到新的洛谷私信",
                "content": "$user$: $content$"
            },
            "email": {
                "enable": "false",
                "smtp_server": "",
                "smtp_port": 0,
                "smtp_user": "",
                "smtp_password": "",
                "receiver": "",
                "title": "来自 $user$ 的 Luogu 私信",
                "content": "$user$: $content$"
            }
        }
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(board_config, f, ensure_ascii=False, indent=4)
        return

    with open("config.json", "r", encoding="utf-8") as f:
        login_data = json.load(f)

        # 登录信息
        if (not login_data.get("luogu")) or login_data["luogu"]["_uid"] == "" or login_data["luogu"]["__client_id"] == "":
            logging.error("请先填入登录信息")
            return
        _uid = login_data["luogu"]["_uid"]
        __client_id = login_data["luogu"]["__client_id"]

        # 开启windows通知
        if login_data.get("windows") and login_data["windows"].get("enable"):
            if login_data["windows"]["enable"] == 'false':
                enable_windows_notifier = False
            else:
                logging.info("windows通知已开启")
                windows_title = login_data["windows"].get("title")
                windows_content = login_data["windows"].get("content")
                enable_windows_notifier = True
        else:
            enable_windows_notifier = False

        # 邮箱信息
        if not login_data.get("email"):
            return _uid, __client_id

        if login_data["email"].get("enable"):
            if login_data["email"]["enable"] == 'false':
                return _uid, __client_id
            logging.info("邮箱通知已开启")
            enable_email_notifier = True
        else:
            return _uid, __client_id
        if login_data["email"].get("smtp_server") and login_data["email"].get("smtp_port") and login_data["email"].get("smtp_user") and login_data["email"].get("smtp_password") and login_data["email"].get("receiver"):
            smtp_server = login_data["email"]["smtp_server"]
            smtp_port = login_data["email"]["smtp_port"]
            smtp_user = login_data["email"]["smtp_user"]
            smtp_password = login_data["email"]["smtp_password"]
            receiver = login_data["email"]["receiver"]
            email_notifier = Email_Notifier(
                smtp_server, smtp_port, smtp_user, smtp_password, receiver)

    return _uid, __client_id


class Email_Notifier:
    def __init__(self, smtp_server, smtp_port, smtp_user, smtp_password, receiver):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = smtp_user
        self.password = smtp_password
        self.to_email = receiver

    def send_email(self, subject, body):
        # 创建一个MIMEText对象
        msg = MIMEMultipart()
        msg['From'] = self.username
        msg['To'] = self.to_email
        msg['Subject'] = subject

        # 添加入内容
        msg.attach(MIMEText(body, 'plain'))

        try:
            # 连接到SMTP服务器
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # 启用安全传输
                server.login(self.username, self.password)  # 登录
                server.sendmail(self.username, self.to_email,
                                msg.as_string())  # 发送邮件
            logging.info(f"邮件发送成功：{self.to_email}")
        except Exception as e:
            logging.error(f"邮件发送失败：{e}")


class Windows_Notifier:
    def __init__(self, uid, name, content):
        self.uid = str(uid)
        self.name = name
        self.content = content

    def show(self):
        global windows_title
        global windows_content
        button_open = {
            "activationType": "protocol",
            "arguments": f'https://www.luogu.com.cn/chat?uid={self.uid}',
            "content": "查看私信"
        }
        _content = windows_content
        _content.replace("$user$", self.name)
        _content.replace("$content$", self.content)
        toast(windows_title, _content,
              duration="short",
              buttons=[button_open, "忽略"],
              audio={"silent": "true"})


class Listen_Message:
    def __init__(self, uid, __client_id, Max_Reconnects=5, Cnt_Reconnect=0):
        self.uid = str(uid)
        self.Max_Reconnects = Max_Reconnects
        self.Cnt_Reconnect = Cnt_Reconnect
        self.headers = {
            "Cookie": f"_uid={uid}; __client_id={__client_id}"
        }

    def on_open(self, ws):
        logging.info("连接成功")
        self.Cnt_Reconnect = 0
        data = json.dumps({
            "channel": "chat",
            "channel_param": self.uid,
            "type": "join_channel"
        })
        ws.send(data)

    def on_close(self, ws, close_status_code, close_msg):
        logging.warning("连接已被关闭")

    def on_message(self, ws, message):
        global email_notifier
        global enable_windows_notifier
        global enable_email_notifier

        global email_title
        global email_content

        data = json.loads(message)
        if data.get("_ws_type") == "server_broadcast":
            msg = data["message"]
            logging.info(
                f'{msg["sender"]["name"]} → {msg["receiver"]["name"]}: {msg["content"]}')
            if str(msg["sender"]["uid"]) != str(self.uid):
                if enable_windows_notifier:
                    logging.info("windows通知")
                    Windows_Notifier(
                        msg["sender"]["uid"], msg["sender"]["name"], msg["content"]).show()

                if enable_email_notifier:
                    logging.info("邮件通知")
                    _title = email_title
                    _content = email_content

                    _title.replace("$user$", msg["sender"]["name"])
                    _content.replace("$user$", msg["sender"]["name"])
                    _title.replace("$content$", msg["content"])
                    _content.replace("$content$", msg["content"])

                    email_notifier.send_email(_title, _content)

    def connect(self):
        ws_url = "wss://ws.luogu.com.cn/ws"
        ws = websocket.WebSocketApp(ws_url,
                                    on_open=self.on_open,
                                    on_message=self.on_message,
                                    on_close=self.on_close,
                                    header=self.headers)
        while True:
            ws.run_forever()
            try:
                ws.close()
            except:
                pass
            self.Cnt_Reconnect += 1
            logging.info(f'正在尝试重连 {self.Cnt_Reconnect}/{self.Max_Reconnects}')
            time.sleep(5)
            if self.Cnt_Reconnect >= self.Max_Reconnects:
                logging.error("连接超时")
                toast("连接超时")
                break


if __name__ == "__main__":
    try:
        _uid, __client_id = init()
    except:
        exit()
    listen_msg = Listen_Message(_uid, __client_id)
    listen_msg.connect()
