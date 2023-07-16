from pprint import pprint
#импорты
import vk_api
from vk_api.exceptions import ApiError

from config import acces_token

#получение данных о пользователе

class VkTools():
    def __init__(self, acces_token):
        self.vkapi = vk_api.VkApi(token=acces_token)

    def get_profile_info(self, user_id):
        try:
            info, = self.vkapi.method('users.get',
                                    {'user_id': user_id,
                                    'fields': 'city, sex, bdate, relation'
                                    }
                                    )
        except ApiError as e:
            info = {}
            print(f'error = {e}')

        result = {'name': info['first_name'] + ' ' + info['last_name'],
                     # 'id': info['id'],
                     # 'bdate': info['bdate'] if 'bdate' in info else None,
                     # 'home_town': info['home_town'],
                     'sex': info['sex'],
                     'city': info['city']['title'],
                     'bdate': info['bdate']
                     }
        return result
    #
    # def serch_users(self, params):
    #
    #     sex = 1 if params['sex'] == 2 else 2
    #     city = params['city']
    #     curent_year = datetime.now().year
    #     user_year = int(params['bdate'].split('.')[2])
    #     age = curent_year - user_year
    #     age_from = age - 5
    #     age_to = age + 5
    #
    #     users = self.api.method('users.search',
    #                             {'count': 10,
    #                              'offset': 0,
    #                              'age_from': age_from,
    #                              'age_to': age_to,
    #                              'sex': sex,
    #                              'city': city,
    #                              'status': 6,
    #                              'is_closed': False
    #                              }
    #                             )
    #     try:
    #         users = users['items']
    #     except KeyError:
    #         return []
    #
    #     res = []
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

    pprint(params)
    # bot = VkTools(acces_token)
    # params = bot.get_profile_info(789657038)
    # users = bot.serch_users(params)
    # print(bot.get_photos(users[2]['id']))