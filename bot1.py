import logging
from bot_privat import TOKEN
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext


logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot,storage = MemoryStorage())


@dp.message_handler(commands=['start', 'help'],state='*')
async def send_welcome(message: types.Message,state: FSMContext):
    await message.answer("приветик, я эхобот!\nвведи своё имя:")
    await state.set_state('q1')

@dp.message_handler(state='q1')
async def process_name(message:types.Message,state:FSMContext):
    name = message.text
    await state.update_data({"name":name})
    await message.answer(f"приятно познакомиться :)\n{name}, введи свой возраст:")
    await state.set_state('q2')

@dp.message_handler(state='q2')
async def process_age(message:types.Message,state:FSMContext):
    age = message.text
    if age.isdigit():
        await state.update_data({"age":int(age)})
        if int(age)<13:
            await message.answer("ты ещё слишком мал чтобы пользоваться ботами, иди делай уроки!")
            await state.set_state('ban')
        else:
            await state.set_state('echo')
            await message.answer("а сейяас я эхобот! попробуй сам")
    else:
        await message.answer("не получилось распознать, пиши свой возраст цифрами")
@dp.message_handler(state = "echo")
async def echo(message: types.Message):
     await message.answer(message.text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)