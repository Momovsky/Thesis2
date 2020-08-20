import requests
import time

class User:
    def __init__(self, user_id, TOKEN):
        self.TOKEN = TOKEN
        if str(user_id).isdigit():
            self.USER_ID = user_id
        else:
            time.sleep(2)
            self.params = {
                'access_token': self.TOKEN,
                'v': 5.89,
                'screen_name': user_id
            }
            response = requests.get('https://api.vk.com/method/utils.resolveScreenName', params=self.params).json()
            self.USER_ID = response['response']['object_id']
        self.params = {
            'access_token': self.TOKEN,
            'v': 5.89,
            'user_ids': self.USER_ID,
            'fields': 'sex, city, relation, bdate'
        }

    def get_info(self):
        response = requests.get('https://api.vk.com/method/users.get', params=self.params).json()
        self.sex = response['response'][0]['sex']
        self.bdate = (2020 - int(response['response'][0]['bdate'][-4:]))
        # Обрабатываем через ошибку только город, потому что пол и дату рождения ВКонтакте нельзя не задать.
        try:
            self.city = response['response'][0]['city']['id']
        except KeyError:
            self.city = input('Введите id вашего города')

    def search_for_pair(self):
        #Кириллица нужна, чтобы формировать при каждой итерации цикла новый запрос
        #Это поможет обойти ограничение в 1000 человек на один запрос
        #Также можно попробовать в цикле передавать в поле bdate каждый из 365 дней в году, это тоже
        #изменит запрос и будет иметь аналогичный эффект
        cyrillic_letters = ['а','б','в','г','д','е','ё','ж','з','и','й','к','л','м','н','о','п','р','с','т','у','ф','х','ц','ч','щ','ш','э','ю','я']
        self.get_info()
        for letter in cyrillic_letters:
            params = {
                'access_token': self.TOKEN,
                'v': 5.89,
                'q': letter,
                'sort': 0,
                'sex': 2 if self.sex==1 else 1,
                'count': 3,
                'age_from': self.bdate-3,
                'age_to': self.bdate+3,
                'has_photo': 1,
                'status': 6,
                'city': self.city,
                'is_closed': 0
            }
            time.sleep(2)
            response = requests.get('https://api.vk.com/method/users.search', params=params).json()
            yield response

    def get_id_list(self):
        id_set = set()
        for result in self.search_for_pair():
            for user in result['response']['items']:
                id_set.add(user['id'])
        return id_set




