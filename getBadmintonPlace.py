import requests
import schedule
import time
from datetime import datetime
def getNextDayTimestamp():
    """
    获取当前日期第二天的毫秒时间戳
    """
    # 获取当前时间
    now = datetime.now()
    # 计算第二天的日期
    next_day = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    # 转换为毫秒时间戳
    timestamp_ms = int(next_day.timestamp() * 1000)
    return timestamp_ms

def getSessionIdRequest():
    """
    获取sessionId
    """
    url = "https://zhcg.swjtu.edu.cn/onesports-gateway/wechat-c/api/wechat/memberBookController/weChatSessionsList"
    payload = {
        "fieldId": "1462312540799516672",
        "isIndoor": "",
        "placeTypeId": "",
        "searchDate": "2025-04-26",
        "sportTypeId": "2"
    }

def sendReserveRequest():
    # 请求地址
    url = "https://zhcg.swjtu.edu.cn/onesports-gateway/business-service/orders/weChatSessionsReserve"

    # 动态获取 orderUseDate
    order_use_date = get_next_day_timestamp()

    # 请求体内容
    payload = {
        "number": 2,
        "orderUseDate": order_use_date,  # 日期时间戳
        "requestsList": [{
            "sessionsId": "1905652610257395712"  # 场次时间id
        }],
        "fieldName": "九里羽毛球1-6号",
        "fieldId": "1462312540799516672",  # 场地id
        "siteName": "1号羽毛球",
        "sportTypeName": "羽毛球",
        "sportTypeId": "2"
    }

    # 请求头
    headers = {
        'Content-Type': 'application/json',
        'X-UserToken': 'af01a19d-614d-4aea-b8e7-5403cbadc0d6',  # token
        'token': 'af01a19d-614d-4aea-b8e7-5403cbadc0d6'
    }

    # 发送 POST 请求
    response = requests.post(url, json=payload, headers=headers, verify=False)

    # 打印响应状态码和内容
    print(f"[{datetime.now()}] Status Code:", response.status_code)
    print("[Response Body]:", response.json())

# 定时任务：每周四、周五的 22:29 执行
schedule.every().thursday.at("22:30:02").do(send_reserve_request)
schedule.every().friday.at("22:30:03").do(send_reserve_request)

if __name__ == "__main__":
    print("定时任务已启动，等待每周四、周五的 22:30 执行...")
    while True:
        schedule.run_pending()
        time.sleep(1)