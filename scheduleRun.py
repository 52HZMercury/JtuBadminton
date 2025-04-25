# scheduleRun.py
import schedule
import time
from datetime import datetime, timedelta
from getBadmintonPlace import GetBadmintonPlace
from sendNotice import sendNotice

def getNextDay():
    """
    获取当前日期第三天日期（只保留日期部分）
    """
    # 获取当前时间
    now = datetime.now()
    # 计算第三天的日期，并去掉时分秒
    next_day = (now + timedelta(days=2)).date()
    return str(next_day)


def scheduleRun(fieldId, targetDate, startTime, endTime, placeName, token):
    print("开始执行,等待中...")

    def task():
        """
        定时任务的具体逻辑
        """
        # 创建 GetBadmintonPlace 实例
        badminton_place = GetBadmintonPlace(token)
        response = badminton_place.sendReserveRequest(fieldId, targetDate, startTime, endTime, placeName)
        # 推送消息
        if isinstance(response, str):
            sendNotice(f"预约失败：{response}")
        elif hasattr(response, 'status_code'):
            response_code = response.status_code
            if response_code == 200:
                sendNotice(f"预约成功，等待付款。场地：{placeName}，时间：{startTime}-{endTime}")
            else:
                sendNotice(f"预约失败，状态码：{response_code}")
        else:
            sendNotice("预约失败，未知错误")

    # 定时任务：
    # 每周四、周五的 22:30 执行
    # 预约周六、周日
    schedule.every().thursday.at("22:30:02").do(task)
    schedule.every().friday.at("23:59:03").do(task)


if __name__ == "__main__":
    # 九里 1462312540799516672
    # 犀浦 1462412671863504896
    fieldId = 1462312540799516672
    targetDate = getNextDay()
    startTime = "18:00:00"
    endTime = "19:00:00"
    placeName = "4号羽毛球"
    token = $TOKEN_HERE

    scheduleRun(fieldId, targetDate, startTime, endTime, placeName, token)

    while True:
        schedule.run_pending()
        time.sleep(1)