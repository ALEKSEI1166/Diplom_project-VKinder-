#импорты

from pprint import pprint
from  datetime import  datetime #определять возраст
import vk_api
from vk_api.exceptions import ApiError
from config import acces_token


#получение данных о пользователе
class VkTools():
    def __init__(self, acces_token):
        self.vkapi = vk_api.VkApi(token=acces_token)


    def _bdate_toyear(selfs, bdate):
        user_year = bdate.split('.')[2]
        now = datetime.now().year
        return now - int(user_year)


    def get_profile_info(self, user_id):
        try:
            info, = self.vkapi.method('users.get',
                                     {'user_id': user_id,
                                      'fields': 'city,sex,bdate,relation'
                                     }
                                     )
        except KeyError as e:
            info = {}
            print(f'error = {e}')

        result = {'name': info['first_name'] + ' ' + info['last_name'] if
                  'first_name' in info and 'last_name' in info else None,
                  'sex': info.get('sex'),
                  'city': info.get('city')['title'] if info.get('city') is not None else None,
                  'year': self._bdate_toyear(info.get('bdate'))
                     }
        return result

    def search_worksheet(self, params, offset):  #находим пользователей
        try:
            users = self.vkapi.method('users.search',
                                    {'count': 50,
                                     'offset': offset,
                                     'hometown': params['city'],
                                     'sex': 1 if params['sex'] ==2 else 2,
                                     'has_photo': True,
                                     'age_from': params['year'] - 3,
                                     'age_to': params['year'] + 3,
                                     }
                                     )
        except KeyError as e:
            info = []
            print(f'error = {e}')

        result = [{'name': item['first_name'] + ' ' + item['last_name'],
                   'id': item['id']
                   } for item in users['items'] if item['is_closed'] is False #берем анкету если профиль не закрыт
                  ]

        return result


    def get_photos(self, id):  #поиск фото
        try:
                photos = self.vkapi.method('photos.get',
                                           {'owner_id': id,
                                            'album_id': 'profile',
                                            'extended': 1   #параметр говорит о том - какая информация нужна о фото
                                            }
                                            )
        except ApiError as e:
                photos = {}
                print(f'error = {e}')

        result = [{'owner_id': item['owner_id'],
                   'id': item['id'],
                   'likes': item['likes']['count'],
                   'comments': item['comments']['count']
                   } for item in photos['items']  #автоматический генератор листа
                  ]
        return result[:3]  # берем первые три анкеты

        '''сортировка по лайкам и комментам'''
        for photo in photos:
            res.append({'owner_id': photo['owner_id'],
                        'id': photo['id'],
                        'likes': photo['likes']['count'],
                        'comments': photo['comments']['count'],
                        }
                       )

        res.sort(key=lambda x: x['likes'] + x['comments'] * 10, reverse=True)

        return res



if __name__ == '__main__':
    user_id = 807607725
    tools = VkTools(acces_token)
    params = tools.get_profile_info(user_id)
    worksheets = tools.search_worksheet(params, 20)
    worksheet = worksheets.pop() #метод 'pop' берет последний элемент списка, сохранияет его в переменную, но при этом он ее удаляет из списка
    photos = tools.get_photos(worksheet['id'])

    pprint(worksheets)
