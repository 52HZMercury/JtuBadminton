import schedule
import time
from getBadmintonPlace import GetBadmintonPlace

def scheduleRun(fieldId, targetDate, startTime, endTime, placeName, token):
    print("开始执行")
    # 创建 GetBadmintonPlace 实例
    badminton_place = GetBadmintonPlace()

    # 定时任务：每周四、周五的 22:30 执行
    schedule.every().thursday.at("22:30:02").do(badminton_place.sendReserveRequest, fieldId, targetDate, startTime, endTime, placeName, token)
    schedule.every().friday.at("22:30:03").do(badminton_place.sendReserveRequest, fieldId, targetDate, startTime, endTime, placeName, token)

if __name__ == "__main__":
    # 九里 1462312540799516672 犀浦 1462412671863504896
    fieldId = "1462312540799516672"
    targetDate = "2025-04-26"
    startTime = "20:00:00"
    endTime = "21:00:00"
    placeName = "5号羽毛球"
    token = $token

    scheduleRun(fieldId, targetDate, startTime, endTime, placeName, token)

    while True:
        schedule.run_pending()
        time.sleep(1)