import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import datetime
import pytz

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
            weekday = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
            date = datetime.datetime.now()
            if 'время' in event.obj.message['text'] or 'число' in event.obj.message['text'] or \
               'дата' in event.obj.message['text'] or 'день' in event.obj.message['text']:
                message = f"Сегодня {str(date).split()[0]}, {weekday[date.weekday()]}\n" \
                          f"Время {str(date).split()[1].split('.')[0]}"
                vk.messages.send(user_id=event.obj.message['from_id'],
                             message=message,
                             random_id=random.randint(0, 2 ** 64))
            else:
                message = 'Я умею говорить дату и время. ' \
                          'Для этого в твоем сообщении должны быть слова: ' \
                          '"время", "дата", "число" или "день" '
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=message,
                                 random_id=random.randint(0, 2 ** 64))

if __name__ == '__main__':
    main()