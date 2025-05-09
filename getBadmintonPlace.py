import requests
from datetime import datetime
from getAfterDay import getAfterDayTimestamp
from requests.models import Response
import json

class GetBadmintonPlace:
    def __init__(self,token):
        self.getAllSessionIdRequestUrl = "https://zhcg.swjtu.edu.cn/onesports-gateway/wechat-c/api/wechat/memberBookController/weChatSessionsList"
        self.sendReserveRequestUrl = "https://zhcg.swjtu.edu.cn/onesports-gateway/business-service/orders/weChatSessionsReserve"
        self.token = token

    def getAllSessionIdRequest(self,fieldId, targetDate):
        """
        获取sessionId
        """
        url = self.getAllSessionIdRequestUrl

        # search_date = getAfterDay()

        payload = {
            "fieldId": fieldId,
            "isIndoor": "",
            "placeTypeId": "",
            "searchDate": targetDate,
            "sportTypeId": "2"
        }

        # 请求头
        headers = {
            'Content-Type': 'application/json',
            'X-UserToken': self.token,
            'token': self.token
        }

        response = requests.post(url, json=payload, headers=headers, verify=False)


        print(f"[{datetime.now()}] 获取全部场次, 状态码:", response.status_code)
        # print("[Response Body]:", response.json())
        return response


    def getUniqueSessionId(self,fieldId, targetDate, startTime, endTime, placeName):
        """
        根据指定条件获取场次 ID列表, 匹配开始时间或结束时间相等的场次
        :param fieldId: 场地 ID
        :param targetDate: 目标日期 (格式: YYYY-MM-DD)
        :param startTime: 开始时间 (格式: HH:mm:ss)
        :param endTime: 结束时间 (格式: HH:mm:ss)
        :param placeName: 场地名称
        :return: 符合条件的场次 ID 列表
        """
        # 调用 getAllSessionIdRequest 获取所有场次数据
        response = self.getAllSessionIdRequest(fieldId, targetDate)
        matching_sessions = []

        sessions_data = response.json()

        # 遍历嵌套列表结构
        for outer_list in sessions_data:
            for session in outer_list:
                if (session.get("openDate") == targetDate and
                    (session.get("openStartTime") == startTime or session.get("openEndTime") == endTime) and
                    session.get("placeName") == placeName and
                    session.get("sessionsStatus") == "NO_RESERVED"):
                    print(f"[{datetime.now()}] 获取到符合条件的场次:", session)
                    matching_sessions.append(session.get("id"))

        if matching_sessions:
            print(f"[{datetime.now()}] 找到 {len(matching_sessions)} 个符合条件的场次")
            return matching_sessions

        print(f"[{datetime.now()}] 未获取到符合条件的场次")
        return []


    def sendReserveRequest(self, sessionIds, fieldId, targetDate, startTime, endTime, placeName):
        # 请求地址
        url = self.sendReserveRequestUrl

        # 动态获取 orderUseDate
        order_use_date = getAfterDayTimestamp()

        # 未获取到sessionId 无法初始化
        if not sessionIds:
            error_response = Response()
            error_response.status_code = 400
            error_response._content = json.dumps({
                "code": "400",
                "error": "未获取到符合条件的场次",
                "fieldId": fieldId,
                "targetDate": targetDate,
                "startTime": startTime,
                "endTime": endTime,
                "placeName": placeName
            }).encode('utf-8')
            return error_response

        fieldName =  "九里羽毛球1-6号" if fieldId == 1462312540799516672 else "犀浦室内羽毛球馆"
        # 请求体内容
        payload = {
            "number": 2,
            "orderUseDate": order_use_date,  # 日期时间戳
            "requestsList": [{"sessionsId": session_id} for session_id in sessionIds],
            "fieldName": fieldName,
            "fieldId": fieldId,  # 场地id
            "siteName": placeName,
            "sportTypeName": "羽毛球",
            "sportTypeId": "2"
        }

        headers = {
            'Content-Type': 'application/json',
            'X-UserToken': self.token,
            'token': self.token
        }

        # 发送 POST 请求
        response = requests.post(url, json=payload, headers=headers, verify=False)

        # 打印响应状态码和内容
        print(f"[{datetime.now()}] 预定指定场次，状态码:{response.status_code}, 预定信息:{response.json()}", )
        return response



if __name__ == "__main__":
    # 创建 GetBadmintonPlace 实例
    badminton_place = GetBadmintonPlace("$token$")

    # 测试参数
    fieldId = 1462412671863504896
    targetDate = "2025-05-11"
    startTime = "19:00:00"
    endTime = "21:00:00"
    placeName = "6号羽毛球"

    # 调用 getUniqueSessionId 方法
    badminton_place.getUniqueSessionId(fieldId, targetDate, startTime, endTime, placeName)

