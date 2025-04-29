import requests
from datetime import datetime, timedelta

class GetBadmintonPlace:
    def __init__(self,token):
        self.getAllSessionIdRequestUrl = "https://zhcg.swjtu.edu.cn/onesports-gateway/wechat-c/api/wechat/memberBookController/weChatSessionsList"
        self.sendReserveRequestUrl = "https://zhcg.swjtu.edu.cn/onesports-gateway/business-service/orders/weChatSessionsReserve"
        self.sessionId = ""
        self.token = token

    def getAfterDayTimestamp(self):
        """
        获取当前日期后天的毫秒时间戳
        """
        # 获取当前时间
        now = datetime.now()
        # 计算第三天的日期
        afterDay = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        # 转换为毫秒时间戳
        timestamp_ms = int(afterDay.timestamp() * 1000)
        return timestamp_ms

    def getAllSessionIdRequest(self,fieldId):
        """
        获取sessionId
        """
        url = self.getAllSessionIdRequestUrl

        search_date_timestamp = self.getAfterDayTimestamp()  # 获取时间戳
        search_date = datetime.fromtimestamp(search_date_timestamp / 1000).strftime('%Y-%m-%d')  # 转换为日期字符串

        payload = {
            "fieldId": fieldId,
            "isIndoor": "",
            "placeTypeId": "",
            "searchDate": search_date,
            "sportTypeId": "2"
        }

        # 请求头
        headers = {
            'Content-Type': 'application/json',
            'X-UserToken': self.token,  # token
            'token': self.token
        }

        response = requests.post(url, json=payload, headers=headers, verify=False)

        # 打印响应状态码和内容
        print(f"[{datetime.now()}] 获取全部场次 SessionId, Status Code:", response.status_code)
        # print("[Response Body]:", response.json())
        return response


    def getUniqueSessionId(self,fieldId, targetDate, startTime, endTime, placeName):
        """
        根据指定条件获取唯一的场次 ID
        :param fieldId: 场地 ID
        :param targetDate: 目标日期 (格式: YYYY-MM-DD)
        :param startTime: 开始时间 (格式: HH:mm:ss)
        :param endTime: 结束时间 (格式: HH:mm:ss)
        :param placeName: 场地名称
        :return: 符合条件的场次 ID 或 None
        """
        # 调用 getAllSessionIdRequest 获取所有场次数据
        response = self.getAllSessionIdRequest(fieldId)

        # 假设返回的是 JSON 数据
        sessions_data = response.json()

        # 遍历嵌套列表结构
        for outer_list in sessions_data:  # 外层列表
            for session in outer_list:  # 内层列表中的字典
                if (session.get("openDate") == targetDate and
                    session.get("openStartTime") == startTime and
                    session.get("openEndTime") == endTime and
                    session.get("placeName") == placeName and
                    session.get("sessionsStatus") == "NO_RESERVED"):
                    print(f"[{datetime.now()}] 获取到符合条件的场次:", session)
                    return session.get("id")  # 返回符合条件的场次 ID

        print(f"[{datetime.now()}] 未获取到符合条件的场次")
        return None

    def sendReserveRequest(self, fieldId, targetDate, startTime, endTime, placeName):
        # 请求地址
        url = self.sendReserveRequestUrl

        # 动态获取 orderUseDate
        order_use_date = self.getAfterDayTimestamp()
        if(self.sessionId == ""):
            sessionIdUnique = self.getUniqueSessionId(fieldId, targetDate, startTime, endTime, placeName)
            if sessionIdUnique is None:
                return "未获取到符合条件的场次"
            self.sessionId = sessionIdUnique
        else:
            fieldName =  "九里羽毛球1-6号" if fieldId == 1462312540799516672 else "犀浦室内羽毛球馆"
            # 请求体内容
            payload = {
                "number": 2,
                "orderUseDate": order_use_date,  # 日期时间戳
                "requestsList": [{
                    "sessionsId": self.sessionId  # 场次id
                }],
                "fieldName": fieldName,
                "fieldId": fieldId,  # 场地id(九里羽毛球1-6号，犀浦室内羽毛球馆)
                "siteName": placeName,
                "sportTypeName": "羽毛球",
                "sportTypeId": "2"
            }

            # 请求头
            headers = {
                'Content-Type': 'application/json',
                'X-UserToken': self.token,
                'token': self.token
            }

            # 发送 POST 请求
            response = requests.post(url, json=payload, headers=headers, verify=False)

            # 打印响应状态码和内容
            print(f"[{datetime.now()}] 预定指定场次 Status Code:{response.status_code}, 预定信息:{response.json()}", )
            # print("[Response Body]:", response.json())
            return response



if __name__ == "__main__":
    # 创建 GetBadmintonPlace 实例
    badminton_place = GetBadmintonPlace("$token$")

    # 测试参数
    fieldId = 1462412671863504896   # 示例场地 ID
    targetDate = "2025-04-29"       # 目标日期
    startTime = "19:00:00"          # 开始时间
    endTime = "20:00:00"            # 结束时间
    placeName = "4号羽毛球"         # 场地名称

    # 调用 getUniqueSessionId 方法
    badminton_place.sendReserveRequest(fieldId, targetDate, startTime, endTime, placeName)

