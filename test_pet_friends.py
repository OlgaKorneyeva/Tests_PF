from api import PetFriends
import pytest
from settings import valid_email, invalid_email, valid_password, invalid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этот ключ
    запрашиваем список всех питомцев и проверяем, что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Семён', animal_type='зяблик',
                                     age='4', pet_photo='images\\zyablik.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Лось", "Павел", "49", "images/pavlik.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Фунтик', animal_type='поросёнок', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

"""TESTS"""

def test_get_api_key_for_invalid_user(email=invalid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает ошибку 403 и сообщение, что логин или пароль неверный"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    #assert 'key' in result

def test_get_api_key_for_invalid_user(email=valid_email, password=invalid_password):
    """ Проверяем что запрос api ключа возвращает ошибку 403 и сообщение, что логин или пароль неверный"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    #assert 'key' in result

def test_create_pet_simple_without_photo_with_uncorrected_data(name='Фунтик', animal_type='поросёнок', age='ололо'):
     """Проверяем, что можно добавить информацию о новом питомце без фото, указав неверный формат раздела Возраст"""

     # Запрашиваем ключ api и сохраняем в переменую auth_key
     _, auth_key = pf.get_api_key(valid_email, valid_password)

     # Добавляем питомца без фото
     status, result = pf.create_pet_simple_without_photo(auth_key, name, animal_type, age)

     # Сверяем полученный ответ с ожидаемым результатом
     # есть ошибка на стороне сервера
     assert status == 400



def test_create_pet_simple_without_photo_auth_invalid(name='Фунтик', animal_type='поросёнок', age='2'):
    """Проверяем, что можно добавить информацию о новом питомце без фото"""

    # Не запрашиваем ключ api и не сохраняем в переменую auth_key, допустив ошибку в ключе
    #_, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца без фото
    status, result = pf.create_pet_simple_without_photo({'key': 'invalid_auth_key'}, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403 #auth_key is incorrected


def test_add_pet_photo_in_invalid_format(name='Жорик', animal_type='дракон', age='5', pet_photo='images\\dragon.png'):
    """Проверяем возможность загрузки изображения в формате png"""
    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца с фото в формате png
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['pet_photo']== ''

def test_delete_pet_with_invalid_id(): #ВЕРНО ЛИ ЧТО ЗДЕСЬ ТОЛЬКО НА 160 СТРОЧКЕ INVALID ID?
    """Проверяем возможность удаления питомца с некорректным pet_id"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Берём некорректный id питомца из списка и отправляем запрос на удаление
    pet_id = 'invalid id'
    status, result = pf.delete_pet(auth_key, pet_id)

    # Проверяем что статус ответа не равен 200 и в списке питомцев данный питомец не найден
    # есть ошибка на стороне сервера
    assert status != 200

def test_get_api_key_for_unregistered_user(unregistered_email = "kurkuma@mail.ru", unregistered_password = "12345"):
    """ Проверяем что запрос api ключа возвращает ошибку 403 и сообщение, что логин или пароль неверный"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(unregistered_email, unregistered_password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    # assert 'key' in result

def test_create_new_pet_with_invalid_auth_key(name='fr', animal_type='fr',
                                     age='7', pet_photo='images\\beliberda.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую invalid auth_key (несколько раз вставлен в строку auth_key)
    _, invalid_auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(invalid_auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_get_list_of_pets_with_invalid_auth_key(filter=''):
    """ Проверяем что запрос моих питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную некорректный auth_key. Далее используя этот ключ
    запрашиваем список моих питомцев и проверяем, что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    # Запрашиваем ключ api и сохраняем в переменую invalid auth_key
    # (несколько раз вставлен в строку корректный auth_key).
    #Также запрашиваем список моих питомцев.
    invalid_auth_key = {'key': 'invalid_auth_key'}
    status, result = pf.get_list_of_pets(invalid_auth_key, filter)

    assert status == 403

def test_add_new_pet_with_uncorrected_data(name='++++++++++++++++++++++++++++++++++++++++++'
                                                '++++++++++++++++++++++++++++++++++++++++++'
                                                '++++++++++++++++++++++++++++++++++++++++++'
                                                '++++++++++++++++++++++++++++++++++++++++++'
                                                '+++++++++++++++++++++++++++++++++++++++++++'
                                                '+++++++++++++++++++++++++++++++++++++++++++'
                                                '+++++++++++++++++++++++++++++++++++++++++++'
                                                '+++++++++++++++++++++++++++++++++++++++++++'
                                                '+++++++++++++++++++++++++++++++++++++++++++'
                                                '+++++++++++++++++++++++++++++++++++++++++++'
                                                '+++++++++++++++++++++++++++++++++++++++++++'
                                                '+++++++++++++++++++++++++++++++++++++++++++'
                                                '+++++++++++++++++++++++++++++++++++++++',
                                           animal_type='крокодил', age='1'):
    """Проверяем, что можно добавить информацию о новом питомце, указав неверный формат раздела Имя"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца без фото
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, 'images\\krokodil.jpg')

    # Сверяем полученный ответ с ожидаемым результатом, ожидаем что сервер вернет ошибку
    assert status != 200




