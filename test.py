import vk_api
import json

def auth_handler():
    """ При двухфакторной аутентификации вызывается эта функция. """

    # Код двухфакторной аутентификации,
    # который присылается по смс или уведомлением в мобильное приложение
    key = input("Enter authentication code: ")
    # Если: True - сохранить, False - не сохранять.
    remember_device = True

    return key, remember_device


import vk_api
import datetime


def main():
    login, password = 79772992982, 'nlaalnooн' # здесь настоящие данные пользователя
    vk_session = vk_api.VkApi(login, password)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    vk = vk_session.get_api()
    response = vk.friends.get(fields="bdate, city")['items']
    resp = sorted(response, key=lambda x: x['last_name'])
    for i in resp:
        try:
            print(i['last_name'], i['first_name'], i['bdate'])
        except:
            print(i['last_name'], i['first_name'])


if __name__ == '__main__':
    main()