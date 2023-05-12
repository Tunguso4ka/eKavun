from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext

import texts
import states
import variables

from main import DB

async def based(message: Message):
    #print("УВАГА БАЗА")a
    your_passport = await DB.get_passport(id=message.from_user.id)
    target_passport = await DB.get_passport(id=message.reply_to_message.from_user.id)
    if not your_passport or not target_passport: await message.answer(texts.PASSPORT_DO_NOT_EXIST); return
    if target_passport != your_passport:
        await message.answer(f"😇 <b>{your_passport.name} {your_passport.surname} збільшив(-ла) репутацію {target_passport.name} {target_passport.surname} до {target_passport.reputation+1}</b>")
        await DB.update_passport(column="reputation", id=target_passport.id, data=(target_passport.reputation + 1))

async def cringe(message: Message):
    #print("ФУ КРІНЖА")
    your_passport = await DB.get_passport(id=message.from_user.id)
    target_passport = await DB.get_passport(id=message.reply_to_message.from_user.id)
    if not your_passport or not target_passport: await message.answer(texts.PASSPORT_DO_NOT_EXIST); return
    if target_passport != your_passport:
        await message.answer(f"😡 <b>{your_passport.name} {your_passport.surname} зменшив(-ла) репутацію {target_passport.name} {target_passport.surname} до {target_passport.reputation-1}</b>")
        await DB.update_passport(column="reputation", id=target_passport.id, data=(target_passport.reputation - 1))
