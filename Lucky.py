from aiogram.dispatcher.filters import Command
from aiogram.types import Message

# Ось нова структура команд та їх обробники:
# (Команда)!я/
async def on_start(message: Message):
    # Логіка для команди (Команда)!я/
    pass

# (Команда)!я/магазин/
async def show_items(message: Message):
    # Логіка для команди (Команда)!я/магазин/
    pass

# (Команда)!я/ігри/
async def start_games(message: Message):
    # Логіка для команди (Команда)!я/ігри/
    pass

# (Команда)!я/настройки/
async def settings_menu(message: Message):
    # Логіка для команди (Команда)!я/настройки/
    pass

# (Команда)!я/видалити/
async def delete_account(message: Message):
    # Логіка для команди (Команда)!я/видалити/
    pass

# Додаємо нові команди та їх обробники до dp
dp.register_message_handler(on_start, CommandStart(), commands=["я"])
dp.register_message_handler(show_items, CommandStart(), commands=["я", "магазин"])
dp.register_message_handler(start_games, CommandStart(), commands=["я", "ігри"])
dp.register_message_handler(settings_menu, CommandStart(), commands=["я", "настройки"])
dp.register_message_handler(delete_account, CommandStart(), commands=["я", "видалити"])
