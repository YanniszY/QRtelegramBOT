from aiogram.fsm.state import State, StatesGroup

class UserOptions(StatesGroup):
    link = State()
    link_size = State()
    
    wifi_name = State()
    wifi_pass = State()
    wifi_size = State()

    wifi_name_nopass = State()
    wifi_size_nopass = State()

    event_name = State()
    start_time_event = State()
    end_time_event = State()
    location_event = State()
    description_event = State()
    size_event = State()

    name_vcard = State()
    company_vcard = State()
    phone_vcard = State()
    email_vcard = State()
    website_vcard = State()
    size_vcard = State()