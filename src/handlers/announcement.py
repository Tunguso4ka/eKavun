from aiogram.types import Message

import texts
import variables

from main import DB, bot, LOG_CHANNEL, MAIN_CHAT, AUTHORISIED_CHATS

async def private_announce(message: Message):
    command, id, *text = message.text.split(" ", 2)
    text = " ".join(text)
    try: await bot.send_message(int(id), text)
    except Exception as e: await message.answer(f"Не можливо відислати повідомлення.\nПомилка {e}")

async def global_announce(message: Message):
    command, *text = message.text.split(" ", 1)
    text = " ".join(text)
    ids = await DB.get_all_ids()
    for i in ids:
        try: await bot.send_message(i[0], text)
        except Exception as e: await message.answer(f"Не можливо відислати повідомлення громадянину {i[0]}.\nПомилка {e}")

async def group_announce(message: Message):
    command, *text = message.text.split(" ", 1)
    text = " ".join(text)
    try:
        group_message = await bot.send_message(MAIN_CHAT, text)
        await group_message.pin(disable_notification=False)
    except Exception as e: await message.answer(f"Вийшла помилочка :'(\nПомилка {e}")

async def spy_on(message: Message):
    id=message.chat.id
    if id not in ([MAIN_CHAT, LOG_CHANNEL] + AUTHORISIED_CHATS): await bot.send_message(LOG_CHANNEL, f"<b>Повідомлення.</b>\n\n<b>Людина:</b>\n@{message.from_user.username}\n<code>{message.from_user.id}</code>\n<b>Чат:</b>\n<code>{message.chat.title}</code>\n<code>{message.chat.id}</code>\n<b>Текст:</b>\n<code>{message.text}</code>")
