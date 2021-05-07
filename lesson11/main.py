import sys
from random import Random

from vk_api import VkApi, Captcha, VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.vk_api import VkApiMethod

rnd = Random()


def get_credentials():
    with open('../secrets.txt') as secrets:
        login = secrets.readline().strip()
        password = secrets.readline().strip()
        return login, password


def get_2fa_code():
    code = input("Введите код авторизации: ")
    remember_me = True
    return code, remember_me


def get_captcha_code(captcha: Captcha):
    ans = input(f"Пройдите капчу по следующему адресу: {captcha.get_url()}\nВведите код: ")
    return captcha.try_again(ans)


def upload_test_photo(vk):
    album_id = '279352419'
    upload = VkUpload(vk)
    upload.photo('C:\\1.jpg', album_id=album_id)


def upload_group_photo(vk):
    group_id = '204321727'
    album_id = '278056166'
    upload = VkUpload(vk)
    upload.photo('C:\\1.jpg', group_id=group_id, album_id=album_id)


def long_poll_example():
    user_id = '100447269'
    api_key = '3cb8e11bf17fb9d7c2d8afbf1943e1d7cbde743e807d5633ca99a57c4992bd0bdd264bcae806e29fe3464'
    session = VkApi(token=api_key)
    vk = session.get_api()
    v = [str(item) for item in vk.messages.search(q='hi')['items']]
    for i in v:
        print(i)
    lp = VkLongPoll(session)
    print('Запускаю LongPoll')
    for event in lp.listen():
        print(event.type)
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                print(f'Вам письмо: {event.text}')
                vk.messages.send(user_id=event.user_id,
                                 random_id=rnd.randint(0, 20000000000),
                                 message='Hi')
            elif event.from_me:
                print(f'Вы написали: {event.text}')


def user_example():
    session = VkApi(*get_credentials(), auth_handler=get_2fa_code, captcha_handler=get_captcha_code)
    session.auth()
    vk: VkApiMethod = session.get_api()
    upload_test_photo(vk)
    upload_group_photo(vk)


def main():
    if sys.argv[1] == '--user':
        user_example()
    elif sys.argv[1] == '--bot':
        long_poll_example()
    else:
        print('Неверная команда')


if __name__ == '__main__':
    main()
