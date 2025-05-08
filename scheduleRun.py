import schedule
import time
from datetime import datetime, timedelta
from getBadmintonPlace import GetBadmintonPlace
from sendNotice import sendNotice
from syncTime import getServerTimeFromHeader, calculateTimeDiff
from getAfterDay import getAfterDay


def scheduleRun(weekdays, fieldId, targetDate, startTime, endTime, placeName, token):

    print(f"[{datetime.now()}] 等待执行任务中...")
    sessionId = ""
    def task1():
        print(f"[{datetime.now()}] 开始执行获取场次任务...")

        nonlocal sessionId
        badminton_place = GetBadmintonPlace(token)
        sessionId = badminton_place.getUniqueSessionId(fieldId, targetDate, startTime, endTime, placeName)

    def task2():
        print(f"[{datetime.now()}] 开始执行预定任务...")

        nonlocal sessionId
        badminton_place = GetBadmintonPlace(token)
        flag = False
        for count in range(20):
            response = badminton_place.sendReserveRequest(sessionId, fieldId, targetDate, startTime, endTime, placeName)
            # 取出回复里面的状态码
            response_json = response.json()
            response_code = response_json.get('code')

            if response.status_code == 200 and response_code == 200:
                flag = True
                print(f"[{datetime.now()}] 预约成功，等待付款。场地：{placeName}，时间：{targetDate} {startTime}-{endTime}")
                break
            else:
                print(f"[{datetime.now()}] 预约失败，正在进行第{count}次重试。场地：{placeName}，时间：{targetDate} {startTime}-{endTime}")

            time.sleep(2)

        # 推送消息
        if flag:
            sendNotice(f"预约成功，等待付款。场地：{placeName}，时间：{startTime}-{endTime}")
        else:
            sendNotice(f"预约失败：{response}")


    # 调用 syncTime 计算时间差值
    # serverTime = getServerTimeFromHeader()
    # if serverTime:
    #     timeDiff = calculateTimeDiff(serverTime)
    #     print(f"[{datetime.now()}] 当前本地时间与服务器时间相差 {timeDiff} 秒")
    #     # 将时间差值加到原定时间 22:30:00(服务器时间) 上
    #     adjusted_time = (datetime.strptime("15:47:00", "%H:%M:%S") + timedelta(seconds=timeDiff)).strftime("%H:%M:%S")
    #     print(f"[{datetime.now()}] 调整后的时间为 {adjusted_time}")

    id_time = (datetime.strptime("22:25:00", "%H:%M:%S") + timedelta(seconds=0)).strftime("%H:%M:%S")
    print(f"[{datetime.now()}] 获取场次任务调整后的时间为 {id_time}")

    reserve_time = (datetime.strptime("22:30:00", "%H:%M:%S") + timedelta(seconds=0)).strftime("%H:%M:%S")
    print(f"[{datetime.now()}] 预定场次任务调整后的时间为 {reserve_time}")

    for weekday in weekdays:
        # 提前两天
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
            weekday_mapping[weekday].at(id_time).do(task1)

    for weekday in weekdays:
        # 提前两天
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
            weekday_mapping[weekday].at(reserve_time).do(task2)



if __name__ == "__main__":
    # 九里 1462312540799516672
    # 犀浦 1462412671863504896
    fieldId = 1462412671863504896
    targetDate = getAfterDay()
    startTime = "20:00:00"
    endTime = "21:00:00"
    placeName = "5号羽毛球"
    token = "$token$"
    # 抢星期几的场地，1代表周一，7代表周日
    weekdays = [3, 4, 5, 6]

    scheduleRun(weekdays, fieldId, targetDate, startTime, endTime, placeName, token)

    while True:
        schedule.run_pending()
        time.sleep(0.5)