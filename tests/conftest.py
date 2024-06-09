import pytest
import requests


class ApiClient:
    def __init__(self, base_address):
        self.base_address = base_address

    def get_search(self, q):
        url = f"{self.base_address}q={q}&format=json"
        return requests.get(url)

    def get_reverse(self, lat, lon):
        url = f"{self.base_address}format=json&lat={lat}&lon={lon}"
        return requests.get(url)


@pytest.fixture
def get_api_search():
    return ApiClient(base_address="https://nominatim.openstreetmap.org/search?")


@pytest.fixture
def get_api_reverse():
    return ApiClient(base_address="https://nominatim.openstreetmap.org/reverse?")