# Вариант 1.
#from datetime import datetime

# import vk_api
#
# from config import acces_token
#
#
# class VkTools():
#     def __init__(self, acces_token):
#         self.api = vk_api.VkApi(token=acces_token)
#
#     def get_profile_info(self, user_id):
#
#         info, = self.api.method('users.get',
#                                 {'user_id': user_id,
#                                  'fields': 'city,bdate,sex,relation,home_town'
#                                  }
#                                 )
#         user_info = {'name': info['first_name'] + ' ' + info['last_name'],
#                      'id': info['id'],
#                      'bdate': info['bdate'] if 'bdate' in info else None,
#                      'home_town': info['home_town'],
#                      'sex': info['sex'],
#                      'city': info['city']['id']
#                      }
#         return user_info
#
#     def serch_users(self, params):
#
#         sex = 1 if params['sex'] == 2 else 2
#         city = params['city']
#         curent_year = datetime.now().year
#         user_year = int(params['bdate'].split('.')[2])
#         age = curent_year - user_year
#         age_from = age - 5
#         age_to = age + 5
#
#         users = self.api.method('users.search',
#                                 {'count': 10,
#                                  'offset': 0,
#                                  'age_from': age_from,
#                                  'age_to': age_to,
#                                  'sex': sex,
#                                  'city': city,
#                                  'status': 6,
#                                  'is_closed': False
#                                  }
#                                 )
#         try:
#             users = users['items']
#         except KeyError:
#             return []
#
#         res = []
#
#         for user in users:
#             if user['is_closed'] == False:
#                 res.append({'id': user['id'],
#                             'name': user['first_name'] + ' ' + user['last_name']
#                             }
#                            )
#
#         return res
#
#     def get_photos(self, user_id):
#         photos = self.api.method('photos.get',
#                                  {'user_id': user_id,
#                                   'album_id': 'profile',
#                                   'extended': 1
#                                   }
#                                  )
#         try:
#             photos = photos['items']
#         except KeyError:
#             return []
#
#         res = []
#
#         for photo in photos:
#             res.append({'owner_id': photo['owner_id'],
#                         'id': photo['id'],
#                         'likes': photo['likes']['count'],
#                         'comments': photo['comments']['count'],
#                         }
#                        )
#
#         res.sort(key=lambda x: x['likes'] + x['comments'] * 10, reverse=True)
#
#         return res
#
#
# if __name__ == '__main__':
#     bot = VkTools(acces_token)
#     params = bot.get_profile_info(789657038)
#     users = bot.serch_users(params)
#     print(bot.get_photos(users[2]['id']))


# Вариант 2.
#импорты
from pprint import pprint
from datetime import datetime  #библиотека для определения времени
import vk_api
from vk_api.exceptions import ApiError


from config import acces_token #импрортирую с config нужный мне токен (acces_token)

#получение данных о пользователе
class VkTools():   #делаю класс
    def __init__(self, acces_token):  #инициализирую его
       self.vkapi = vk_api.VkApi(token=acces_token)  #инициализую vkapi используя токен пользователя(acces_token)

    def _bdate_toyear(self, bdate):  #она сначала определяет возраст юзера
        user_year = bdate.split ('.')[2]  #день рождения(второй по списку - Индекс 2)
        now = datetime.now().year
        return now - int(user_year)


    def get_profile_info(self, user_id):  #делаю функцию для вызывания данных о пользователе
        try:
            info, = self.vkapi.method('users.get',    #вызываю метод "users.get"(информация о пользователе). Записываю ответ в переменную 'info'
                                   {'user_id': user_id, #передаём параметры которые мне нужны (город, пол, дата)
                                    'fields': 'city,sex,relation,bdate'
                                    }
                                   )
        except ApiError as e:
            info = {}
            print(f'error = {e}')

        result = dict(name=(info['first_name'] + ' ' + info[
            'last_name']) if 'first_name' in info and 'last_name' in info else None, sex=info.get('sex') is not None,
                      city=info.get('city')['title'] if info.get('city') is not None else None,
                      year=self._bdate_toyear(info.get('bdate')))
        return result  #возвращаю result (ответ)


    def search_worksheet(self, params, offset):  #будем искать анкеты
        try:
            users = self.vkapi.method("users.search",
                                      dict(count=50, offset=offset, hometown=params['city'],
                                           sex=1 if params['sex'] == 2 else 2, has_photo=True,
                                           age_from=params['year'] - 3, age_to=params['year'] + 3)
                                      )
        except KeyError as e:
            user = []
            print(f'error = {e}')

        result = []
        for item in users['items']:
            if item['is_closed'] is False:
                result.append({'name': item['first_name'] + item['last_name'],
                               'id': item['id']
                               })
        return result


    def get_photos(self, id):    #поиск фото
        try:
            photos = self.vkapi.method('photos.get',
                                   {'owner_id': id,
                                    'album_id': 'profile',
                                    'extended': 1 # этот параметр спрашивает-"какая информ о фото нам нужна?"
                                    }
                                   )
        except ApiError as e:
            photos = {}
            print(f'error = {e}')


        result = [{
                    'owner_id': item['owner_id'],  #owner_id -это id профиля
                    'id': item['id'],   #а это id самого фото
                    'likes': item['likes']['count'],  #лайки
                    'comments': item['comments']['count']  #комментарии
                  } for item in photos['items']  #автоматический генератор листа
                ]
        return result[:3]  # берем первые 3 фото

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
    worksheet = worksheets.pop()  #метод берет последний элемент списка,сохраняет его в переменную, но при этом удаляет её из списка
    photos = tools.get_photos(worksheet['id'])

    pprint(worksheets)