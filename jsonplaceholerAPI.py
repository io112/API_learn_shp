import requests
import json


class JSONPlaceholderAPI:
    URL = 'http://jsonplaceholder.typicode.com'

    def get_all_posts(self) -> list:
        s = requests.get(self.URL + '/posts')
        if s.status_code != 200:
            print('Error:', s.status_code)
            return []
        res = json.loads(s.content)
        return res

    def get_all_users(self) -> list:
        s = requests.get(self.URL + '/users')
        if s.status_code != 200:
            print('Error:', s.status_code)
            return []
        res = json.loads(s.content)
        return res

    def get_post(self, id) -> dict:
        s = requests.get(f'{self.URL}/posts/{id}')
        if s.status_code != 200:
            print('Error:', s.status_code)
            return {}
        res = json.loads(s.content)
        return res

    def get_users(self, id) -> dict:
        s = requests.get(f'{self.URL}/users/{id}')
        if s.status_code != 200:
            print('Error:', s.status_code)
            return {}
        res = json.loads(s.content)
        return res


def main():
    api = JSONPlaceholderAPI()
    print(api.get_post(101))


if __name__ == '__main__':
    main()
