import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random


def main():
    vk_session = vk_api.VkApi(
        token='d793c36d91cff1c0f93a216c5a95549a62788fe1cc65cee98728d74d41d90afd3e5a5cfbd789227b6c1e2')
    #токен к моему сообществу
    longpoll = VkBotLongPoll(vk_session, '193282244')

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            print(event)
            print('Новое сообщение:')
            print('Для меня от:', event.obj.message['from_id'])
            print('Текст:', event.obj.message['text'])
            vk = vk_session.get_api()
            name = vk.users.get(user_id=event.obj.message['from_id'])[0]['first_name']
            try:
                city = vk.users.get(user_id=event.obj.message['from_id'], fields=['city'])[0]['city']['title']
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"Привет, {name}!\n"
                                         f"Как поживает {city}?",
                                 random_id=random.randint(0, 2 ** 64))
            except:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"Привет, {name}!",
                                 random_id=random.randint(0, 2 ** 64))


if __name__ == '__main__':
    main()