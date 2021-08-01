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
    print(f'result_id = {result_id}')
    return result_id


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
    global con
    try:
        con = sqlite3.connect('id_database.db')  # создаем базу и коннект к ней

        cursor = con.cursor()  #  создаем курсор

        cursor.execute("""CREATE TABLE IF NOT EXISTS id_picture (id TEXT)""")  # создаем команду
        con.commit()  # комитим

        cursor.execute("SELECT * FROM id_picture WHERE id = ?", (result_id,))

        if cursor.fetchone() is None:  # если нет записи с result_id
            cursor.execute("INSERT INTO id_picture VALUES (?)", (result_id,))
            con.commit()
            bot.send_photo(channel, grab_top_meme())
            print(f'отправил сообщение {result_id}')
            time.sleep(400)
        else:
            print(f'Такая запись {result_id} уже есть')
            time.sleep(400)
    except Error:
        print(Error)
    finally:
        con.commit()
        con.close()


def main():

        while True:
            try:
                sql_connection(get_id())
                continue
            except Exception as e:
                print('Error in main func', e)
                continue

if __name__ == '__main__':
    main()
