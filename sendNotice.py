import requests
from datetime import datetime
def sendNotice(content):
    token = "$token$"
    title = "场馆预约"
    url = f"http://www.pushplus.plus/send?token={token}&title={title}&content={content}&template=html"
    response = requests.request("GET", url)
    print(f"[{datetime.now()}] 已推送信息")

