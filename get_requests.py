import json
import logging
from requests.exceptions import HTTPError


class GetCordAddress:
    """
    Отправка на сервер запроса для извлечения данных,
    преобразование данных в json
    и получение адреса и координат
    """
    def __init__(self, response):
        self.response = response
        self.response_text = response.text
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


class GetDataJson:
    def __init__(self, file_json):
        self.file_json = file_json

    def get_dict(self):
        with open(self.file_json) as file:
            search_reverse_dict = json.load(file)
            logging.info(f'Получение данных для тестирования в формате json {search_reverse_dict}')
            return search_reverse_dict


