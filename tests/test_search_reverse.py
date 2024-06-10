import pytest
import json
from get_requests import GetCordAddress
import logging
from requests.exceptions import HTTPError
import allure

logger = logging.getLogger('py_log.log')
logger.setLevel(logging.INFO)

# настройка обработчика и форматировщика для logger
handler = logging.FileHandler('py_log.log', mode='w')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s')
    #"%(name)s %(asctime)s %(levelname)s %(message)s")

# добавление форматировщика к обработчику
handler.setFormatter(formatter)
# добавление обработчика к логгеру
logger.addHandler(handler)

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
        except HTTPError as http_err:
            logger.warning (f'HTTP error occurred: {http_err}')
    with open('values_search.json') as file:
        search_dict = json.load(file)
        logging.info(f'Получение данных для тестирования в формате json {search_dict}')
    with allure.step("Запрос отправлен. Десериализируем ответ из json в словарь."):
        response = response.text
        test_json = GetCordAddress(response)
    with allure.step(f"Посмотрим какие координаты получены из {test_json}"):
        coord = test_json.get_coord()
    with allure.step(f"Проверим полченные данные:"):
        assert coord[0] == search_dict[index]['lat'] and coord[1] == search_dict[index]['lon'], logger.warning(f'Полученные данные не верны')


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

    response = get_api_reverse.get_reverse("-34.44076", "-58.70521")
    try:
        response.raise_for_status()    # Вызывает исключение, если код ответа не равен 200 (OK)
    except HTTPError as http_err:
        logger.error(f'HTTP error occurred: {http_err}')
    with open('values_reverse.json') as file:
        reverse_dict = json.load(file)
        logging.info(f'Получение данных для тестирования в формате json {reverse_dict}')
    with allure.step("Запрос отправлен. Десериализируем ответ из json в словарь."):
        response = response.text
        test_json = GetCordAddress(response)
    with allure.step(f"Посмотрим какие координаты получены из {test_json}"):
        address = test_json.get_address()
    assert address == reverse_dict[index]['address'], logger.error(f'В соответствии с коррдинатами: lat = -34.44076, lon = -58.70521\n'
                                                                   f'с сервера получен адрес {address}, '
                                                                   f'не совпадает с адресом указанном в файле values_reverse.json')