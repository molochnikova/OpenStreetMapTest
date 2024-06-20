import pytest
import requests
import logging
import json


class GetCordAddress:
    """
    Отправка на сервер запроса для извлечения данных,
    преобразование данных в json
    и получение адреса и координат
    """
    def __init__(self, url):
        self.url = url
        self.response = requests.get(self.url, timeout=20)
        self.response_text = self.response.text
        self.response_json = json.loads(self.response_text)

    def send_req(self):
        print(self.response.status_code)
        try:
            if self.response.status_code == 200:
                logging.info(f'[{self.response.status_code}] - веб-сервер успешно обработал запрос')
                return True
            else:
                raise Exception("Ошибка при проверки статуса сайта")
        except Exception as e:
            logging.error(f'[{self.response.status_code}] - веб-сервер не обработал запрос, {e}')
            return False

    def get_coord(self):
        coord_lat = self.response_json[0]['lat']
        coord_lon = self.response_json[0]['lon']
        return coord_lat, coord_lon

    def get_address(self):
        return self.response_json['display_name']


def get_dict(file_json):
    with open(file_json) as file:
        dict_values = json.load(file)
        return dict_values

