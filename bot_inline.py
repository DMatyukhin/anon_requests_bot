import asyncio
import logging
import os
from collections import OrderedDict
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from dotenv import load_dotenv

# --------------------
# Конфигурация
# --------------------

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
MAX_USERS = 10  # ограничение на кэш

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Словарь user_id -> код (U001...U010)
user_codes = OrderedDict()
# Обратный словарь код -> user_id
code_to_user = {}

# Админ в "режиме ответа": admin_id -> user_code
admin_reply_mode = {}

code_counter = 1


def get_or_assign_code(user_id: int) -> str:
    """Присвоить пользователю уникальный код или вернуть существующий"""
    global code_counter

    if user_id in user_codes:
        return user_codes[user_id]

    if len(user_codes) >= MAX_USERS:
        oldest_user, oldest_code = user_codes.popitem(last=False)
        del code_to_user[oldest_code]

    code = f"U{code_counter:03d}"
    code_counter_plus = code_counter + 1
    globals()["code_counter"] = code_counter_plus if code_counter_plus <= 999 else 1

    user_codes[user_id] = code
    code_to_user[code] = user_id
    return code


# --------------------
# Старт
# --------------------
@dp.message(Command("start"))
async def start_cmd(message: Message):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Написать анонимное сообщение", callback_data="write_admin")]
        ]
    )
    await message.answer("Нажмите кнопку, чтобы анонимно написать админу.", reply_markup=kb)


# --------------------
# Пользователь начинает диалог
# --------------------
@dp.callback_query(F.data == "write_admin")
async def user_start_dialog(callback: CallbackQuery):
    code = get_or_assign_code(callback.from_user.id)
    await callback.message.answer(
        f"Вам присвоили код <b>{code}</b>. Теперь можете анонимно написать свое сообщение, "
        f"а психолог увидит только код.",
        parse_mode="HTML"
    )
    await callback.answer()


# --------------------
# Пользователь пишет админу
# --------------------
@dp.message(F.text & (F.from_user.id != ADMIN_ID))
async def forward_to_admin(message: Message):
    code = get_or_assign_code(message.from_user.id)
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"Ответить {code}", callback_data=f"reply:{code}")]
        ]
    )
    await bot.send_message(
        ADMIN_ID,
        f"✉️ Сообщение от <b>{code}</b>:\n\n{message.text}",
        parse_mode="HTML",
        reply_markup=kb
    )


# --------------------
# Админ нажал кнопку "Ответить"
# --------------------
@dp.callback_query(F.data.startswith("reply:"))
async def admin_choose_reply(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        return

    code = callback.data.split(":", 1)[1]
    if code not in code_to_user:
        await callback.answer("❌ Пользователь недоступен.")
        return

    admin_reply_mode[callback.from_user.id] = code
    await callback.message.answer(
        f"✏️ Введите ответ для <b>{code}</b>:",
        parse_mode="HTML"
    )
    await callback.answer()


# --------------------
# Админ пишет ответ после нажатия кнопки
# --------------------
@dp.message(F.from_user.id == ADMIN_ID)
async def handle_admin_message(message: Message):
    if message.from_user.id in admin_reply_mode:
        code = admin_reply_mode[message.from_user.id]
        user_id = code_to_user.get(code)
        if user_id:
            await bot.send_message(user_id, f"💬 Ответ психолога:\n\n{message.text}")
            await message.answer(f"✅ Ответ отправлен пользователю {code}")
        else:
            await message.answer("❌ Пользователь недоступен.")
        # выходим из режима ответа
        del admin_reply_mode[message.from_user.id]
    else:
        await message.answer("ℹ️ Чтобы ответить пациенту, нажмите кнопку под его сообщением.")


# --------------------
# Запуск
# --------------------
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
