from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="QR код с ссылкой", callback_data="qr_code_link")],
        [InlineKeyboardButton(text="QR код для wi-fi", callback_data="qr_code_wifi")],
        [InlineKeyboardButton(text="QR код для wi-fi (без пароля)", callback_data="qr_code_wifi_nopass")],
        [InlineKeyboardButton(text="QR код с событием", callback_data="qr_code_event")],
        [InlineKeyboardButton(text="QR код визитка", callback_data="qr_code_contactcard")],
    ]
)

size_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="10")],
        [KeyboardButton(text="15")],
        [KeyboardButton(text="20")],
    ]
)

wifi_answer_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="нет")],
        [KeyboardButton(text="да")],
    ]
)
