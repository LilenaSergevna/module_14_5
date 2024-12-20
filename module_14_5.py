from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

import crud_functions

api="8042797506:AAFBTh3aQgJv5fy0cSYJ8gBLEugumTTEeAc"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb=ReplyKeyboardMarkup(resize_keyboard=True)
but1=KeyboardButton(text="Рассчитать")
but2=KeyboardButton(text="Информация")
but3=KeyboardButton(text="Купить")
but4=KeyboardButton(text="Регистрация")
kb.row(but1, but2)
kb.add(but3)
kb.add(but4)

kb1 = InlineKeyboardMarkup()
InBut1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
InBut2 = InlineKeyboardButton(text="Формулы расчёта", callback_data="formulas")
kb1.add(InBut1, InBut2)

kb2 = InlineKeyboardMarkup()
InBut1 = InlineKeyboardButton(text='Product1', callback_data='product_buying')
InBut2 = InlineKeyboardButton(text='Product2', callback_data='product_buying')
InBut3 = InlineKeyboardButton(text='Product3', callback_data='product_buying')
InBut4 = InlineKeyboardButton(text='Product4', callback_data='product_buying')
kb2.add(InBut1, InBut2, InBut3, InBut4)



class UserState(StatesGroup):
    age=State()
    growth=State()
    weight=State()


class RegistrationState(StatesGroup):
    username=State()
    email=State()
    age=State()



@dp.message_handler(text='Рассчитать')
async def main_menu(message: types.Message):
    await message.answer('Выберите опцию:', reply_markup=kb1)

@dp.callback_query_handler(text="formulas")
async def form(call):
    await call.message.answer('10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')
    await call.answer()

@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer(f'Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer(f'Введите свой рост')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer(f'Введите свой вес')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def set_weight(message, state):
    await state.update_data(weight=message.text)
    data= await state.get_data()
    kol=10*int(data['weight'])+ 6.25*int(data['growth'])- 5*int(data['age'])+int(5)
    print(kol)
    await message.answer(f'Норма каллорий {kol}')
    await state.finish()


@dp.message_handler(commands=["start"])
async def start(message):
    await message.answer(f'Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)


#14_3
@dp.message_handler(text='Купить')
async def get_buying_list(message):
    my_prods=crud_functions.get_all_products()

    for prod in my_prods:
        await message.answer(f'Название: {prod[1]} | Описание: {prod[2]} | Цена: {prod[3]}')
        with open(f'file_m14/{prod[0]}.png','rb') as img:
            await message.answer_photo(img)
    await message.answer("Выберите продукт для покупки:", reply_markup=kb2)

@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer(f'Вы успешно приобрели продукт!')
    await UserState.age.set()

#14_5
@dp.message_handler(text='Регистрация')
async def sing_up(message):
    await message.answer(f'Введите имя пользователя (только латинский алфавит):')
    await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    if crud_functions.is_included(message.text) is False:
        await state.update_data(username=message.text)
        await message.answer(f'Введите свой email:')
        await RegistrationState.email.set()
    else:
        await message.answer(f'Пользователь существует, введите другое имя')
        await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer(f'Введите свой возраст:')
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    new_user = await state.get_data()
    crud_functions.add_user(new_user['username'],new_user['email'],new_user['age'])
    await message.answer(f'Пользователь удачно зарегистрирован!')
    await state.finish()


if __name__=="__main__":
    executor.start_polling(dp, skip_updates=True)

