import requests
from datetime import datetime
def sendNotice(content):
    token = "74d8fb96035b45e79f1b77f2dd699196"
    title = "场馆预约"
    url = f"http://www.pushplus.plus/send?token={token}&title={title}&content={content}&template=html"
    response = requests.request("GET", url)
    print(f"[{datetime.now()}]推送信息 {response.text}")

