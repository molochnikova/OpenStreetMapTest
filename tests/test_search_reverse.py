import pytest
import json
from get_requests import GetCordAddress
import logging
from requests.exceptions import HTTPError
import allure


@allure.feature('Получение координат')
@allure.story('Проверка всякая такая разная')
@pytest.mark.parametrize('index', [0,
                                   1,
                                   2,
                                   ])
def test_chek_address(index, get_api_search):
    """
    Проверяет, соответствуют ли полученные координаты адресу.
    """
    response = get_api_search.get_search('14%2C+Bradford+Road%2C+Upper+Pells%2C+Lewes%2C+East+Sussex%2C+England%2C+BN7+1RB%2C+United+Kingdom')
    with allure.step('Запрос отправлен, посмотрим код ответа:'):
        try:
            for _ in range(3):
                response.raise_for_status()       # если ответ успешен, исключения задействованы не будут
                logging.info(f'[{response.status_code}] - веб-сервер успешно обработал запрос')
        except HTTPError as http_err:
            logging.warning (f'HTTP error occurred: {http_err}')
    with open('values_search.json') as file:
        search_dict = json.load(file)
        logging.info(f'Получение данных для тестирования в формате json {search_dict}')
    with allure.step("Прочитаем полученный JSON и преобразуем его в объект стандартного типа данных Python"):
        response = response.text
        test_json = GetCordAddress(response)
    with allure.step(f"Получим координаты:"):
        coord = test_json.get_coord()
        logging.info(f'Из обработанного ответа были получены координаты: {coord.text}')
    with allure.step(f"Проверим полученные данные:"):
        assert coord[0] == search_dict[index]['lat'] and coord[1] == search_dict[index]['lon'], logging.warning(f'В соответствии с адресом: "14, Bradford Road, Upper Pells, Lewes, East Sussex, England, BN7 1RB, United Kingdom"'
                                                                   f'с сервера получены координаты {coord}, '
                                                                   f'не совпадает с координатами указанными в values_search.json')


@allure.feature('Получение адреса')
@allure.story('Проверка')
@pytest.mark.parametrize('index', [0,
                                   1,
                                   2,
                                   ])
def test_chek_coord(index, get_api_reverse):
    """
    Проверяет, соответствуют ли полученные координаты адресу.
    """

    response = get_api_reverse.get_reverse("50.8741261", "0.0006877111111111112")
    with allure.step('Запрос отправлен, посмотрим код ответа:'):
        try:
            for _ in range(3):
                response.raise_for_status()       # если ответ успешен, исключения задействованы не будут
                logging.info(f'[{response.status_code}] - веб-сервер успешно обработал запрос')
        except HTTPError as http_err:
            logging.warning (f'HTTP error occurred: {http_err}')
    with open('values_reverse.json') as file:
        reverse_dict = json.load(file)
        logging.info(f'Получение данных для тестирования в формате json {reverse_dict}')
    with allure.step("Прочитаем полученный JSON и преобразуем его в объект стандартного типа данных Python"):
        response = response.text
        test_json = GetCordAddress(response)
    with allure.step(f"Получим адрес:"):
        address = test_json.get_address()
    assert address == reverse_dict[index]['address'], logging.warning(f'В соответствии с коррдинатами: lat = 50.8741261, lon = 0.0006877111111111112'
                                                                   f'с сервера получен адрес {address}, '
                                                                   f'не совпадает с адресом указанном в файле values_reverse.json')