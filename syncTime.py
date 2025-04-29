import requests
from datetime import datetime, timedelta

def calculateTimeDiff(serverTime):
    """
    计算服务器时间与当前本地时间相差的秒数
    """
    # 将服务器时间字符串解析为 datetime 对象
    serverDatetime = datetime.strptime(serverTime, '%Y-%m-%d %H:%M:%S')
    # 获取当前本地时间
    localDatetime = datetime.now()
    # 计算时间差
    timeDiff = (localDatetime - serverDatetime).total_seconds()
    return timeDiff
def convert2gmt8(serverTime):
    """
    将服务器时间(GMT)转换为北京时间(GMT+8)
    """
    # 解析服务器时间为 datetime 对象
    gmt_time = datetime.strptime(serverTime, '%a, %d %b %Y %H:%M:%S GMT')
    # 转换为北京时间（GMT+8）
    gmt8_time = gmt_time + timedelta(hours=8)
    return gmt8_time.strftime('%Y-%m-%d %H:%M:%S')

def getServerTimeFromHeader():
        """
        发送 GET 请求获取系统参数，并提取响应标头中的 date 字段作为服务器时间信息
        """
        url = "https://zhcg.swjtu.edu.cn/onesports-gateway/wechat-c/api/wechat/indexController/getSystemParameters"

        # 发送 GET 请求
        response = requests.get(url, verify=False)

        # 提取响应标头中的 date 字段
        serverTimeGMT0 = response.headers.get("date")

        if serverTimeGMT0:
            serverTimeGMT8 = convert2gmt8(serverTimeGMT0)
            print(f"[{datetime.now()}] 获取到服务器时间: {serverTimeGMT8}")
            return serverTimeGMT8
        else:
            print(f"[{datetime.now()}] 未获取到服务器时间")
            return None

if __name__ == "__main__":
    serverTime = getServerTimeFromHeader()
    diff = calculateTimeDiff(serverTime)
    print(f"[{datetime.now()}] 当前本地时间与服务器时间相差 {diff} 秒")
