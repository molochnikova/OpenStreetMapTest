import json
import logging





# class GetDataJson:
#     def __init__(self, file_json):
#         self.file_json = file_json
#
#     def get_dict(self):
#         with open(self.file_json) as file:
#             search_reverse_dict = json.load(file)
#             logging.info(f'Получение данных для тестирования в формате json {search_reverse_dict}')
#             return search_reverse_dict


class ApiClient:
    """
    Преобразование полученного адреса или координат в нужный формат url
    """
    def __init__(self, base_address):
        self.base_address = base_address

    def get_search(self, q):
        url = f"{self.base_address}q={q}&format=json&addressdetails=1&limit=1"
        logging.info(f'Получен url: {url}')
        return requests.get(url, timeout=20)

    def get_reverse(self, lat, lon):
        url = f"{self.base_address}format=json&lat={lat}&lon={lon}"
        logging.info(f'Получен url: {url}')
        return requests.get(url, timeout=20)