import pytest
import json
import logging
import allure


def get_dict_search(file_json):
    with open(file_json) as file:
        search_dict = json.load(file)

        logging.info(f'Получение данных для тестирования в формате json {search_dict}')
        return search_dict


@allure.feature('Проверка соответствия получаемых данных')
@allure.story('Проверка прямого кодирования: адрес')
@pytest.mark.parametrize('search_dict_lat', 'search_dict_lon'[

])
def test_chek_address(search_dict):
    """
    Проверяет, соответствуют ли полученные координаты адресу.
    """
    response = GetCordAddress('https://nominatim.openstreetmap.org/search?q=14%2C+Bradford+Road%2C+Upper+Pells%2C+Lewes%2C+East+Sussex%2C+England%2C+BN7+1RB%2C+United+Kingdom&'
                              'format=json&addressdetails=1&limit=1')

    with allure.step('Запрос отправлен, посмотрим код ответа'):
        response.send_req()

    #with allure.step('Получим из файла values_search.json необходимые для тестирования значения: '):
     #   search = GetDataJson('../values_search.json')
      #  search_dict = search.get_dict()
    # with allure.step("Прочитаем полученный JSON и преобразуем его в объект стандартного типа данных Python"):
    #     test_json = response.

    with allure.step(f"Из обработанного ответа получим координаты"):
        coord = response.get_coord()
        logging.info(f'Из обработанного ответа были получены координаты {coord}')

    with (allure.step(f"Проверим полученные данные {coord}")):
        assert coord[0] == search_dict_lat and coord[1] == search_dict_lon, 'Координаты не совпадают'


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

    response = get_api_reverse.get_reverse('https://nominatim.openstreetmap.org/reverse?'
                                           'format=json&lat=50.8741261&lon=0.0006877111111111112')

    with allure.step('Запрос отправлен, посмотрим код ответа'):
        get_req = GetCordAddress(response)
        get_req.send_req()

    with allure.step('Получим из файла values_search.json необходимые для тестирования значения: '):
        search = GetDataJson('../values_reverse.json')
        reverse_dict = search.get_dict()

    with allure.step("Прочитаем полученный JSON и преобразуем его в объект стандартного типа данных Python"):
        test_json = GetCordAddress(response)

    with allure.step(f"Из обработанного ответа получим адрес"):
        address = test_json.get_address()

    with (allure.step(f"Проверим полученные данные {address}")):
        assert address == reverse_dict[index]['address'], 'Адрес не совпадает'
