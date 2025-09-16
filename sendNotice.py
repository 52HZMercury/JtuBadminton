import requests
from datetime import datetime


import requests
from datetime import datetime


def sendNotice(push_token, content):
    token = push_token
    title = "场馆预约"
    url = f"http://www.pushplus.plus/send?token={token}&title={title}&content={content}&template=html"
    try:
        response = requests.request("GET", url, timeout=10)
        print(f"[{datetime.now()}] 通知发送成功: {response.status_code}")
    except requests.exceptions.Timeout:
        print(f"[{datetime.now()}] 发送通知超时，已跳过")
    except requests.exceptions.RequestException as e:
        print(f"[{datetime.now()}] 发送通知时发生错误: {e}")
    except Exception as e:
        print(f"[{datetime.now()}] 发送通知时发生未知错误: {e}")
    print(f"[{datetime.now()}] 已推送信息")

