import pytest
import logging
import allure
from get_req import GetCordAddress, get_dict


@allure.feature('Проверка соответствия получаемых данных')
@allure.story('Проверка прямого кодирования: адрес')
@pytest.mark.parametrize('search_dict', get_dict('../values_search.json'))
def test_chek_address(search_dict):
    """
    Проверяет, соответствуют ли полученные координаты адресу.
    """
    response = GetCordAddress('https://nominatim.openstreetmap.org/search?q=14%2C+Bradford+Road%2C+Upper+Pells%2C+Lewes%2C+East+Sussex%2C+England%2C+BN7+1RB%2C+United+Kingdom&format=json&addressdetails=1&limit=1')

    with allure.step('Запрос отправлен, посмотрим код ответа'):
        response.send_req()

    with allure.step(f"Из обработанного ответа получим координаты"):
        coord = response.get_coord()
        logging.info(f'Из обработанного ответа были получены координаты {coord}')

    with (allure.step(f"Проверим полученные данные {coord}")):
        assert coord[0] == search_dict['lat'] and coord[1] == search_dict['lon'], 'Координаты не совпадают'


@allure.feature('Проверка соответствия получаемых данных')
@allure.story('Проверка обратного кодирования: координаты')
@pytest.mark.parametrize('reverse_dict', get_dict('../values_reverse.json'))
def test_chek_coord(reverse_dict):
    """
    Проверяет, соответствуют ли полученные координаты адресу.
    """
    response = GetCordAddress('https://nominatim.openstreetmap.org/reverse?format=json&lat=50.8741261&lon=0.0006877111111111112')

    with allure.step('Запрос отправлен, посмотрим код ответа'):
        response.send_req()

    with allure.step(f"Из обработанного ответа получим адрес"):
        address = response.get_address()
        logging.info(f'Из обработанного ответа были получены координаты {address}')

    with (allure.step(f"Проверим полученные данные {address}")):
        assert address == reverse_dict['address'], 'Адрес не совпадает'
