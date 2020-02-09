import discord
from selenium import webdriver
import time
from operator import eq
import os

client = discord.Client() # discord.Client() 대신 "app"를 써도 되게 만들어주자

@client.event
async def on_ready():
    print(client.user.id)
    print("ready")
    game = discord.Game("열심히 일")
    await client.change_presence(status=discord.Status.online, activity=game)

@client.event
async def on_message(message):
    if message.content.startswith("!help"):
        await message.channel.send("!전적검색 ID입력\n!전적검색 띄우고 아이디입력")
        await message.channel.send("!오늘날씨 지역입력\n!오늘날씨 띄우고 지역이름 ex) 대구 북구")
    elif message.content.startswith("!오늘날씨"):
        area = message.content[6:]
        driver = webdriver.Chrome("https://github.com/seokee33/DicBot/blob/master/cr.exe")
        driver.get("https://www.naver.com")
        driver.find_element_by_css_selector("#query").send_keys(area+" 오늘날씨")
        driver.find_element_by_css_selector("#search_btn").click()
        today = driver.find_element_by_class_name("cast_txt").text
        temperature = driver.find_element_by_css_selector("#main_pack > div.sc.cs_weather._weather > div > div.weather_box > div.weather_area._mainArea > div.today_area._mainTabContent > div.main_info > div.info_data > p.info_temperature > span").text
        driver.quit()
        await message.channel.send("온도 : "+temperature+"도\n"+today)
    elif message.content.startswith("!전적검색"):
        gameID = message.content[6:]
        driver = webdriver.Chrome("https://github.com/seokee33/DicBot/blob/master/cr.exe")
        driver.get("https://dak.gg")
        driver.find_element_by_css_selector("#frontPage > div.panel-left > form.search > input").send_keys(gameID)
        driver.find_element_by_css_selector("#frontPage > div > form > button > i").click()
        driver.find_element_by_css_selector("#profile > div > div > div.renew > button.renew > span").click()
        time.sleep(5)
        while True:
            renew = driver.find_element_by_css_selector("#profile > div > div > div > button.renew.latest > span").text
            if eq(renew, "최신 전적") == True :
                break
        time.sleep(10)
        soloKD = driver.find_element_by_css_selector("#profile > div > div > section > div > div > div > p.value").text
        soloDeals = driver.find_element_by_css_selector("#profile > div > div > section > div > div > div.deals.stats-item.stats-top-graph > p.value").text
        duoKD = driver.find_element_by_css_selector("#profile > div > div > section:nth-child(2) > div > div > div > p.value").text
        duoDeals = driver.find_element_by_css_selector("#profile > div > div > section:nth-child(2) > div > div > div:nth-child(4) > p.value").text
        squadKD = driver.find_element_by_css_selector("#profile > div > div > section:nth-child(3) > div > div > div > p.value").text
        squadDeals = driver.find_element_by_css_selector("#profile > div > div > section:nth-child(3) > div > div > div:nth-child(4) > p.value").text
        driver.quit()
        await message.channel.send("솔로\nK/D : " + soloKD + "\n평균 딜량 : " + soloDeals + "\n듀오\nK/D : " + duoKD + "\n평균 딜량 : " + duoDeals + "\n스쿼드\nK/D : " + squadKD + "\n평균 딜량 : " + squadDeals)

access_token = os.environ["BOT_TOKEN"]
client.run(access_token)
