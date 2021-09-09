from aiogram import Bot, Dispatcher, executor, types
from db_connector import AsyncDataBaseConnector
from messages_for_bot import *
from TOKEN import *


bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)
db_conn = AsyncDataBaseConnector("./db/users.db", "tg")


@dp.message_handler(commands=['start'])
async def hello(message: types.Message) -> None:
    await message.reply("Привет, я -- бот-дневник)\nДля помощи: команда /help")


@dp.message_handler(commands=['help'])
async def help_to_user(message: types.Message) -> None:
    await message.reply(hello)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
