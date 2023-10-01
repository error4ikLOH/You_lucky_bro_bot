from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Початковий стан
class StateMachine(Enum):
    START = "start"
    SHOP = "shop"
    BUY_ITEM = "buy_item"

# Команда !я
@dp.message_handler(commands=['я'])
async def start_game(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_balance = 100  # По дефолту 100 грн (або руб або доларів, залежно від мови користувача)

    # Отримуємо дані ігрока з бази даних або зберігаємо їх в деяких змінних

    # Відправляємо повідомлення з даними користувача
    await message.answer(f"Ваше ім'я: {message.from_user.username}\n"
                         f"Ваш баланс: {user_balance} грн\n"
                         f"Ваші предмети: {', '.join(user_items)}", reply_markup=main_menu_keyboard)

# Обробник кнопки "Магазин"
@dp.callback_query_handler(lambda query: query.data.startswith('shop'))
async def show_shop_items(query: types.CallbackQuery, state: FSMContext):
    await query.message.delete()

    # Отримуємо список предметів з бази даних або іншого джерела
    items = [("медведик🐻", 75), ("яхта🛥️", 100), ("будинок🏡", 50)]

    markup = InlineKeyboardMarkup(row_width=2)
    for item_name, item_price in items:
        markup.add(InlineKeyboardButton(f"{item_name} ({item_price} грн)", callback_data=f"buy_item_{item_name}"))

    markup.add(InlineKeyboardButton("Назад", callback_data="back_to_main_menu"))

    await query.message.answer("Список предметів:", reply_markup=markup)
    await StateMachine.SHOP.set()

# Обробник кнопок предметів в магазині
@dp.callback_query_handler(lambda query: query.data.startswith('buy_item'), state=StateMachine.SHOP)
async def buy_item(query: types.CallbackQuery, state: FSMContext):
    await query.message.delete()

    item_name = query.data.split('_')[1]  # Отримуємо назву предмета з data
    item_price = get_item_price(item_name)  # Отримуємо ціну предмета з бази даних або іншого джерела

    user_balance = get_user_balance(query.from_user.id)  # Отримуємо баланс користувача з бази даних або іншого джерела

    if user_balance >= item_price:
        # Віднімаємо ціну предмета з балансу користувача
        new_balance = user_balance - item_price
        update_user_balance(query.from_user.id, new_balance)  # Оновлюємо баланс користувача в базі даних

        # Додаємо предмет до списку предметів користувача
        add_item_to_user(query.from_user.id, item_name)  # Додавання предмета до списку користувача в базі даних

        await query.message.answer(f"Ви успішно придбали {item_name} за {item_price} грн.")
    else:
        await query.message.answer("У вас недостатньо коштів для придбання цього предмета.")

    await StateMachine.START.set()  # Повертаємося в початковий стан

# Обробник кнопки "Назад" в магазині або інших меню
@dp.callback_query_handler(lambda query: query.data == 'back_to_main_menu', state=[StateMachine.SHOP, StateMachine.BUY_ITEM])
async def back_to_main_menu(query: types.CallbackQuery, state: FSMContext):
    await query.message.delete()
    await StateMachine.START.set()  # Повертаємося в початковий стан
    await start_game(query.message, state)
  
