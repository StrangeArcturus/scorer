from aiogram import Bot, Dispatcher, executor, types
from db_connector import AsyncDataBaseConnector
from messages_for_bot import hello
from typing import List, Union
from TOKEN import *


bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)
db_conn = AsyncDataBaseConnector("./db/users.db", "tg")
COMMANDS = {
    "добавить": db_conn.add_subject_to_user,
    "дописать": db_conn.add_scores_to_subject,
    "очистить": db_conn.clean_subject,
    "стереть_всё": db_conn.clean_all_users_subjects,
    "текущий_балл": db_conn.now_score,
    "предсказать_балл": db_conn.predict_scores,
    "все_предметы": db_conn.all_subjects_with_scores_as_dict
}
file_conmmander = types.InputFile(db_conn.name, filename=db_conn.name)


@dp.message_handler(commands=['start'])
async def welcome(message: types.Message) -> None:
    print(f"получено сообщение: {message.text}")
    answer: str = "Привет, я -- бот-дневник)\nДля помощи: команда /help"
    print(f"мой ответ -- {answer}")
    user_id = message.from_user.id
    await db_conn.add_user(user_id=user_id)
    await message.reply(answer)


@dp.message_handler(commands=['help'])
async def help_to_user(message: types.Message) -> None:
    print(f"получено сообщение: {message.text}")
    print(f"мой ответ -- {hello}")
    await message.reply(hello)


@dp.message_handler(commands=['get_db_file'])
async def get_database_file(message: types.Message) -> None:
    print(f"получено сообщение: {message.text}")
    answer: str = "моё почтение, .db файл прилагаю)"
    """
    with open(db_conn.name, 'r') as file:
        # await message.reply_document(db_conn.name)
        # await bot.send_document(message.chat.id, (db_conn.name, file))
        # await message.answer_document(message.from_user.id, file_conmmander)
    """
    await message.reply(answer)
    print(f'отвечаю: {answer}\nОтсылаю файл базы данных')
    await bot.send_document(message.chat.id, file_conmmander)  # единственный рабочий способ чеек


