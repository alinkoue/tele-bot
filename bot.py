from random import choice, random
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove
from bot_privat import TOKEN
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text, Command
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from keyboards import keyboard, keyboard2, keyboard3, keyboard4
from dictionaries import grammar_dictionary, vocabular_dictionary
import logging
from test_test import questions_x_answers

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


class TestStates(StatesGroup):
    v_waiting_for_answer = State()
    g_waiting_for_answer = State()
    start_state = State()
    choose_level = State()
    a2 = State()
    b1 = State()
    b2 = State()
    wait_answer = State()


@dp.message_handler(commands=['start', 'help'], state='*')
async def send_welcome(message: types.Message):
    """обработчик запуска бота, устанавливает state start_state"""
    await TestStates.start_state.set()
    await message.answer("Hi! Я твой помошник в изучении английского языка")
    await message.answer("Как тебя зовут?")


@dp.message_handler(state=TestStates.start_state)
async def _(message: types.Message, state: FSMContext):
    """сохраняет имя, устанавливает state choose_level"""
    name = message.text
    await state.update_data(name=name)
    await message.answer(f"приятно познакомиться :)\n{name}, знаешь свой уровень?", reply_markup=keyboard)
    await TestStates.choose_level.set()


@dp.message_handler(Text(equals='стоп'), state="*")
async def _(message: types.Message, state: FSMContext):
    """выбирает уровень"""
    await message.answer(f"выбери уровень: ", reply_markup=keyboard)
    await TestStates.choose_level.set()

# test
@dp.message_handler(Text(equals="не знаю"), state=TestStates.choose_level)
async def _(message: types.Message, state: FSMContext):
    """"""
    await message.answer(f"Сейчас тебе нужно будет пройти тест.", reply_markup=keyboard4)
    await state.update_data(current_question=0, correct=0)
    await write_question(message, state)
    await TestStates.wait_answer.set()

######################## VOCABULAR #####################

async def vocabular_choose_answer(message: types.Message, state: FSMContext, level: str):
    """
    :param level: 'b1' | 'b2' | 'a1'
    """
    level_dictionary = vocabular_dictionary[level]
    random_key = choice(list(level_dictionary.keys()))
    true_answer = level_dictionary[random_key]
    await message.answer(f"Напишите перевод слова '{random_key}': ", reply_markup=keyboard3)
    await state.update_data(true_answer=true_answer, random_key=random_key)
    await TestStates.v_waiting_for_answer.set()


@dp.message_handler(state=TestStates.v_waiting_for_answer)
async def vocabular_check_answer(message: types.Message, state: FSMContext):  # middleware
    """сравнивает ответ пользователя с правильным ответом, проверяя правильность"""
    data = await state.get_data()
    true_answers = data['true_answer']
    level = data['level']
    user_answer = message.text
    if isinstance(true_answers, str):
        true_answers = [true_answers]

    for true_answer in true_answers:
        if true_answer.lower() == user_answer.lower():
            await message.answer("Правильно ✅")
            await vocabular_choose_answer(message, state, level)
            break
    else:
        text = ", ".join(true_answers)
        await message.answer(f"Неправильно ❌\nПравильный ответ: {text}")
        await vocabular_choose_answer(message, state, level)

@dp.message_handler(Text(equals='vocabulary'), state="*")
async def start_vocabulary_test(message: types.Message, state: FSMContext):
    data = await state.get_data()
    level = data['level']
    await vocabular_choose_answer(message, state, level)

###############################################



###################### GRAMMAR ################################
@dp.message_handler(Text(equals='grammar'), state="*")
async def start_grammar_test(message: types.Message, state: FSMContext):
    data = await state.get_data()
    level = data['level']
    await grammar_choose_answer(message, state, level)

@dp.message_handler(state=TestStates.g_waiting_for_answer)
async def grammar_check_answer(message: types.Message, state: FSMContext):  # middleware
    """сравнивает ответ пользователя с правильным ответом, проверяя правильность"""
    data = await state.get_data()
    true_answers = data['true_answer']
    level = data['level']
    user_answer = message.text
    if isinstance(true_answers, str):
        true_answers = [true_answers]

    for true_answer in true_answers:
        if true_answer.lower() == user_answer.lower():
            await message.answer("Правильно ✅")
            await grammar_choose_answer(message, state, level)
            break
    else:
        text = ", ".join(true_answers)
        await message.answer(f"Неправильно ❌\nПравильный ответ: {text}")
        await grammar_choose_answer(message, state, level)

async def grammar_choose_answer(message: types.Message, state: FSMContext, level: str):
    """
    :param level: 'b1' | 'b2' | 'a1'
    """
    level_dictionary = grammar_dictionary[level]
    random_key = choice(list(level_dictionary.keys()))
    true_answer = level_dictionary[random_key]
    await state.update_data(true_answer=true_answer, random_key=random_key)
    await message.answer(f"{random_key}",reply_markup=keyboard3)
    await TestStates.g_waiting_for_answer.set()

######################################################



################## УРОВНИ #################
# A2

@dp.message_handler(Text(equals="A2"), state=TestStates.choose_level)
async def _(message: types.Message, state: FSMContext):
    await TestStates.a2.set()
    await state.update_data(level="a2")
    await message.answer(f"выбери режим: ", reply_markup=keyboard2)


# B1
@dp.message_handler(Text(equals="B1"), state=TestStates.choose_level)
async def _(message: types.Message, state: FSMContext):
    await TestStates.b1.set()
    await state.update_data(level="b1")
    await message.answer(f"выбери режим: ", reply_markup=keyboard2)


# B2
@dp.message_handler(Text(equals="B2"), state=TestStates.choose_level)
async def _(message: types.Message, state: FSMContext):
    await TestStates.b2.set()
    await state.update_data(level="b2")
    await message.answer(f"выбери режим: ", reply_markup=keyboard2)
########################################################


################## ТЕСТ ######################
@dp.message_handler(state=TestStates.wait_answer)
async def _(message: types.Message, state: FSMContext):
    """завершает тест, выдаёт кол-во правильных ответов, уровень"""
    data = await state.get_data()
    current_question = data["current_question"]
    correct = data["correct"]
    if current_question + 1 >= len(questions_x_answers):
        if correct <= 5:
            level_test = "твой уровень английского А2 📒✏️"
        elif 5 < correct <= 11:
            level_test = "молодец,твой уровень английского B1 📚"
        else:
            level_test = "ого, твой уровень английского B2 📕🖍"
        await message.answer(f"тест закончен: правильных ответов {correct}\n{level_test}", reply_markup=keyboard3)
        await state.reset_state()
        return

    question, answer = questions_x_answers[current_question]
    if message.text == answer:
        await state.update_data(correct=correct + 1)
    await state.update_data(current_question=current_question + 1)
    await write_question(message, state)


async def write_question(message: types.Message, state: FSMContext):
    """"""
    data = await state.get_data()
    current_question = data["current_question"]
    question, answer = questions_x_answers[current_question]
    await message.answer(f"{question}")
############################################################

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
