import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random


from auth_data import TOKEN, group_id, VK_PASS, VK_USER, album_id

from io import BytesIO
# Этот класс поможет нам сделать картинку из потока байт

import requests
from PIL import Image


def geo(toponym_to_find):
    login, password = VK_USER, VK_PASS
    vk_session = vk_api.VkApi(login, password)
    vk = vk_session.get_api()
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        # обработка ошибочной ситуации
        pass

    # Преобразуем ответ в json-объект
    json_response = response.json()
    # Получаем первый топоним из ответа геокодера.
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    # Координаты центра топонима:
    toponym_coodrinates = toponym["Point"]["pos"]
    # Долгота и широта:
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

    delta = "0.005"

    # Собираем параметры для запроса к StaticMapsAPI:
    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "spn": ",".join([delta, delta]),
        "l": "map"
    }

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    # ... и выполняем запрос

    response = requests.get(map_api_server, params=map_params)
    upload = vk_api.VkUpload(vk_session)

    photo = upload.photo(  # Подставьте свои данные
        Image.open(BytesIO(response.content)),
        album_id=album_id,
        group_id=group_id
    )

    vk_photo_url = 'https://vk.com/photo{}_{}'.format(
        photo[0]['owner_id'], photo[0]['id']
    )

    upload_url = vk.photos.getWallUploadServer(group_id=group_id)['upload_url']
    photo = vk.photos.saveMessagesPhoto(server=upload_url['server'],
                                        photo=upload_url['photo'],
                                        hash=upload_url['hash'])

    return f'photo{photo["owner_id"]}_{photo["photo_id"]}'




def main():
    vk_session = vk_api.VkApi(
        token=TOKEN)

    longpoll = VkBotLongPoll(vk_session, group_id)
    n = 0
    city = ''
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            vk = vk_session.get_api()
            if n == 0:

                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message="Введите название местности",
                                 random_id=random.randint(0, 2 ** 64))
                n += 1
            elif n == 1:
                city = event.obj.message['text']
                vk = vk_session.get_api()

                vk.messages.send(
                    user_id=event.obj.message['from_id'],
                    message='Выберите тип карты',
                    random_id=random.randint(0, 2 ** 64),
                    keyboard=open('keyboard.json', "r", encoding="UTF-8").read()
                )
                n += 1
            else:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"Это {city}. Что вы еще хотите увидеть?",
                                 random_id=random.randint(0, 2 ** 64),
                                 keyboard={"buttons": [], "one_time": "true"},
                                 attachment=geo(city))
                n = 0


if __name__ == '__main__':
    main()