from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData

def finish_registration_buttons():
    kbd = InlineKeyboardMarkup(inline_keyboard=[
        [ InlineKeyboardButton(text = "Завершить регистрацию ✒️", callback_data = "finish_registration")],
        [ InlineKeyboardButton(text = "Заполнить заново", callback_data = "again")]
    ])

    return kbd

