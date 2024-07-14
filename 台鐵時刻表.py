import requests
from bs4 import BeautifulSoup
import pandas as pd

payload= {
	"_csrf": "d426467a-e2f8-46bf-a851-549b934e7804",
	"startStation": "1080-桃園",
	"endStation": "1210-新竹",
	"transfer": "ONE",
	"rideDate": "2023/05/01",
	"startOrEndTime": "true",
	"startTime": "00:00",
	"endTime": "23:59",
	"trainTypeList": "ALL",
	"queryClassification": "NORMAL",
	"query": "查詢"
}

response = requests.post("https://tip.railway.gov.tw/tra-tip-web/tip/tip001/tip112/querybytime", data = payload)

root = BeautifulSoup(response.text,"html.parser")

df = pd.DataFrame(columns=['始發站 → 終點站','出發時間','抵達時間','行駛時間'])

tr = root.find_all("tr", class_ = "trip-column")

for index in tr:
    data = []
    locations = index.find_all('span', attrs={"class":"location"})
    start_station = locations[0].text.strip()  
    end_station = locations[1].text.strip()
    data.append(f"{start_station}→{end_station}")  
    tds = index.find_all('td')
    data.append(tds[1].text.strip())  
    data.append(tds[2].text.strip())  
    data.append(tds[3].text.strip())  

    df.loc[len(df)] = data

df.to_csv('台鐵時刻表.csv',encoding="utf_8_sig",index = False)
