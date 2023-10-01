from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from .utils.get_user_language import get_user_language

class LanguageMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data: dict):
        # Отримуємо мову користувача з get_user_language.py
        user_id = message.from_user.id
        user_language = get_user_language(user_id)

        # Додаємо інформацію про мову до контексту повідомлення
        data['user_language'] = user_language
      
