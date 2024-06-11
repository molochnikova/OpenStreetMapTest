import pytest
from get_requests import GetCordAddress, GetDataJson
import logging
import allure


@allure.feature('Проверка соответствия получаемых данных')
@allure.story('Проверка прямого кодирования: адрес')
@pytest.mark.parametrize('index', [
    0,
    1,
    2,
])
def test_chek_address(index, get_api_search):
    """
    Проверяет, соответствуют ли полученные координаты адресу.
    """
    response = get_api_search.get_search('14%2C+Bradford+Road%2C+Upper+Pells%2C+Lewes%2C+East+Sussex%2C+England%2C+BN7+1RB%2C+United+Kingdom')

    with allure.step('Запрос отправлен, посмотрим код ответа'):
        get_req = GetCordAddress(response)
        get_req.send_req()

    with allure.step('Получим из файла values_search.json необходимые для тестирования значения: '):
        search = GetDataJson('values_search.json')
        search_dict = search.get_dict()

    with allure.step("Прочитаем полученный JSON и преобразуем его в объект стандартного типа данных Python"):
        test_json = GetCordAddress(response)

    with allure.step(f"Из обработанного ответа получим координаты"):
        coord = test_json.get_coord()
        logging.info(f'Из обработанного ответа были получены координаты {coord}')

    with (allure.step(f"Проверим полученные данные {coord}")):
        assert coord[0] == search_dict[index]['lat'] and coord[1] == search_dict[index]['lon'], 'Координаты не совпадают'


@allure.feature('Проверка соответствия получаемых данных')
@allure.story('Проверка геокодирования: координаты')
@pytest.mark.parametrize('index', [
    0,
    1,
    2,
])
def test_chek_coord(index, get_api_reverse):
    """
    Проверяет, соответствуют ли полученные координаты адресу.
    """

    response = get_api_reverse.get_reverse("50.8741261", "0.0006877111111111112")

    with allure.step('Запрос отправлен, посмотрим код ответа'):
        get_req = GetCordAddress(response)
        get_req.send_req()

    with allure.step('Получим из файла values_search.json необходимые для тестирования значения: '):
        search = GetDataJson('values_reverse.json')
        reverse_dict = search.get_dict()

    with allure.step("Прочитаем полученный JSON и преобразуем его в объект стандартного типа данных Python"):
        test_json = GetCordAddress(response)

    with allure.step(f"Из обработанного ответа получим адрес"):
        address = test_json.get_address()

    with (allure.step(f"Проверим полученные данные {address}")):
        assert address == reverse_dict[index]['address'], 'Адрес не совпадает'
