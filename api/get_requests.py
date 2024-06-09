import json


class GetCordAddress:
    def __init__(self, response):
        self.response_json = json.loads(response)

    def get_coord(self):
        coord_lat = self.response_json[0]['lat']
        coord_lon = self.response_json[0]['lon']
        return coord_lat, coord_lon

    def get_address(self):
        return self.response_json['display_name']