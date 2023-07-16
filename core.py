from pprint import pprint
from  datetime import  datetime #определять возраст
#импорты
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
        except ApiError as e:
            info = {}
            print(f'error = {e}')

        result = {'name': info['first_name'] + ' ' + info['last_name'] if
                  'first_name' in info and 'last_name' in info else None,
                     # 'id': info['id'],
                     # 'bdate': info['bdate'] if 'bdate' in info else None,
                     # 'home_town': info['home_town'],
                     'sex': info.get('sex'),
                     'city': info.get('city')['title'] if info.get('city') is not None else None,
                     'year': self._bdate_toyear(info.get('bdate'))
                     }
        return result

    def serch_worksheet(self, params):  #находим пользователей
        try:
            users = self.vkapi.method('users.search',
                                    {'count': 50,
                                     'hometown': params['city'],
                                     'sex': 1 if params['sex'] ==2 else 2,
                                     'has_photo': True,
                                     'age_from': params['year'] - 3,
                                     'age_to': params['year'] + 3,
                                     }
                                     )
        except ApiError as e:
            info = []
            print(f'error = {e}')

        result = [{'name': item['first_name'] + ' ' + item['last_name'],
                   'id': item['id']
                   } for item in users['items'] if item['is_closed'] is False
                  ]

        return result



        # try:
        #     users = users['items']
        # except KeyError:
        #     return []

        # res = []
    #
    #     for user in users:
    #         if user['is_closed'] == False:
    #             res.append({'id': user['id'],
    #                         'name': user['first_name'] + ' ' + user['last_name']
    #                         }
    #                        )
    #
    #     return res
    #
    # def get_photos(self, user_id):
    #     photos = self.api.method('photos.get',
    #                              {'user_id': user_id,
    #                               'album_id': 'profile',
    #                               'extended': 1
    #                               }
    #                              )
    #     try:
    #         photos = photos['items']
    #     except KeyError:
    #         return []
    #
    #     res = []
    #
    #     for photo in photos:
    #         res.append({'owner_id': photo['owner_id'],
    #                     'id': photo['id'],
    #                     'likes': photo['likes']['count'],
    #                     'comments': photo['comments']['count'],
    #                     }
    #                    )
    #
    #     res.sort(key=lambda x: x['likes'] + x['comments'] * 10, reverse=True)
    #
    #     return res
    #

if __name__ == '__main__':
    user_id = 807607725
    tools = VkTools(acces_token)
    params = tools.get_profile_info(user_id)
    worksheet = tools.serch_worksheet(params)

    pprint(worksheet)
    # bot = VkTools(acces_token)
    # params = bot.get_profile_info(789657038)
    # users = bot.serch_users(params)
    # print(bot.get_photos(users[2]['id']))