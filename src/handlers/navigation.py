from aiogram.types import Message

async def navig(msg: Message):
    await msg.reply("""
<b>Навігатор простору Республіки</b>

🍉 <a href="https://t.me/kavunstate">Основний Чат</a>
🛂 <a href="https://t.me/cebula_mvs">Представницький Комітет</a>
📰 <a href="https://t.me/cebulanews">Вісник Республіки</a>
⚜️  <a href="https://t.me/kavunlaw">Законодавство</a>
🛡️ <a href="https://t.me/+zZTUWDKMP6plM2Iy">Службовий Реєстр</a>
🚫 <a href="https://t.me/+x2xUHRW1E2w0MmZi">Миротворець</a>
""")
