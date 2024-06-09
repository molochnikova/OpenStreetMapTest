import pytest
from api.get_requests import GetCordAddress
from api.values_search import address_search_values
from api.values_revers import address_reverse_values
import logging
from requests.exceptions import HTTPError


logger = logging.getLogger('py_log.log')
logger.setLevel(logging.INFO)

# настройка обработчика и форматировщика для logger
handler = logging.FileHandler('py_log.log', mode='w')
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

# добавление форматировщика к обработчику
handler.setFormatter(formatter)
# добавление обработчика к логгеру
logger.addHandler(handler)


@pytest.mark.parametrize('index', [0,
                                   1,
                                   2
                                   ])
def test_chek_address(index, get_api_search):
    """
    Проверяет, соответствуют ли полученные координаты адресу.
    """
    response = get_api_search.get_search(str(address_search_values[index]['q']))
    try:
        for _ in range(5):
            response.raise_for_status()       # если ответ успешен, исключения задействованы не будут
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        logger.error(f"Статус сайта: {response.status_code}")

    response = response.text
    test_json = GetCordAddress(response)
    coord = test_json.get_coord()
    assert coord[0] == address_search_values[index]['lat'] and coord[1] == address_search_values[index]['lon']


@pytest.mark.parametrize('index', [0,
                                   1,
                                   2
                                   ])
def test_chek_coord(index, get_api_reverse):
    """
    Проверяет, соответствуют ли полученные координаты адресу.
    """
    response = get_api_reverse.get_reverse(address_reverse_values[index]['lat'], address_reverse_values[index]['lon'])
    try:
        response.raise_for_status()    # Вызывает исключение, если код ответа не равен 200 (OK)
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        logger.error(f"Статус сайта: {response.status_code}")

    response = response.text
    test_json = GetCordAddress(response)
    address = test_json.get_address()
    assert address == address_reverse_values[index]['address'], logger.error("В соответствии с координатами, адрес неверный")