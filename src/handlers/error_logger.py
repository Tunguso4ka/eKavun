from aiogram.types import Update

from main import bot, dp, LOG_CHANNEL

async def error_notify(update: Update, exception):
    tag = ""
    id = 0
    chat = 0
    if "callback_query" in update:
        tag = update.callback_query.from_user.username
        id = update.callback_query.from_user.id
        chat_title = update.callback_query.message.chat.title
        chat_id = update.callback_query.message.chat.id
        command = update.callback_query.message.text
        await update.callback_query.message.reply(f"تحذير! خطأ فادح!\nВиникла помилочка :'(\n{exception}")
    elif "message" in update:
        tag = update.message.from_user.username
        id = update.message.from_user.id
        chat_title = update.message.chat.title
        chat_id = update.message.chat.id
        command = update.message.text
        await update.message.reply(f"تحذير! خطأ فادح!\nВиникла помилочка :'(\n{exception}")
    else:
        tag = "error"
        id=1
        chat_title=""
        chat_id = 1
        command=''
    #await bot.send_message(1013681916, f"Нова помилка {tag, id, chat}")
    await bot.send_message(LOG_CHANNEL, f"<b>Помилка.</b>\n\n<b>Людина:</b>\n@{tag}\n<code>{id}</code>\n<b>Чат:</b>\n<code>{chat_title}</code>\n<code>{chat_id}</code>\n<b>Команда:</b>\n<code>{command}</code>\n<b>Опис помилкі:</b>\n<code>{exception}</code>")
    state = dp.current_state(chat=chat, user=id)
    await state.finish()
    
