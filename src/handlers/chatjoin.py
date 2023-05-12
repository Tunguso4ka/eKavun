from aiogram.types import Message

import texts
import variables

from main import DB, bot, LOG_CHANNEL

async def new_request(message: Message):
    await message.answer(LOG_CHANNEL, f"Тест\n{message.from_user.title, message.from_user.id}")
