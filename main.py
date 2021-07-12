import time
import requests
import telebot
from bs4 import BeautifulSoup
from config import api_token, channel

url = 'https://topmemas.top/'
bot = telebot.TeleBot(api_token)


def get_request_html(url):
    res = requests.get(url).text
    return res


def get_id():  # парсит id для определения актуальности мема
    soup_id = BeautifulSoup(get_request_html(url), 'lxml').find_all('div', class_='cont_item')
    result_id = soup_id[0].get('id')

    with open('id.txt', 'r', encoding='utf-8') as r_file:
        ids = r_file.readlines()
        if ids is None:
            r_file.writelines(str(result_id) + '\n')
            print('base impty, i am write')
            return False
        else:
            if str(result_id) + '\n' in ids:
                print(f'id - {result_id} in base!')
                return True
            else:
                with open('id.txt', 'a', encoding='utf-8') as file:
                    file.writelines(str(result_id) + '\n')
                print(f' id {result_id} not in base i am write!')
                return False



def grab_top_meme():
    """
    Парсит картику мем
    :return: возвращает обьект метода content
    """
    soup_img = BeautifulSoup(get_request_html(url), 'lxml').find_all('div', class_='content_list')
    for i in soup_img:
        result_link = i.find('img').get('src')
        image_bytes = requests.get(f'{url}{result_link}').content
        return image_bytes


def main():
    count = 1
    while True:
        if not get_id():
            try:
                bot.send_photo(channel, grab_top_meme())
                print(f'отправил в канал {count} сообщение')
                count += 1
                time.sleep(600)
            except Exception as e:
                print(e)
                time.sleep(30)
        else:
            print('ждем новых мемов')
            time.sleep(600)
            continue


if __name__ == '__main__':
    main()
