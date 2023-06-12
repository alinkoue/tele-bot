import asyncio
from bot_privat import TOKEN
import random
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import Message
from aiogram.dispatcher.filters import Text, Command
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from keyboards import keyboard, keyboard2
import logging

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
all_users = set()
connected_users = set()

@dp.message_handler(commands=['start', 'help'], state='*')
async def send_welcome(message: types.Message, state: FSMContext):
    await message.answer("привет, это чат-рулетка \nнапиши своё имя (твоё имя будет видно собеседникам)")
    await state.set_state("q1")

@dp.message_handler(state="q1")
async def process_name(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data({"name": name})
    await state.set_state("q2")
    await message.answer("напиши свой возраст")

@dp.message_handler(state='q2')
async def process_level(message:types.Message,state:FSMContext):
    age = message.text
    if age.isdigit():
        await state.update_data({"age":int(age)})
        if int(age)<13:
            await message.answer("ты ещё слишком мал чтобы пользоваться ботами, иди делай уроки!")
            await state.set_state('ban')
        else:
            await state.set_state('ready')
            await message.answer("а сейчас я чат-бот! попробуй сам",reply_markup=keyboard)
    else:
        await message.answer("не получилось распознать, пиши свой возраст цифрами")

@dp.message_handler(commands="find", state="ready")
@dp.message_handler(Text(equals="найти собеседника"), state="ready")
async def _(message: types.Message, state: FSMContext):
    global keyboard
    all_users.add(message.from_user.id)
    user_id = message.from_user.id
    targets = all_users - connected_users - {user_id, }
    if targets:
        target = random.choice(list(targets))
        target_state: FSMContext = dp.current_state(chat=target, user=target)
        target_data = await target_state.get_data()
        target_name = target_data.get('name')
        user_data = await state.get_data()
        user_name = user_data.get('name')
        await state.update_data({"buddy": target})
        await target_state.update_data({"buddy": user_id})
        await message.answer(f"! Вы связаны с {target_name} !", reply_markup=keyboard2)
        await bot.send_message(target, f"! Вы связаны с {user_name} !", reply_markup=keyboard2)
        await state.set_state("connected")
        await target_state.set_state("connected")
        connected_users.add(message.from_user.id)
        connected_users.add(target)

    else:
        await message.answer("найти собеседника не получилось, подожди немножко :(")


@dp.message_handler(Text(equals="не хочу искать"), state="ready")
async def _(message: types.Message, state: FSMContext):
    await message.answer(f"чтобы восстановить общение нажмите на /find", reply_markup=types.ReplyKeyboardRemove())
    if message.from_user.id in connected_users:
        connected_users.remove(message.from_user.id)
@dp.message_handler(Text(equals="не хочу искать"), state="connected")
async def _(message: types.Message, state: FSMContext):
    data = await state.get_data()
    buddy = data.get('buddy')
    await state.set_state("ready")
    target_state: FSMContext = dp.current_state(chat=buddy, user=buddy)
    await target_state.set_state("ready")
    if message.from_user.id in connected_users:
        connected_users.remove(message.from_user.id)
        await message.answer("чтобы восстановить общение нажмите на 'найти собеседника'", reply_markup=keyboard)
    if buddy in connected_users:
        connected_users.remove(buddy)
        await bot.send_message(buddy, "ваш собеседник решил бросить вас, чтобы найти нового нажмите на 'найти собеседника'", reply_markup=keyboard)


@dp.message_handler(state="connected")
async def _(message: types.Message, state: FSMContext):
    data = await state.get_data()
    buddy = data.get('buddy')
    name = data.get('name')
    txt = f"{name}: {message.text}"
    await bot.send_message(buddy, txt)

    tasks = []
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
