from aiogram.fsm.state import  State, StatesGroup

class FSMFillForm(StatesGroup):
    fill_surname = State()
    fill_name = State()
    fill_mid_name = State()
    fill_grade = State()
    fill_group = State()

class FSMFillevent(StatesGroup):
    fill_name_event = State()
    fill_date_event = State()
    fill_kvota = State()
    fill_place_event = State()
    fill_info_event = State()
    fill_details_event = State()
    fill_registration_expire_date = State()
    fill_points = State()

class RegistrationState(StatesGroup):
    waiting_for_ticket = State()
    waiting_for_confirmation = State()
    opening_menu = State()
    show_my_events = State()
    show_current_events = State()
    add_event = State()
    show_cancel_events = State()
    enter_reason = State()
    select_event = State()
    show_registered_members = State()
    show_information_events = State()
    fill_name_event = State()
    fill_date_event = State()
    fill_kvota = State()
    fill_place_event = State()
    fill_info_event = State()
    fill_details_event = State()
    fill_registration_expire_date = State()
    fill_points = State()