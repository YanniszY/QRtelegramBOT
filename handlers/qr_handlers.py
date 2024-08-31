from aiogram import Router, types, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram import types
from aiogram.filters import Command, CommandStart
import asyncio
from util.fucn import generate_qr, generate_pass_wifi, generate_nopass_wifi, generate_event_qr, generate_contact_card
from keyboards.kb import kb, size_kb, wifi_answer_kb
from States.states import UserOptions

router = Router()


# Обработчик команды старт
@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer("Привет! Это бот для генерации QR кодов. Выбери действие в меню!", reply_markup=kb)

# Обработка QR кода с ссылкой
@router.callback_query(F.data == 'qr_code_link')
async def qr_link(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(UserOptions.link)
    await callback_query.message.answer("Отправь ссылку для генерации QR кода")

# Получение пользовательской ссылки + выбор размера
@router.message(UserOptions.link)
async def get_link(message: Message, state: FSMContext):
    await state.update_data(link=message.text)
    await state.set_state(UserOptions.link_size)
    await message.answer("Теперь укажите размер QR кода (рекомендуемый размер - 15)", reply_markup=size_kb)

# Обработка размера
@router.message(UserOptions.link_size)
async def qr_size(message: Message, state: FSMContext):
    data = await state.get_data()
    link = data.get('link')
    size = message.text
    await generate_qr(link, size, message)
    await state.clear()

# Обработка Wi-Fi с паролем
@router.callback_query(F.data == 'qr_code_wifi')
async def qr_pass_wifi(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(UserOptions.wifi_name)
    await callback_query.message.answer("Напишите название Wi-Fi сети")

@router.message(UserOptions.wifi_name)
async def get_wifi_name(message: Message, state: FSMContext):
    await state.update_data(wifi_name=message.text)
    await state.set_state(UserOptions.wifi_pass)
    await message.answer("Введите пароль от Wi-Fi")

@router.message(UserOptions.wifi_pass)
async def get_wifi_pass(message: Message, state: FSMContext):
    await state.update_data(wifi_pass=message.text)
    await state.set_state(UserOptions.wifi_size)
    await message.answer("Теперь выберите размер QR кода (рекомендуемый размер - 15)", reply_markup=size_kb)

@router.message(UserOptions.wifi_size)
async def get_wifi_size(message: Message, state: FSMContext):
    data = await state.get_data()
    wifi_name = data.get('wifi_name')
    wifi_pass = data.get('wifi_pass')
    size = message.text
    await generate_pass_wifi(wifi_name, wifi_pass, size, message)
    await state.clear()

# Обработка Wi-Fi без пароля
@router.callback_query(F.data == 'qr_code_wifi_nopass')
async def qr_code_wifi_nopass(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(UserOptions.wifi_name_nopass)
    await callback_query.message.answer("Напишите название Wi-Fi сети")

@router.message(UserOptions.wifi_name_nopass)
async def get_wifi_nopass(message: Message, state: FSMContext):
    await state.update_data(wifi_name_nopass=message.text)
    await state.set_state(UserOptions.wifi_size_nopass)
    await message.answer("Теперь выберите размер QR кода (рекомендуемый размер - 15)", reply_markup=size_kb)

@router.message(UserOptions.wifi_size_nopass)
async def get_wifi_size_nopass(message: Message, state: FSMContext):
    data = await state.get_data()
    wifi_name_nopass = data.get('wifi_name_nopass')
    size = message.text
    await generate_nopass_wifi(wifi_name_nopass, size, message)
    await state.clear()

# Обработка события (Event QR)
@router.callback_query(F.data == 'qr_code_event')
async def qr_code_event(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(UserOptions.event_name)
    await callback_query.message.answer("Напишите название события")

@router.message(UserOptions.event_name)
async def get_event_name(message: Message, state: FSMContext):
    await state.update_data(event_name=message.text)
    await state.set_state(UserOptions.start_time_event)
    await message.answer("Введите дату и время начала события в формате YYYY M D H M\nПример: 2024 08 15 12 30")

@router.message(UserOptions.start_time_event)
async def get_start_time(message: Message, state: FSMContext):
    await state.update_data(start_time_event=message.text)
    await state.set_state(UserOptions.end_time_event)
    await message.answer("Введите дату и время окончания события в формате YYYY M D H M\nПример: 2024 08 15 16 45")

@router.message(UserOptions.end_time_event)
async def get_end_time(message: Message, state: FSMContext):
    await state.update_data(end_time_event=message.text)
    await state.set_state(UserOptions.location_event)
    await message.answer("Введите место проведения события")

@router.message(UserOptions.location_event)
async def get_location_event(message: Message, state: FSMContext):
    await state.update_data(location_event=message.text)
    await state.set_state(UserOptions.description_event)
    await message.answer("Введите описание события")

@router.message(UserOptions.description_event)
async def get_description_event(message: Message, state: FSMContext):
    await state.update_data(description_event=message.text)
    await state.set_state(UserOptions.size_event)
    await message.answer("Выберите размер QR кода (рекомендуемый размер - 15)", reply_markup=size_kb)

@router.message(UserOptions.size_event)
async def get_size_event(message: Message, state: FSMContext):
    await state.update_data(size_event=message.text)
    data = await state.get_data()
    await generate_event_qr(data, message)
    await state.clear()

# Обработка контактной карты (vCard)
@router.callback_query(F.data == 'qr_code_contactcard')
async def contactcard(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(UserOptions.name_vcard)
    await callback_query.message.answer("Напишите имя")

@router.message(UserOptions.name_vcard)
async def get_name_vcard(message: Message, state: FSMContext):
    await state.update_data(name_vcard=message.text)
    await state.set_state(UserOptions.company_vcard)
    await message.answer("Напишите название компании")

@router.message(UserOptions.company_vcard)
async def get_company_vcard(message: Message, state: FSMContext):
    await state.update_data(company_vcard=message.text)
    await state.set_state(UserOptions.phone_vcard)
    await message.answer("Напишите свой номер телефона")

@router.message(UserOptions.phone_vcard)
async def get_phone_vcard(message: Message, state: FSMContext):
    await state.update_data(phone_vcard=message.text)
    await state.set_state(UserOptions.email_vcard)
    await message.answer("Введите свою электронную почту")

@router.message(UserOptions.email_vcard)
async def get_email_vcard(message: Message, state: FSMContext):
    await state.update_data(email_vcard=message.text)
    await state.set_state(UserOptions.website_vcard)
    await message.answer("Введите адрес своего сайта")

@router.message(UserOptions.website_vcard)
async def get_website_vcard(message: Message, state: FSMContext):
    await state.update_data(website_vcard=message.text)
    await state.set_state(UserOptions.size_vcard)
    await message.answer("Выберите размер QR кода (рекомендуемый размер - 15)", reply_markup=size_kb)

@router.message(UserOptions.size_vcard)
async def get_size_vcard(message: Message, state: FSMContext):
    await state.update_data(size_vcard=message.text)
    data = await state.get_data()
    await generate_contact_card(data, message)
    await state.clear()

# Обработка всех остальных сообщений
@router.message()
async def error(message: Message):
    await message.answer("Ошибка. Попробуйте еще раз.")