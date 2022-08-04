import aiogram.utils.markdown as md
from aiogram import Bot, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.utils import executor
from aiogram.utils.markdown import text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import aiogram
import asyncio
import config
import logging
import os
import photo

bot = Bot(token = config.token)
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)

bga = 0
stay_fact = ''
class answers(StatesGroup):
    edited_fact = State()



@dp.message_handler(commands = ['start'])
async def start(message: types.Message):
    await message.answer('Привет, этот бот принадлежит группе вк - Гений Гысли (@geniy_gisly). \nЗдесь можете создать свою цитату/факт используя комманды из списка.')
    await message.answer('1)/create_quote - Создать цитату \n2)/create_fact - Создать факт \nПолучить помощь можете с помощью комманды /help')


@dp.message_handler(commands=['help'])
async def help(message: types.message):
    await message.answer(
''' 
Цитаты!
1)Цитирование создается автоматически, вы никак не вправе повлиять на это!
2)чтобы создать цитату достаточно написать комманду

Факты!
1)Бот будет отправлять вам конечную версию факта
2)Бот дает вам возможность редактировать факт
3)Если вы уже не хотите создавать факт, то напишите - skip
4)Хотите оставить факт напишите - stay
Фон!
1)Вы можете доверить выбор фона рандому алгоритма с помощью комманды цифры 0
2)Хотите свой фон напишите его номер
3)Чтобы узнать сколько всего фонов есть напишите комманду /bg_count

Поскольку мне лень писать защиту от дурака это ваши проблемы что вы проебались где-то с вводом данных. Поэтому если проебали что-то крутое, идите к черту
'''
)

@dp.message_handler(commands=['create_quote'])
async def create_quote(message: types.message):
    try:
        bg = message.get_args()
    except:
        bg = 0
    photo.create_smth(1, bg)
    await message.answer_document(open('pics/ready.jpg', 'rb'))

@dp.message_handler(commands=['create_fact'])
async def create_fact(message: types.message):
    global bga, stay_fact
    try:
        bga = message.get_args()
    except:
        bga = 0
    text_i = photo.create_smth(2, console=False)
    stay_fact = text_i
    await answers.edited_fact.set()
    await message.answer(f"{text_i} \n\nНапишите комманду или отредактируйте текст")


async def send_fact(text, chat_idd):
    if text.lower() != 'stay':
        error = photo.create_smth(2,console=False,edited=text, BG=bga)
        if error == 'ernno':
            await bot.send_message(chat_idd, 'Успешная отмена')
        elif error == 'succes':
            await bot.send_document(chat_idd, open('pics/ready.png', 'rb'))
    elif text.lower() == 'stay':
        error = photo.create_smth(2,console=False,edited=stay_fact, BG=bga)
        if error == 'ernno':
            await bot.send_message(chat_idd, 'Успешная отмена')
        elif error == 'succes':
            await bot.send_document(chat_idd, open('pics/ready.png', 'rb'))

@dp.message_handler(state=answers.edited_fact)
async def edit_fact(message: types.Message, state:FSMContext):
    edited = message.text
    await state.update_data(fact=edited)
    await send_fact(edited, message.chat.id)
    await state.finish()

@dp.message_handler(commands=['bg_count'])
async def bg_count(message: types.message):
    await message.answer(f"Всего фонов - {photo.count_bg()}")

if __name__ == '__main__':
	executor.start_polling(dp, skip_updates = True)