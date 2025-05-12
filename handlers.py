import asyncio
from aiogram import types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from config import CHANNEL_ID
from states import Form
from keyboards import menu_keyboard
from api import get_allocation

async def sub_checker(message: types.Message, is_start: bool = False) -> bool:
    try:
        member = await message.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=message.from_user.id)
        if member.status not in ["member", "administrator", "creator"]:
            await message.answer(f"Чтобы пользоваться ботом, подпишитесь на канал {CHANNEL_ID}!")
            return False
    except Exception as e:
        await message.answer(f"Ошибка проверки подписки: {e}\nПопробуйте позже.")
        return False

    if is_start:
        await message.answer("Привет! Выбери чекер:", reply_markup=menu_keyboard)
    return True

async def cmd_start(message: types.Message):
    if not await sub_checker(message, is_start=True):
        return

async def jup_checker_handler(message: types.Message, state: FSMContext):
    if not await sub_checker(message):
        return
    await state.set_state(Form.waiting_for_addresses_jup)
    await message.answer("Введите адрес(а) для проверки:")

async def kiloex_checker_handler(message: types.Message, state: FSMContext):
    if not await sub_checker(message):
        return
    await state.set_state(Form.waiting_for_addresses_kiloex)
    await message.answer("Введите адрес(а) для проверки:")

async def hyperlane_checker_handler(message: types.Message, state: FSMContext):
    if not await sub_checker(message):
        return
    await state.set_state(Form.waiting_for_addresses_hyperlane)
    await message.answer("Введите адрес(а) для проверки:")

async def process_addresses(message: types.Message, state: FSMContext):
    if not await sub_checker(message):
        return
    current_state = await state.get_state()
    addresses = [line.strip() for line in message.text.splitlines() if line.strip()]
    if len(addresses) > 50: 
        await message.answer("Слишком много адресов. Максимум — 50.")
        return
    
    valid_addresses = []
    invalid_addresses = []

    for addr in addresses:
        if 40 <= len(addr) <= 50:
            valid_addresses.append(addr)
        else:
            invalid_addresses.append(addr)

    if invalid_addresses:
        await message.answer(
            "Некорректно введен адрес:\n" +
            "\n".join(invalid_addresses) +
            "\nУдалите его из списка и повторите попытку"
        )
        return

    if not valid_addresses:
        await message.answer("Не получены адреса.")
        return

    await message.answer("Обработка адресов...")
    results = []
    #platform = "jup" if current_state == Form.waiting_for_addresses_jup.state else "kiloex" if current_state == Form.waiting_for_addresses_kiloex.state else "hyperlane"
    platforms = {
        Form.waiting_for_addresses_jup.state: "jup",
        Form.waiting_for_addresses_kiloex.state: "kiloex",
        Form.waiting_for_addresses_hyperlane.state: "hyperlane",
    }

    platform = platforms[current_state]

    for addr in valid_addresses:
        result = await get_allocation(addr, platform)
        results.append(result)
        await asyncio.sleep(0.1)
    await message.answer("\n".join(results))
    await state.clear()
