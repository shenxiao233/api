import requests
import json

url = "https://gist.githubusercontent.com/yonghuname/14d0a057154f9a4d2c98d9c91137c966/raw/c16a3b229cbc01004b4a865e7673996b6d7001ff/202310_windows-google-chrome-1709530945035.json"

response = requests.get(url)
data = response.json()

print()  # 将JSON数据以漂亮的格式打印出来
