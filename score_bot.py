import json
import traceback
import telebot
from datetime import datetime
from time import sleep
from TOKEN import TOKEN

# from telebot.apihelper import send_message
'''
импорт всех нужных либ, затем объявка функций


по сценарию бот должен сдороваться с юзером,
затем пиказывать ему команду помощи чтобы показать ему все
доступные команды и познакомить с ними

затем бот либо добавляет юзера в БД, либо уже ищет его там
'''

# первый бот в телеге ы
# TOKEN потому что ЭТО МОЙ ТОКЕН ЭТО МАЙО
bot = telebot.TeleBot(TOKEN)
havi_flag = False


def num_sort(arg):
    ans = ''
    for char in arg:
        if char.isdigit():
            ans += char
    return ans


def logging(message):
    try:
        with open('logs.txt', 'a') as logs:
            string = f'''
            Пишет чел:
            id -- {message.from_user.id}
            имя -- {message.from_user.first_name} {message.from_user.last_name}
            username -- {message.from_user.username}
            время на сервере -- {datetime.now()}
            текст сообщения -- "{message.text}"
            кароче, вот весь лог по юзеру -- "{message.from_user}"\n
            а вот вообще весь лог -- {message}
            '''
            logs.write(string)
            print(string)
    except Exception as e:
        with open('logs.txt', 'a') as logs:
            logs.write(f'!!!ПОПАЛАСЬ ОШИБКА:\n{traceback.format_exc()}')
            logs.write(f'ОШИБКА -- {e}')
            traceback.print_exc()
            print(f'ОШИБКА -- {e}')
            bot.send_message(message.from_user.id, ('Извините, я Вас не понял\n'
                                                    'Мне понятен только чистый текст, совсем без эмодзи и написанный на русском языке. '
                                                    'А также без перевёрнутых знаков препинания или прочих знаков, которых нет на норм клаве'))


tegs = ['text', 'audio', 'document', 'photo',
        'sticker', 'video', 'video_note', 'voice',
        'location', 'contact', 'new_chat_members', 'left_chat_member',
        'new_chat_title', 'new_chat_photo', 'delete_chat_photo', 'group_chat_created',
        'supergroup_chat_created', 'channel_chat_created', 'migrate_to_chat_id', 'migrate_from_chat_id',
        'pinned_message']


# ВСЕ ТЕГИ ТЕЛЕГИ НА ВСЯКИЙ СЛУЧАЙ


@bot.message_handler(commands=['start'])
def well_cum(message):  # ыыы смешнявка (:
    # шутки про кам, да-да)
    logging(message)
    bot.send_message(message.from_user.id, 'Привет-привет, для помощи с командами пиши\n\n/help')


@bot.message_handler(commands=['help'])
def helper(message):
    logging(message)
    sp = '        '
    bot.send_message(message.from_user.id, ('Итак, все команды для справки по боту:\n\n'
                                            '/start -- для начала общения (:\n'
                                            '/help -- для вызова помощи по командам\n'
                                            '/append_me -- добавляет пользователя - тебя - в базу данных для взаимодействия с тобой\n'
                                            'После команды /append_me будет доступна работа с командами по управлению данными'
                                            "и в любой момент можно будет посмотреть их и их инфу тут, в разделе /help\n\n\n"
                                            'Итак, команды управления данными:\n\n'
                                            '-добавить -- добавляет в базу данных ваш предмет. Внимание, знак минуса (-) или восклицательный знак (!) в этой и в следующих командах обязателен!\n'
                                            f'{sp}Для работы с этой командой, её нужно писать в формате "-добавить <название предмета>", через пробел и жеталельно без лишних слов!\n'
                                            f'{sp}Эту, как и другие команды с минусом, пишите именно маленькими буквами, пожалуйста\n'
                                            f'{sp}Внимание!!! В силу технических возможностей, названия предметов должны быть без пробелов!!!'
                                            '-дописать -- дописывает оценку к уже существующему предмету, пример использования -- "!дописать матеша 4"\n'
                                            '-очистить -- безвозвратно стирает оценки по выбранному предмету, но не удаляет его. Пример -- "-очистить инфа"\n'
                                            '-стереть_всё -- безвозвратно стирает все ваши предметы. Полезно перед 1 сентября, или когда начат новый семестр/триместр/четверть\n'
                                            '-текущий_балл -- подсчитывает нынешний балл по выбранному предмету. Пример -- "-текущий_балл геометрия"\n'
                                            '-предсказать_балл -- какой будет средний балл по выбранному предмету с учётом указанной оценки. Пример -- "!предсказать_балл русский 4"\n'
                                            '-все_предметы -- выводит в сообщении все ваши предметы и оценки по ним. Пример -- "-все_предметы"\n\n'
                                            'Если что-то не так или есть вопросы -- пишите @strange_arcturus\nЗаранее спасибо.'
                                            ))


