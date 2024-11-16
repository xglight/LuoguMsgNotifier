import json
import time
import websocket
from win11toast import toast
import logging
import os


hearders = {}

def init():
    global headers

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s: %(message)s')
    
    if not os.path.exists("login.json"):
        logging.error("请先填入登录信息")
        with open("login.json", "w", encoding="utf-8") as f:
            f.write('{"_uid": "", "__client_id": ""}')
        return

    with open("login.json", "r", encoding="utf-8") as f:
        login_data = json.load(f)
        _uid = login_data["_uid"]
        __client_id = login_data["__client_id"]
    
    headers = {
        "Cookie": f"_uid={_uid}; __client_id={__client_id}"
    }

    return _uid


class Listen_Message:
    def __init__(self, uid, Max_Reconnects=5, Cnt_Reconnect=0):
        self.uid = str(uid)
        self.Max_Reconnects = Max_Reconnects
        self.Cnt_Reconnect = Cnt_Reconnect

    def on_open(self,ws):
        logging.info("连接成功")
        self.Cnt_Reconnect = 0
        data = json.dumps({
            "channel": "chat",
            "channel_param": self.uid,
            "type": "join_channel"
        })
        ws.send(data)


    def on_close(self,ws, close_status_code, close_msg):
        logging.warning("连接已被关闭")


    def on_message(self, ws, message):
        data = json.loads(message)
        if data.get("_ws_type") == "server_broadcast":
            msg = data["message"]
            logging.info(f'{msg["sender"]["name"]} → {msg["receiver"]["name"]}: {msg["content"]}')
            if str(msg["sender"]["uid"]) != str(self.uid):
                button_open = {
                    "activationType": "protocol",
                    "arguments": f'https://www.luogu.com.cn/chat?uid={msg["sender"]["uid"]}',
                    "content": "查看私信"
                }
                toast("收到新的洛谷私信", f'{msg["sender"]["name"]}: {msg["content"]}',
                    duration="short",
                    buttons=[button_open, "忽略"],
                    audio={"silent": "true"})


    def connect(self):
        global headers
        ws_url = "wss://ws.luogu.com.cn/ws"
        ws = websocket.WebSocketApp(ws_url,
                                    on_open=self.on_open,
                                    on_message=self.on_message,
                                    on_close=self.on_close,
                                    header=headers)
        while True:
            ws.run_forever()
            try:
                ws.close()
            except:
                pass
            self.Cnt_Reconnect += 1
            logging.info(f'正在尝试重连({self.Cnt_Reconnect}/{self.Max_Reconnects})')
            time.sleep(5)
            if self.Cnt_Reconnect >= self.Max_Reconnects:
                logging.error("连接超时")
                toast("连接超时")
                break


if __name__ == "__main__":
    _uid = init()
    listen_msg = Listen_Message(_uid)
    listen_msg.connect()
    
