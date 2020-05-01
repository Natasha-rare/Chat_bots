import vk_api
from auth_data import VK_USER, VK_PASS, album_id, group_id

def main():
    login, password = VK_USER, VK_PASS
    vk_session = vk_api.VkApi(login, password)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    vk = vk_session.get_api()
    response = vk.photos.get(album_id=album_id, group_id=group_id)['items']
    for image in response:
        print(f"url: {image['sizes'][-1]['url']}, size:{image['sizes'][-1]['width']} X {image['sizes'][-1]['height']}")


if __name__ == '__main__':
    main()