@bot.message_handler(commands=['append_me'])
def append_me(message):
    global havi_flag
    logging(message)
    try:
        with open('users.json', 'r') as file:
            users_dict = json.load(file)

        if str(message.from_user.id) not in users_dict:
            bot.send_message(message.from_user.id, 'Окей, щща добавлю')
            users_dict[str(message.from_user.id)] = {
                'name': f'{message.from_user.first_name} {message.from_user.last_name}',
                "status_flag": True,
                'subj': {}
            }
            havi_flag = True
        elif str(message.from_user.id) in users_dict:
            bot.send_message(message.from_user.id, 'Сорри, тебя незачем добавлять ещё раз (:')
            havi_flag = True

        with open('users.json', 'w') as file:
            json.dump(users_dict, file, indent=4)
    except Exception as e:
        with open('logs.txt', 'a') as logs:
            logs.write(f'!!!ПОПАЛАСЬ ОШИБКА:\n{traceback.format_exc()}')
            logs.write(f'ОШИБКА -- {e}')
            traceback.print_exc()
            print(f'ОШИБКА -- {e}')
            bot.send_message(message.from_user.id, 'Ой, что-то пошло не так...')


# функция для повторения слов за юзером, пока что самое лёгкое, если юзер не попал по командам
@bot.message_handler(content_types=tegs)
def get_text_messages(message):
    global havi_flag
    logging(message)
    try:
        txt = message.text
        commands = txt.split()
        with open('users.json', 'r') as file:
            users_dict = json.load(file)
        if commands[0] == '-добавить' or commands[0] == '!добавить':
            if havi_flag is False and users_dict[str(message.from_user.id)]['status_flag'] is False:
                bot.send_message(message.from_user.id,
                                 'Сорри, пока что не могу выполнить эту команду\n\nЕсли что, есть команда /help')
            else:
                if commands[1].lower() not in users_dict[str(message.from_user.id)]['subj']:
                    users_dict[str(message.from_user.id)]['subj'][commands[1].lower()] = ''
                    bot.send_message(message.from_user.id, f'Предмет "{commands[1]}" успешно добавлен')
                else:
                    bot.send_message(message.from_user.id, f'Предмет "{commands[1]}" уже был добавлен раннее')
        elif commands[0] == '-дописать' or commands[0] == '!дописать':
            if havi_flag is False and users_dict[str(message.from_user.id)]['status_flag'] is False:
                bot.send_message(message.from_user.id,
                                 'Сорри, пока что не могу выполнить эту команду\n\nЕсли что, есть команда /help')
            else:
                if commands[1].lower() not in users_dict[str(message.from_user.id)]['subj']:
                    bot.send_message(message.from_user.id,
                                     'У тебя нет такого предмета в боте, посмотри, пожалуйста, /help')
                else:
                    users_dict[str(message.from_user.id)]['subj'][commands[1].lower()] += str(commands[2])
                    bot.send_message(message.from_user.id,
                                     f'Оценка "{commands[2]}" добавлена к предмету "{commands[1]}"')
        elif commands[0] == '-очистить' or commands[0] == '!очистить':
            if havi_flag is False and users_dict[str(message.from_user.id)]['status_flag'] is False:
                bot.send_message(message.from_user.id,
                                 'Сорри, пока что не могу выполнить эту команду\n\nЕсли что, есть команда /help')
            else:
                if commands[1] not in users_dict[str(message.from_user.id)]['subj']:
                    bot.send_message(message.from_user.id, 'Извини, такого предмета ты не добавлял')
                else:
                    users_dict[str(message.from_user.id)]['subj'][commands[1].lower()] = ''
                    bot.send_message(message.from_user.id, f'Все оценки по предмету "{commands[1]}" очищены')
        elif commands[0] == '-стереть_всё' or commands[0] == '!стереть_всё':
            if havi_flag is False and users_dict[str(message.from_user.id)]['status_flag'] is False:
                bot.send_message(message.from_user.id,
                                 'Сорри, пока что не могу выполнить эту команду\n\nЕсли что, есть команда /help')
            else:
                users_dict[str(message.from_user.id)]['subj'] = {}
                bot.send_message(message.from_user.id, 'Все ваши предметы были безвозвратно стёрты)')
        elif commands[0] == '-текущий_балл' or commands[0] == '!текущий_балл':
            if havi_flag is False and users_dict[str(message.from_user.id)]['status_flag'] is False:
                bot.send_message(message.from_user.id,
                                 'Сорри, пока что не могу выполнить эту команду\n\nЕсли что, есть команда /help')
            else:
                string = list(num_sort(users_dict[str(message.from_user.id)]['subj'][commands[1].lower()]))
                string = list(map(int, string))
                bot.send_message(message.from_user.id,
                                 f'Нынешняя оценка по предмету "{commands[1]}" составляет {sum(string) / len(string)}')
        elif commands[0] == '-предсказать_балл' or commands[0] == '!предсказать_балл':
            if havi_flag is False and users_dict[str(message.from_user.id)]['status_flag'] is False:
                bot.send_message(message.from_user.id,
                                 'Сорри, пока что не могу выполнить эту команду\n\nЕсли что, есть команда /help')
            else:
                string = list(
                    num_sort(users_dict[str(message.from_user.id)]['subj'][commands[1].lower()] + commands[2]))
                string = list(map(int, string))
                bot.send_message(message.from_user.id, (
                    f'Рассчитывая на оценку {commands[2]}, балл по предмету "{commands[1]}" составит'
                    f' {sum(string) / len(string)}'))
        elif commands[0] == '-все_предметы' or commands[0] == '!все_предметы':
            if havi_flag is False and users_dict[str(message.from_user.id)]['status_flag'] is False:
                bot.send_message(message.from_user.id,
                                 'Сорри, пока что не могу выполнить эту команду\n\nЕсли что, есть команда /help')
            else:
                arr = list(users_dict[str(message.from_user.id)]['subj'].keys())
                final_arr = []
                for elem in arr:
                    wh = f'{str(elem)}: {str({users_dict[str(message.from_user.id)]["subj"][elem]})}'
                    final_arr.append(wh)
                ans = '\n'.join(final_arr)
                bot.send_message(message.from_user.id, f'Список ваших добавленных предметов:\n{ans}')
        else:
            bot.send_message(message.from_user.id,
                             f'Извини, я тебя не понял. Поэтому напомню про команду /help и повторю за тобой\n\n{message.text}')
            pass
        # ВНИМАНИЕ, КОМАНДА ПРО ВСЕ ПРЕДМЕТЫ НЕ РАБОТАЕТ
        # а, не, работает всё
        with open('users.json', 'w') as file:
            json.dump(users_dict, file, indent=4)
    except Exception as e:
        with open('logs.txt', 'a') as logs:
            logs.write(f'!!!ПОПАЛАСЬ ОШИБКА:\n{traceback.format_exc()}')
            logs.write(f'ОШИБКА -- {e}')
            traceback.print_exc()
            print(f'ОШИБКА -- {e}')
            bot.send_message(message.from_user.id, (
                'Ой, что-то пошло не так...'
                f" Я тебя не понимаю, повторю за тобой\n\n{message.text}\n\nЕсли что, есть команда /help"))


while True:
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception as e:
        with open('logs.txt', 'a') as logs:
            logs.write(f'!!!ПОПАЛАСЬ ОШИБКА:\n{traceback.format_exc()}')
            logs.write(f'ОШИБКА -- {e}')
            traceback.print_exc()
            print(f'ОШИБКА -- {e}')
            sleep(0.5)
