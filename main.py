import time
import requests
import telebot
from bs4 import BeautifulSoup
from config import api_token, channel

bot = telebot.TeleBot(api_token)
count = 1

def get_request_html(url):
    res = requests.get(url).text
    return res

def grab_top_meme():
    url = 'https://topmemas.top/'
    soup = BeautifulSoup(get_request_html(url), 'lxml').find_all('div', class_='content_list')
    for i in soup:
        result_link = i.find('img').get('src')
        image_bytes = requests.get(f'{url}{result_link}').content
        return image_bytes

while True:
    try:
        bot.send_photo(channel, grab_top_meme())
        print(f'отправил {count}')
        count += 1
        time.sleep(1200)
    except Exception as e:
        print(e)
        time.sleep(30)
