import json


class GetCordAddress:
    """
    Отправка на сервер запроса для извлечения данных,
    преобразование данных в json
    и получение адреса и координат
    """
    def __init__(self, response):
        self.response_json = json.loads(response)

    def get_coord(self):
        coord_lat = self.response_json[0]['lat']
        coord_lon = self.response_json[0]['lon']
        return coord_lat, coord_lon

    def get_address(self):
        return self.response_json['display_name']

#https://nominatim.openstreetmap.org/search?q=Unter%20den%20Linden%201%20Berlin&format=json&addressdetails=1&limit=1&polygon_svg=1