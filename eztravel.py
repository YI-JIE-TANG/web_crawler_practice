import requests
import json
import pandas as pd

payload = {
    "data": {
        "checkInDate": "2023-05-23",
        "checkOutDate": "2023-05-24",
        "childAges": "",
        "cityID": 7805,
        "direction": 0,
        "facility": 0,
        "hotelQuerySettingList": {},
        "isFreeCancel": False,
        "isInstantConfirm": False,
        "isNeedReFetch": True,
        "orderBy": 0,
        "pageIndex": 1,
        "pageSize": 10,
        "person": 2,
        "provinceID": 0,
        "roomCount": 1
    },
    "head": {
        "auth": "",
        "cid": "03168350899771359599",
        "cver": "6.1.0",
        "lang": "zh",
        "sid": "3",
        "sver": "",
        "syscode": "03"
    }
}

response = requests.post("https://h.eztravel.com.tw/api/hotel/public/listV2", json=payload)
response.encoding = "utf-8"

result = json.loads(response.text)

data = [[i['hotelName'], i['cityName'], i['address'], i['twdPriceWithTax']] for i in result['data']['list']]
data_2 = result['data']['list']

points = []
for item in data_2:
    points.append([item['comment']['totalPoint']])
        
df = pd.DataFrame(data=data, columns=["飯店名稱", "縣市", "地址", "每晚含稅價"])
df["評價分數(1-5)"] = pd.DataFrame(points)
df.to_csv("eztravel.csv", encoding="utf_8_sig", index=False)