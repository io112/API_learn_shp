from vk_api import VkApi
from vk_api.vk_api import VkApiMethod


def get_credentials():
    with open('../secrets.txt') as secrets:
        login = secrets.readline().strip()
        password = secrets.readline().strip()
        return login, password


def get_posts(vk: VkApiMethod):
    posts = vk.wall.get(domain='paramonod', count=5)
    print(f'На странице {posts["count"]} постов. ')
    for post in posts['items']:
        print(f'- {post["text"]}')


def get_last_post_id(vk: VkApiMethod):
    posts = vk.wall.get(domain='paramonod', count=1)
    if len(posts["items"]) == 0:
        print('Постов нет!')
        return
    return posts["items"][0]['id']


def set_like(vk: VkApiMethod, item_id: int):
    vk.likes.add(type='post', item_id=item_id)
    print('like set')


def del_like(vk: VkApiMethod, item_id: int):
    vk.likes.delete(type='post', item_id=item_id)
    print('like deleted')


def find_countries(vk):
    countries = vk.database.getCountries(need_all=0, code='RU,GB')
    print(f'Найдено {countries["count"]} стран: ')
    for coutry in countries['items']:
        print(f'- {coutry["title"]}')


def main():
    session = VkApi(*get_credentials())
    session.auth()
    vk = session.get_api()
    vk: VkApiMethod
    find_countries(vk)
    get_posts(vk)
    set_like(vk, get_last_post_id(vk))
    del_like(vk, get_last_post_id(vk))


if __name__ == '__main__':
    main()
