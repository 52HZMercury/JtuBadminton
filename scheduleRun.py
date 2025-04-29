import schedule
import time
from datetime import datetime, timedelta
from getBadmintonPlace import GetBadmintonPlace
from sendNotice import sendNotice
from syncTime import getServerTimeFromHeader, calculateTimeDiff

def getAfterDay():
    """
    获取当前日期第三天日期（只保留日期部分）
    """
    now = datetime.now()
    # 计算第三天的日期，并去掉时分秒
    afterday = (now + timedelta(days=2)).date()
    return str(afterday)


def scheduleRun(weekdays, fieldId, targetDate, startTime, endTime, placeName, token):

    print("开始执行,等待中...")

    def task():
        """
        定时任务的具体逻辑
        """
        # 创建 GetBadmintonPlace 实例
        badminton_place = GetBadmintonPlace(token)
        flag = False
        for _ in range(200):
            response = badminton_place.sendReserveRequest(fieldId, targetDate, startTime, endTime, placeName)
            if isinstance(response, str):
                print(f"[{datetime.now()}] 预约失败，正在重试。场地：{placeName}，时间：{startTime}-{endTime}")
            elif hasattr(response, 'status_code'):
                response_code = response.status_code
                if response_code == 200:
                    flag = True
                    print(f"[{datetime.now()}] 预约成功，等待付款。场地：{placeName}，时间：{startTime}-{endTime}")
                    sendNotice(f"预约成功，等待付款。场地：{placeName}，时间：{startTime}-{endTime}")
                    break
                time.sleep(1)
        # 推送消息
        if not flag:
            sendNotice(f"预约失败：{response}")


    # 调用 syncTime 计算时间差值
    serverTime = getServerTimeFromHeader()
    if serverTime:
        timeDiff = calculateTimeDiff(serverTime)
        print(f"[{datetime.now()}] 当前本地时间与服务器时间相差 {timeDiff} 秒")
        # 将时间差值加到原定时间 22:30:01(服务器时间) 上
        adjusted_time = (datetime.strptime("22:30:01", "%H:%M:%S") + timedelta(seconds=timeDiff)).strftime("%H:%M:%S")
        print(f"[{datetime.now()}] 调整后的时间为 {adjusted_time}")

        for weekday in weekdays:
            # 提前两天抢
            weekday = (int(weekday) - 3) % 7
            weekday_mapping = {
                0: schedule.every().monday,
                1: schedule.every().tuesday,
                2: schedule.every().wednesday,
                3: schedule.every().thursday,
                4: schedule.every().friday,
                5: schedule.every().saturday,
                6: schedule.every().sunday
            }
            if weekday in weekday_mapping:
                weekday_mapping[weekday].at(adjusted_time).do(task)



if __name__ == "__main__":
    # 九里 1462312540799516672
    # 犀浦 1462412671863504896
    fieldId = 1462312540799516672
    targetDate = getAfterDay()
    startTime = "20:00:00"
    endTime = "21:00:00"
    placeName = "5号羽毛球"
    token = "af01a19d-614d-4aea-b8e7-5403cbadc0d6"
    # 抢星期几的场地，1代表周一，7代表周日
    weekdays = [3, 5, 6]

    scheduleRun(weekdays, fieldId, targetDate, startTime, endTime, placeName, token)

    while True:
        schedule.run_pending()
        time.sleep(1)