@dp.message_handler(content_types='text')
async def talking(message: types.Message) -> None:
    text: Union[str, None] = message.text
    user_id = message.from_user.id
    if text:
        print(f"получено сообщение: {text}")
        if text[0] == "!":
            msg: List[str] = text[1:].split()
            if msg[0] in COMMANDS:
                command = msg.pop(0) if len(msg) >= 1 else None
                subject = msg.pop(1) if len(msg) >= 2 else None
                #  scores = msg.pop(2) if len(msg) >= 3 else None
                scores = " ".join(msg[:]) if len(msg) else None
                if command == "добавить":
                    if scores:
                        result: Union[int, None] = await db_conn.add_subject_to_user(
                            user_id=user_id,
                            subject=subject,
                            scores=scores
                        )
                        if not result:
                            print(f"предмет {subject} с оценками {scores} успешно добавлен юзеру {user_id}")
                            await message.reply(f"предмет {subject} с оценками {scores} успешно добавлен")
                        else:
                            print(f"упс, что-то пошло не так с добавлением предмета {subject} с оценками {scores}")
                            await message.reply(
                                f"упс, что-то пошло не так с добавлением предмета {subject} с оценками {scores}"
                            )
                    else:
                        result: Union[int, None] = await db_conn.add_subject_to_user(
                            user_id=user_id,
                            subject=subject
                        )
                        if not result:
                            print(f"предмет {subject} успешно добавлен юзеру {user_id}")
                            await message.reply(f"предмет {subject} успешно добавлен")
                        else:
                            print(f"упс, что-то пошло не так с добавлением предмета {subject}")
                            await message.reply(
                                f"упс, что-то пошло не так с добавлением предмета {subject}"
                            )
                elif command == "дописать":
                    if scores:
                        result: Union[int, None] = await db_conn.add_scores_to_subject(
                            user_id=user_id,
                            subject=subject,
                            scores=scores
                        )
                        if not result:
                            print(f"предмет {subject} с оценками {scores} успешно обновлён юзеру {user_id}")
                            await message.reply(f"предмет {subject} с оценками {scores} успешно обновлён")
                        else:
                            print(f"упс, что-то пошло не так с обновлением предмета {subject} с оценками {scores}")
                            await message.reply(
                                f"упс, что-то пошло не так с обновлением предмета {subject} с оценками {scores}"
                            )
                    else:
                        result: Union[int, None] = await db_conn.add_scores_to_subject(
                            user_id=user_id,
                            subject=subject
                        )
                        if not result:
                            print(f"предмет {subject} успешно добавлен юзеру {user_id}")
                            await message.reply(f"предмет {subject} успешно добавлен")
                        else:
                            print(f"упс, что-то пошло не так с добавлением предмета {subject}")
                            await message.reply(
                                f"упс, что-то пошло не так с добавлением предмета {subject}"
                            )
                elif command == "очистить":
                    result: Union[int, None] = await db_conn.clean_subject(
                        user_id=user_id,
                        subject=subject
                    )
                    if not result:
                        print(f"предмет {subject} успешно очищен у юзера {user_id}")
                        await message.reply(f"предмет {subject} успешно очищен")
                    else:
                        print(f"упс, что-то пошло не так с очищением предмета {subject}")
                        await message.reply(
                            f"упс, что-то пошло не так с очищением предмета {subject}"
                        )
                elif command == "стереть_всё":
                    result: Union[int, None] = await db_conn.clean_all_users_subjects(
                        user_id=user_id
                    )
                    if not result:
                        print(f"предметы юзера {user_id} были успешно очищены")
                        await message.reply("ваши предметы были успешно очищены")
                    else:
                        print(f"упс, что-то пошло не так с очищением предметов юзера {user_id}")
                        await message.reply(
                            f"упс, что-то пошло не так с очищением ваших предметов"
                        )
                elif command == "текущий_балл":
                    result: Union[float, None] = await db_conn.now_score(
                        user_id=user_id,
                        subject=subject
                    )
                    if result is None:
                        print(f"упс, что-то пошло не так с получением оценки по предмету {subject} юзера {user_id}")
                        await message.reply(f"упс, что-то пошло не так с получением оценки по предмету {subject}")
                    else:
                        print(f"средний балл по предмету {subject} юзера {user_id}: {result}")
                        await message.reply(f"средний балл по предмету {subject}: {result}")
                elif command == "предсказать_балл":
                    if scores:
                        result: Union[float, None] = await db_conn.predict_scores(
                            user_id=user_id,
                            subject=subject,
                            predict_scores=scores
                        )
                        if result is None:
                            print(
                                f"упс, что-то пошло не так с предсказанием оценки по предмету {subject} юзера {user_id}"
                            )
                            await message.reply(
                                f"упс, что-то пошло не так с предсказанием оценки по предмету {subject}"
                            )
                        else:
                            print(f"предсказанный средний балл "
                                  f"по предмету {subject} у юзера {user_id} составляет {result}")
                            await message.reply(f"предсказанный средний балл по предмету {subject} составляет {result}")
                    else:
                        print("ошибка в данных оценках для предсказания")
                        await message.reply("ошибка в данных оценках для предсказания")
                elif command == "все_предметы":
                    result: Union[dict, None] = await db_conn.all_subjects_with_scores_as_dict(
                        user_id=user_id
                    )
                    if result is None:
                        print(f"упс, ошибка с предметами и оценками юзера {user_id}")
                        await message.reply(f"упс, произошла ошибка с получением предметами и оценками")
                    else:
                        answer: str = ""
                        for elem in result.keys():
                            answer += f"{elem}: {result[elem]}\n"
                        print(f"получены оценки юзера {user_id} в следующем виде:\n{answer}")
                        await message.reply('Все ваши оценки приведены в следующем соообщении списком в формате '
                                            '"название предмета": "оценки по этому предмету"')
                        await message.reply(answer)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
