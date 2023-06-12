from random import choice, random
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove
from bot_privat import TOKEN
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text, Command
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from keyboard_eng import keyboard, keyboard2, keyboard3
from dictionaries import main_dictionary
import logging

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


class TestStates(StatesGroup):
    waiting_for_answer = State()


@dp.message_handler(commands=['start', 'help'], state='*')
async def send_welcome(message: types.Message, state: FSMContext):
    await state.set_state('q1')
    await message.answer("Hi! Я твой помошник в изучении английского языка")
    await message.answer("Как тебя зовут?")


@dp.message_handler(state='q1')
async def process_name(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await message.answer(f"приятно познакомиться :)\n{name}, знаешь свой уровень?", reply_markup=keyboard)
    await state.set_state('q2')


async def choose_word(message: types.Message, state: FSMContext, level: str):
    level_dictionary = main_dictionary[level]
    random_key = choice(list(level_dictionary.keys()))
    true_answer = level_dictionary[random_key]
    await message.answer(f"Напишите перевод слова '{random_key}': ", reply_markup=keyboard3)
    await state.update_data(true_answer=true_answer, random_key=random_key)
    await TestStates.waiting_for_answer.set()


@dp.message_handler(state=TestStates.waiting_for_answer)
async def check_answer(message: types.Message, state: FSMContext):  # middleware
    data = await state.get_data()
    true_answers = data['true_answer']
    level = data['level']
    user_answer = message.text
    if isinstance(true_answers, str):
        true_answers = [true_answers]

    for true_answer in true_answers:
        if true_answer.lower() == user_answer.lower():
            await message.answer("Правильно ✅")
            await choose_word(message, state, level)
            break
    else:
        await message.answer(f"Неправильно ❌\nПравильный ответ: {true_answers}")
        await choose_word(message, state, level)


# A2
@dp.message_handler(Text(equals="A2"), state="q2")
async def _(message: types.Message, state: FSMContext):
    await state.set_state('a2')
    await state.update_data(level="a2")
    await message.answer(f"выбери режим: ", reply_markup=keyboard2)


@dp.message_handler(Text(equals='vocabulary'))
async def start_vocabulary_test(message: types.Message, state: FSMContext):
    data = await state.get_data()
    level = data['level']
    await choose_word(message, state, level)


@dp.message_handler(Text(equals='grammar'), state="a2")
async def _(message: types.Message, state: FSMContext):
    ...


# B1
@dp.message_handler(Text(equals="B1"), state="q2")
async def _(message: types.Message, state: FSMContext):
    await state.set_state('b1')
    await state.update_data(level="b1")
    await message.answer(f"выбери режим: ", reply_markup=keyboard2)


@dp.message_handler(Text(equals='vocabulary'), state="b1")
async def start_vocabulary_test(message: types.Message, state: FSMContext):
    await choose_word(message, state, "b1")


@dp.message_handler(Text(equals='grammar'), state="b1")
async def _(message: types.Message, state: FSMContext):
    ...


# B2
@dp.message_handler(Text(equals="B2"), state="q2")
async def _(message: types.Message, state: FSMContext):
    await state.set_state('b2')
    await state.update_data(level="b2")
    await message.answer(f"выбери режим: ", reply_markup=keyboard2)


@dp.message_handler(Text(equals='vocabulary'), state="b2")
async def _(message: types.Message, state: FSMContext):
    await state.set_state('b2')
    await state.update_data(level="b2")
    await message.answer(f"выбери режим: ", reply_markup=keyboard2)


@dp.message_handler(Text(equals='grammar'), state="b2")
async def start_vocabulary_test(message: types.Message, state: FSMContext):
    await choose_word(message, state, "b2")


# test
@dp.message_handler(Text(equals="не знаю"), state="q2")
async def _(message: types.Message, state: FSMContext):
    await state.set_state('xx')
    await message.answer(f" сейчас тебе нужно будет пройти тест", reply_markup=ReplyKeyboardRemove())


@dp.message_handler(state='xx')
async def process_age(message: types.Message, state: FSMContext):
    # total = 0
    # for i in range
    ...


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
