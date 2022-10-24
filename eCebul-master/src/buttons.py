from aiogram.types import (
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    KeyboardButton
)

from aiogram.utils.callback_data import CallbackData
from db import title_shop

captcha_cb = CallbackData("cap", "answer")
party_select = CallbackData("sel", "act")
party = CallbackData("par", "act")
candidates_cb = CallbackData("can", "id")
vote_cb = CallbackData("vote", "id")


start_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Звичайно!")
        ],
        
    ],
    resize_keyboard=True
)

sex_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Чоловік")
        ],
        [
            KeyboardButton(text="Жінка")
        ],
        
    ],
    resize_keyboard=True
)  

complete = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Затвердити!")
        ],
        
    ],
    resize_keyboard=True
)

balance_reg = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="0")
        ],
        
    ],
    resize_keyboard=True
)  

job_reg = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Безробітній")
        ],
        [
            KeyboardButton(text='Президент')
        ],
        [
            KeyboardButton(text='Спікер')
        ], 
        [
            KeyboardButton(text='Віце-Спікер')
        ], 
        [
            KeyboardButton(text='Чатовий')
        ], 
        [
            KeyboardButton(text='Жандарм')
        ], 
        [
            KeyboardButton(text='Депутат')
        ], 
        [
            KeyboardButton(text='Міністр Внутрішніх Справ')
        ],
        [
            KeyboardButton(text='Міністр Оборони')
        ],
        [
            KeyboardButton(text='Міністр Економіки')
        ],
        [
            KeyboardButton(text='Верховний Суддя')
        ],
        [
            KeyboardButton(text='Помічник Судді')
        ],
        [
            KeyboardButton(text='Апеляційний Суддя')
        ]
    ],
    resize_keyboard=True
)

change_info = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="❌ Відсторонений, не має впливу на Державу")
        ],
        [
            KeyboardButton(text="🪆 Новачок, тільки приєднався до Держави!")
        ],
        [
            KeyboardButton(text="🎗️ Середняк, розуміє головні Державні аспекти!")
        ],
        [
            KeyboardButton(text="🎖️ Ветеран, знається на Державі")
        ],
        
    ],
    resize_keyboard=True
)

shop_info = InlineKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Аукціон")
        ],       
        [
            KeyboardButton(text='Магазини')
        ],
        [
            KeyboardButton(text="Моє багатство")
        ]
 
    ],
    resize_keyboard=True, one_time_keyboard=True
)



def shops(count: int):
    shop = InlineKeyboardMarkup()
    
    for i in range(0, count):
        shop_title = title_shop(id = i)[0][0]
        i = InlineKeyboardButton(shop_title, callback_data=i)
        shop.add(i)

def dicise_party(owner: int):
    dis = InlineKeyboardMarkup(row_width=2)
    dis.insert(InlineKeyboardButton(
        "Прийняти",
        callback_data=party_select.new(
            act="yes_"+str(owner)
        ))
    )
    dis.insert(InlineKeyboardButton(
        "Відхилити",
        callback_data=party_select.new(
            "no_"+str(owner)
        ))
    )
    return dis

def party_manage_keyboard(is_owner: bool):
    if is_owner:
        party_manage = InlineKeyboardMarkup(row_width=1)
        party_manage.add(InlineKeyboardButton(
            "Додати учасника",
            callback_data=party.new(act="add")
        ))
        party_manage.add(InlineKeyboardButton(
            "Видалити учасника",
            callback_data=party.new(act="delete")
        ))
        return party_manage
    else:
        return

def change_kb_gen(lor: int):
    change_kb = ...
    if lor == 5:
        change_kb = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="ім'я")
                ],
                [
                    KeyboardButton(text="прізвище")
                ],
                [
                    KeyboardButton(text="стать")
                ],
                [
                    KeyboardButton(text="тег")
                ],
                [
                    KeyboardButton(text="баланс")
                ],
                [
                    KeyboardButton(text="інфо")
                ],
                [
                    KeyboardButton(text="робота")
                ],
            ],
            resize_keyboard=True
        )
    elif lor == 4:
        change_kb = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="ім'я")
                ],
                [
                    KeyboardButton(text="прізвище")
                ],
                [
                    KeyboardButton(text="стать")
                ],
                [
                    KeyboardButton(text="тег")
                ],
                [
                    KeyboardButton(text="інфо")
                ],
                [
                    KeyboardButton(text="робота")
                ],
            ],
            resize_keyboard=True
        )
    elif lor == 3:
        change_kb = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="баланс")
                ],
            ],
            resize_keyboard=True
        )
    return change_kb

def gen_captcha_keyboard(correct, user_id):
    captcha = InlineKeyboardMarkup(row_width=1)
    for i in range(1, 5):
        if i != correct:
            captcha.add(InlineKeyboardButton(
                "Слава Цибулі",
                callback_data=captcha_cb.new(
                    answer="wrong_"+str(user_id)
                ))
            )
        else:
            captcha.add(InlineKeyboardButton(
                "Слава Цибулі",
                callback_data=captcha_cb.new(
                    answer="correct_"+str(user_id)
                ))
            )
    return captcha

def candidates_keyboard(candidats: dict):
    keyb = InlineKeyboardMarkup(row_width=1)
    for candidat in candidats:
        keyb.add(InlineKeyboardButton(
            "".join(
                [
                    candidats[candidat]["name"],
                    " ",
                    candidats[candidat]["surname"]
                ]
            ),
            callback_data=candidates_cb.new(id=str(candidats[candidat]["id"]))
        ))
    return keyb

def vote(id: int):
    id = str(id)
    keyb = InlineKeyboardMarkup()
    keyb.add(InlineKeyboardButton("Проголосувати", callback_data=vote_cb.new(id=id)))
    return keyb
