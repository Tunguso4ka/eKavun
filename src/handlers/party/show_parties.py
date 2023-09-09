from aiogram.types import Message

import texts

from main import DB

async def show_parties(msg: Message):
    list_of_parties = await DB.get_all()
    if list_of_parties:
        text = "<b>Політичні партії\nКавуневої Республіки\n</b>"
        for party in list_of_parties:
            owner_passport = await DB.get_passport(id=party.owner)
            members = await DB.get_members(party_id=party.id)
            if owner_passport and members:
                party_text = texts.PARTIES[1].format(
                    name=party.name,
                    username=owner_passport.username[1::],
                    owner_name=owner_passport.name,
                    owner_surname=owner_passport.surname,
                    members_count=len(members)
                )
                text = "\n".join([text, party_text])
        await msg.reply(text)
    else:
        await msg.reply("Поки партій нема. Створіть першу!")
