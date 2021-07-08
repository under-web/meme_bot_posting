import time
import requests
import telebot
from bs4 import BeautifulSoup
from config import api_token, channel

bot = telebot.TeleBot(api_token)
count = 1

while True:
    try:
        global image_bytes
        url = 'https://topmemas.top/'
        r = requests.get(url).text
        soup = BeautifulSoup(r, 'lxml').find_all('div', class_='content_list')
        for i in soup:
            result_link = i.find('img').get('src')
            image_bytes = requests.get(f'{url}{result_link}').content

        bot.send_photo(channel, image_bytes)
        print(f'отправил {count}')
        count += 1
        time.sleep(1200)
    except Exception as e:
        print(e)
        time.sleep(30)

