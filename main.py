from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random
import time
 
localtime = time.localtime(time.time())
print ("本地时间为 :", localtime)

today = datetime.now()
start_date = os.environ['START_DATE'] # 日期格式的字符串 "2018-01-11"
city = os.environ['CITY'] # 地区字符串 "深圳"
birthday = os.environ['BIRTHDAY'] # 日期字符串  "08-16"
Legal_start = os.environ['LEGAL_START']
print(Legal_start)
#Legal_start = os.environ['LEGAL_START'] # 日期格式的字符串 "2018-01-11"

 

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]
user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]




# 对应模板格式
# {{today.DATA}}  {{week.DATA}}  
# {{festival.DATA}}  
# 天气: {{weather.DATA}} 
# 最低温度:{{low.DATA}}
# 最高温度:{{high.DATA}}
# 今天是我们恋爱的第:{{love_days.DATA}} 天
# 我们已经成为合法夫妇:{{Legal_couple.DATA }} 天
# 距离你的生日还有:{{birthday_left.DATA}}天

# {{words.DATA}}

# {{Text.DATA}}

def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['low']),math.floor(weather['high'])

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_Legal_couple_days():
  delta = today - datetime.strptime(Legal_start, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


wea,low,high  = get_weather()
weekList=["星期一","星期二","星期三","星期四","星期五","星期六","星期日"]
todaystr=today.strftime("%Y-%m-%d") 
weekSrt=weekList[datetime.now().weekday()]
festival="周末愉快!" if datetime.now().weekday()>=6 else ""

data = {
  "today":{"value":todaystr},
  "week":{"value":weekSrt},
  "festival":{"value":festival},
  "weather":{"value":wea},
  "low":{"value":low},
  "high":{"value":high}, 
  "love_days":{"value":get_count()},
  "Legal_couple":{"value":get_Legal_couple_days()},# 空字符或数值
  "birthday_left":{"value":get_birthday()},
  "words":{"value":get_words(), "color":get_random_color()},
  "Text":{"value":get_words(), "color":get_random_color()}
}


print(data)

client = WeChatClient(app_id, app_secret)
wm = WeChatMessage(client)

res = wm.send_template(user_id, template_id, data)
print(res)
