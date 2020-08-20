import data_table
import user
import requests
import time
import json
import gettoken


def get_photos(User):
    final_dict = {}
    for id in User.get_id_list():
        params = {
            'access_token': User.TOKEN,
            'v': 5.89,
            'owner_id': id,
            'album_id': 'profile',
            'extended': 1
        }
        # Здесь я беру все фотографии из аватарок у пользователя по айдишнику
        time.sleep(1)
        response = requests.get('https://api.vk.com/method/photos.get', params=params).json()
        try:
            photos = response['response']['items']
        except KeyError:
            continue
        # Здесь я создаю словарь, в который собираю пары индекс фотки: количество лайков+комментов
        photo_dict = {}
        for item in range(len(photos)):
            photo_dict[item] = photos[item]['likes']['count']+photos[item]['comments']['count']
        # Здесь я сортирую все полученные фотки, выбираю топ-3 по количеству лайков и нахожу их индексы в своем словаре
        top_3 = sorted(photo_dict.values())[-3:]
        indexes = [k for k,v in photo_dict.items() if v in top_3]
        # Здесь я забиваю финальный словарь парами юзер_айди: список со ссылками на топ-3 фоток
        final_dict['vk.com/id' + str(photos[0]['owner_id'])] = []
        for index in indexes:
            final_dict['vk.com/id' + str(photos[0]['owner_id'])].append(photos[index]['sizes'][-1]['url'])
    return(final_dict)

def dump_to_json(dict, filename):
    #эту функцию можно использовать как для кэширования промежуточного результата из функции get_photos()
    #Так и для получения финального результата из фунции get_random_people модуля data_table.py
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(dict, f, ensure_ascii=False)
    return filename



if __name__ == '__main__':
    id = input('Введите свой id: ')
    print('Пройдите по этой ссылке и скопируйте токен из строки браузера: ')
    print(gettoken.get_token(id))
    TOKEN = input()
    user = user.User(id, TOKEN)
    dump_to_json(get_photos(user), 'found_users.json')
    data_table.create_db()
    data_table.add_user('found_users.json')
    print(data_table.get_random_people())

