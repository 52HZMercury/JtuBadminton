import schedule
import time
from datetime import datetime, timedelta
from getBadmintonPlace import GetBadmintonPlace
from sendNotice import sendNotice
from getAfterDay import getAfterDay


def scheduleRun(weekdays, fieldId, targetDate, startTime, endTime, placeName, token):

    print(f"[{datetime.now()}] 等待执行任务中...", flush=True)
    sessionIds = []
    def task1():
        print(f"[{datetime.now()}] 开始执行获取场次任务...", flush=True)
        nonlocal sessionIds
        targetDate = getAfterDay()
        badminton_place = GetBadmintonPlace(token)
        sessionIds = badminton_place.getUniqueSessionId(fieldId, targetDate, startTime, endTime, placeName)

    def task2():
        print(f"[{datetime.now()}] 开始执行预定任务...", flush=True)
        nonlocal sessionIds
        badminton_place = GetBadmintonPlace(token)
        targetDate = getAfterDay()
        # 首先选择的场地编号
        number = int(placeName[0])
        flag = False
        first_flag = True

        # 有多少个场地，循环多少次
        for count in range(9):

            print(f"[{datetime.now()}] 进行第{count + 1}次尝试。场地: {number}号羽毛球，时间：{targetDate} {startTime}-{endTime}", flush=True)

            # 第一次尝试不执行, 第二次及以后的进行请求更新场次ID
            if not first_flag:
                sessionIds = badminton_place.getUniqueSessionId(
                            fieldId, targetDate, startTime, endTime,
                            f"{number}号羽毛球")
            first_flag = False

            if not sessionIds:
                number = (number % 9) + 1
                print(f"[{datetime.now()}] 没有可用场次，预约失败。", flush=True)
                time.sleep(1)
                continue

            response = badminton_place.sendReserveRequest(sessionIds, fieldId, targetDate, startTime, endTime, placeName)
            # 取出回复里面的状态码
            response_json = response.json()
            response_code = response_json.get('code')

            if response.status_code == 200 and response_code == 200:
                flag = True
                print(f"[{datetime.now()}] 预约成功，等待付款。场地: {placeName}，时间：{targetDate} {startTime}-{endTime}", flush=True)
                break
            else:
                number = (number % 9) + 1

            time.sleep(20)

        # 推送消息
        if flag:
            sendNotice(f"预约成功，等待付款。场地：{number}号羽毛球，时间：{targetDate} {startTime}-{endTime}")
        else:
            sendNotice(f"预约失败，请查看日志！")


    # 第一次尝试的获取场次任务提前五分钟进行，以压缩第一次发送预定时的时
    id_time = (datetime.strptime("22:25:00", "%H:%M:%S") + timedelta(seconds=0)).strftime("%H:%M:%S")
    print(f"[{datetime.now()}] 获取场次任务调整后的时间为 {id_time}", flush=True)

    reserve_time = (datetime.strptime("22:30:00", "%H:%M:%S") + timedelta(seconds=0)).strftime("%H:%M:%S")
    print(f"[{datetime.now()}] 预定场次任务调整后的时间为 {reserve_time}", flush=True)

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
    # 不需要填写，执行任务时自动获取
    targetDate = ""

    # 最多同时预定相邻的2小时场次
    startTime = "20:00:00"
    endTime = "21:00:00"

    # 这个参数意思是首先选择8号,如果失败，会继续尝试9号，1号，2号...
    # 因为服务器不能短时间内(20秒)多次重试，因此第一次没成功，等20秒之后很大概率场地已经抢完
    # 所以谨慎选择第一个尝试的场地
    placeName = "8号羽毛球"

    # 登录的token
    token = "$token$"

    # 抢星期几的场地，1代表周一，7代表周日
    weekdays = [2, 3]

    scheduleRun(weekdays, fieldId, targetDate, startTime, endTime, placeName, token)

    while True:
        schedule.run_pending()
        time.sleep(0.1)
