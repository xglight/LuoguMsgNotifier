import requests

hearder = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
    "cookie": "__client_id=ca4bbe72de4daa3d894c5fa7369bdd403f12000d; _uid=755370; C3VK=c4ae51"
}

url = "https://www.luogu.com.cn/record/31079909"

response = requests.get(url, headers=hearder)

print(response.status_code)

with open("test.html", "w", encoding="utf-8") as f:
    f.write(response.text)
