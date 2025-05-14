from datetime import datetime, timedelta

# 提前几天
delay = 2

"""
获取当前日期第三天毫秒时间戳（只保留日期部分）
"""
def getAfterDayTimestamp():
    # 获取当前时间
    now = datetime.now()
    # 计算第三天的日期
    afterDay = (now + timedelta(days=delay)).replace(hour=0, minute=0, second=0, microsecond=0)
    # 转换为毫秒时间戳
    timestamp_ms = int(afterDay.timestamp() * 1000)
    return timestamp_ms

"""
获取当前日期第三天日期（只保留日期部分）
"""
def getAfterDay():
    now = datetime.now()
    # 计算第三天的日期，并去掉时分秒
    afterday = (now + timedelta(days=delay)).date()
    return str(afterday)

