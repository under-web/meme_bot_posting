import time
import requests
import telebot
import sqlite3
from sqlite3 import Error
from bs4 import BeautifulSoup
from config import api_token, channel

url = 'https://topmemas.top/'
bot = telebot.TeleBot(api_token)


def get_request_html(url):
    res = requests.get(url).text
    return res


def get_id():  # парсит id для определения актуальности мема
    """
    Проверяет есть ли id  в списке файла,
    :return: если есть ждем когда появится новый, если нет записываем его в базу
    """
    soup_id = BeautifulSoup(get_request_html(url), 'lxml').find_all('div', class_='cont_item')
    result_id = soup_id[0].get('id')
    return result_id
    # with open('id.txt', 'r', encoding='utf-8') as r_file:
    #     ids = r_file.readlines()
    #     if ids is None:
    #         r_file.writelines(str(result_id) + '\n')
    #         print('base impty, i am write')
    #         return False
    #     else:
    #         if str(result_id) + '\n' in ids:
    #             print(f'id - {result_id} in base!')
    #             return True
    #         else:
    #             with open('id.txt', 'a', encoding='utf-8') as file:
    #                 file.writelines(str(result_id) + '\n')
    #             print(f' id {result_id} not in base i am write!')
    #             return False


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


def sql_connection(result_id):
    try:
        con = sqlite3.connect('id_database.db')

        cursor = con.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS id_picture (id TEXT)""")
        con.commit()

        cursor.execute("SELECT id FROM id_picture")

        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO id_picture VALUES (?)", (result_id,))
            con.commit()
            bot.send_photo(channel, grab_top_meme())
            print(f'отправил сообщение')
            time.sleep(600)
        else:
            print('Такая запись уже есть')
            time.sleep(600)
    except Error:
        print(Error)
    finally:
        con.close()


def main():

    while True:
        sql_connection(get_id())
        continue


if __name__ == '__main__':
    main()
