from aiogram.types import Message, FSInputFile
import segno
import tempfile
import asyncio
from datetime import datetime

# ? генерация QR кода
async def generate_qr(userlink, qrcode_size, message: Message):
    img = segno.make(userlink)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:

        img.save(tmp_file.name, scale=int(qrcode_size))
        qr_code_file = FSInputFile(tmp_file.name)
        await message.answer_photo(photo=qr_code_file, caption="Вот ваш QR код")


async def generate_pass_wifi(wifiname, wifipass, size, message: Message):
    img = segno.helpers.make_wifi(ssid=wifiname, password=wifipass, security='WPA')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:

        img.save(tmp_file.name, scale=int(size))
        qr_code_file = FSInputFile(tmp_file.name)
        await message.answer_photo(photo=qr_code_file, caption="Вот ваш QR код для WiFi с паролем")


async def generate_nopass_wifi(wifiname, size, message: Message):
    img = segno.helpers.make_wifi(ssid=wifiname, security='nopass')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:

        img.save(tmp_file.name, scale=int(size))
        qr_code_file = FSInputFile(tmp_file.name)
        await message.answer_photo(photo=qr_code_file, caption="Вот ваш QR код для открытого WiFi")


async def generate_event_qr(event_data, message: Message):
    # Получаем данные из словаря
    name = event_data.get('event_name')
    start_time = event_data.get('start_time_event')
    end_time = event_data.get('end_time_event')
    location = event_data.get('location_event')
    description = event_data.get('description_event')
    size = event_data.get('size_event')

    # Преобразуем ввод пользователя в формат даты и времени
    # Ожидается ввод в формате "YYYY M D H M"
    start_time_obj = datetime.strptime(start_time, "%Y %m %d %H %M")
    end_time_obj = datetime.strptime(end_time, "%Y %m %d %H %M")

    # Форматируем время для iCalendar
    start_time_ical = start_time_obj.strftime('%Y%m%dT%H%M%S')
    end_time_ical = end_time_obj.strftime('%Y%m%dT%H%M%S')

    # Формируем строку iCalendar
    event_calendar = f"""
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Your Organization//Your Product//EN
BEGIN:VEVENT
SUMMARY:{name}
DTSTART:{start_time_ical}
DTEND:{end_time_ical}
LOCATION:{location}
DESCRIPTION:{description}
END:VEVENT
END:VCALENDAR
    """

    img = segno.make(event_calendar)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:

        img.save(tmp_file.name, scale=int(size))
        qr_code_file = FSInputFile(tmp_file.name)
        await message.answer_photo(photo=qr_code_file, caption="Вот ваш QR код для события")


async def generate_contact_card(event_data, message: Message):
    name = event_data.get('name_vcard')
    company = event_data.get('company_vcard')
    phone = event_data.get('phone_vcard')
    email = event_data.get('email_vcard')
    website = event_data.get('website_vcard')
    size = event_data.get('size_vcard')

    vcard = f"""
BEGIN:VCARD
VERSION:3.0
FN:{name}
ORG:{company}
TEL:{phone}
EMAIL:{email}
URL:{website}
END:VCARD
    """

    img = segno.make(vcard)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:

        img.save(tmp_file.name, scale=int(size))
        qr_code_file = FSInputFile(tmp_file.name)
        await message.answer_photo(photo=qr_code_file, caption="Ваш QR код")