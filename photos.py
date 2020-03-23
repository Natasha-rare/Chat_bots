import vk_api


def main():
    login, password = '79772992982', 'nlaalnooн'
    vk_session = vk_api.VkApi(login, password)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    upload = vk_api.VkUpload(vk_session)
    photos = ['static/img/pic_cat.jpg', 'static/img/kitten.jpg']

    for item in photos:
        photo = upload.photo(
            item,
            album_id=457239018,
            group_id=193282244
        )
        vk_photo_url = 'https://vk.com/photo{}_{}'.format(
            photo[0]['owner_id'], photo[0]['id']
        )
        vk_photo_id = f"photo{photo[0]['owner_id']}_{photo[0]['id']}"

        print(photo, vk_photo_id, vk_photo_url, sep="\n")
        vk = vk_session.get_api()
        vk.wall.post(message="Cats", attachments=[vk_photo_id])


if __name__ == '__main__':
    main()