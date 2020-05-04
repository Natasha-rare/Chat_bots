'''
пример загрузки изображения и создания сообщения с ним на стену
'''
import vk_api
from random import randint
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from auth_data import TOKEN, group_id, VK_USER, VK_PASS, album_id
import sys

def photo_id():
    login, password = VK_USER, VK_PASS
    vk_session = vk_api.VkApi(login, password)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    vk = vk_session.get_api()
    response = vk.photos.get(album_id=album_id, group_id=group_id)
    photo = response[randint(0, len(response) - 1)]
    return f"photo{photo['owner_id']}_{photo['photo_id']}"


def main():
    vk_session = vk_api.VkApi(
        token=TOKEN)

    longpoll = VkBotLongPoll(vk_session, group_id)


    # Используем метод wall.get
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            vk = vk_session.get_api()
            vk.messages.send(user_id=event.obj.message['from_id'],
                             message="Случайное фото из альбома:",
                             attachment=photo_id())


if __name__ == '__main__':
    main()