# # Вариант 1.

# # импорты
# import vk_api
# from vk_api.longpoll import VkLongPoll, VkEventType
# from vk_api.utils import get_random_id
#
# from config import comunity_token, acces_token
# from core import VkTools
#
#
# class BotInterface():
#
#     def __init__(self, comunity_token, acces_token):
#         self.interface = vk_api.VkApi(token=comunity_token)
#         self.api = VkTools(acces_token)
#         self.params = None
#
#     def message_send(self, user_id, message, attachment=None):
#         self.interface.method('messages.send',
#                               {'user_id': user_id,
#                                'message': message,
#                                'attachment': attachment,
#                                'random_id': get_random_id()
#                                }
#                               )
#
#     def event_handler(self):
#         longpoll = VkLongPoll(self.interface)
#
#         for event in longpoll.listen():
#             if event.type == VkEventType.MESSAGE_NEW and event.to_me:
#                 command = event.text.lower()
#
#                 if command == 'привет':
#                     self.params = self.api.get_profile_info(event.user_id)
#                     self.message_send(event.user_id, f'здравствуй {self.params["name"]}')
#                 elif command == 'поиск':
#                     users = self.api.serch_users(self.params)
#                     user = users.pop()
#                     # здесь логика дял проверки бд
#                     photos_user = self.api.get_photos(user['id'])
#
#                     attachment = ''
#                     for num, photo in enumerate(photos_user):
#                         attachment += f'photo{photo["owner_id"]}_{photo["id"]}'
#                         if num == 2:
#                             break
#                     self.message_send(event.user_id,
#                                       f'Встречайте {user["name"]}',
#                                       attachment=attachment
#                                       )
#                     # здесь логика для добавленяи в бд
#                 elif command == 'пока':
#                     self.message_send(event.user_id, 'пока')
#                 else:
#                     self.message_send(event.user_id, 'команда не опознана')
#
#
# if __name__ == '__main__':
#     bot = BotInterface(comunity_token, acces_token)
#     bot.event_handler()



# # Вариант 2.

# импорты
import vk_api  #импорт vk_api(здесь задействованы все модули с которыми придется работать)
from vk_api.longpoll import VkLongPoll, VkEventType #из этого же пакета мы импортруем инструменты для работы с LongPoll
from vk_api.utils import get_random_id  #импортируем из утилит спецутилиту для генерации специального айдишника

from config import comunity_token, acces_token #берем из config comunity_token (это токен сообщества)
from core import VkTools
#отправка сообщений
vk = vk_api.VkApi(token=comunity_token)  #Здесь производим инициализацию нашей API-> получается обьект VK,из этого обьекта vk будем вызывать все методы.

class BotInterface():
    def __init__(self, comunity_token, acces_token):
        self.vk = vk_api.VkApi(token=comunity_token)
        self.longpoll = VkLongPoll(self.vk)
        self.vk_tools = VkTools(acces_token)  #определяем vk_tools
        self.params = {}  #пустой словарь
        self.worksheets = []
        self.offset = 0


    def message_send(self, user_id, message, attachment=None): #функция отправки соообщений
        self.vk.method('messages.send',  #она построена на методе'messages.send'. Здесь передаём название метода
               {'user_id': user_id,  #здесь (и ниже) передаём как "словарик" его основные параметры
                'message': message,
                'attachment': attachment,
                'random_id': get_random_id()
                }
                )

#обработка сообщений/получение сообщений
    def event_handler(self):
        for event in self.longpoll.listen(): #перебираем события в longpoll
            if event.type == VkEventType.MESSAGE_NEW and event.to_me: #если тип этого события (event.type)новое сообщениe (MESSAGE_NEW) и стоит to_me (личное сообщение боту)->
                if event.text.lower() == 'привет':
                    ''' логика для получения данных о пользователе'''
                    self.params = self.vk_tools.get_profile_info(event.user_id)
                    self.message_send(  #тогда он вызывает функцию message_send и по id пользователя он возвращает текст, кторый тот написал.
                        event.user_id, f'Привет друг, {self.params["name"]}')
                elif event.text.lower() == 'поиск':
                    ''' логика для поиска анкет'''
                    self.message_send(
                        event.user_id, 'Начинаем поиск')
                    if self.worksheets:
                        worksheet = self.worksheets.pop()  # берем любую анкету

                        'проверка анкеты в БД в соответствии с event.user_id'
                        # worksheet = 50 # объявление переменной 'worksheet' для условия цикла
                        # while worksheet < 50:  # ключевое слово 'while' и условие выполнение цикла-не более 50 раз
                        #     self.worksheets.pop() # тело цикла
                        #     print(worksheet)  # выводg значения переменной 'worksheet'
                        #     worksheet += 1  # уменьшение значения переменной 'worksheet' на единицу

                        for worksheet in list:
                            worksheet: profile_id = worksheet**2
                            print(worksheet)

                        photos = self.vk_tools.get_photos(worksheet['id'])  # ищем фото к этой анкете
                        photo_string = ''
                        for photo in photos:  # формируем строку
                            photo_string += f'photo{photo["owner_id"]}_{photo["id"]},'
                    else:
                        self.worksheets = self.vk_tools.search_worksheet(  #здесь мы находим анкеты
                            self.params)
                        worksheet = self.worksheets.pop()  #берем любую анкету
                        photos = self.vk_tools.get_photos(worksheet['id']) #ищем фото к этой анкете
                        photo_string = ''
                        for photo in photos:  #формируем строку
                            photo_string += f'photo{photo["owner_id"]}_{photo["id"]},'
                        self.offset += 50

                    self.message_send(
                        event.user_id,
                        f'имя: {worksheet["name"]} ссылка: vk.com/{worksheet["id"]}',
                        attachment=photo_string   #и отправляем сообщение пользователю
                    )
                    'добавить анкету в БД в соответствии с event.user_id'

                elif event.text.lower() == 'пока':
                    self.message_send(
                        event.user_id, 'До новых встреч')
                else:
                    self.message_send(
                        event.user_id, 'Неизвестная команда')


if __name__ == '__main__':  #это условие позволяет определять самим выполнение кода в данном файле
   bot_interface = BotInterface(comunity_token, acces_token)
   bot_interface.event_handler()