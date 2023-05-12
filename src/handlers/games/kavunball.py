from pyexpat.errors import messages
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from main import DB

import texts, variables, random, states, buttons

async def game_bot(message: Message):
    command, amount = message.text.split()
    bet = int(amount)
    if bet < 0: bet = 0
    passport = await DB.get_passport(id=message.from_user.id)
    if passport.balance >= bet:
        your_kavun = random.randint(0,50)
        enemy_kavun = random.randint(0,50)
        result = 1
        if your_kavun > enemy_kavun: result = 0; passport.balance += bet
        elif your_kavun == enemy_kavun: result = 1
        else: result = 2
        text = texts.KAVUNBALL.format(
            your_kavun = your_kavun,
            your_kavun_map = "<u>" + "_" * your_kavun + "</u>🍉<u>" + "_" * (50 - your_kavun) + "</u>",
            enemy_kavun = enemy_kavun,
            enemy_kavun_map = "<u>" + "_" * enemy_kavun + "</u>🍉<u>" + "_" * (50 - enemy_kavun) + "</u>",
            result = variables.KAVUNS[result])
        await message.answer(text)
        if result == 0: await DB.update_passport(column="balance", id=passport.id, data=passport.balance)
        elif result == 2: await DB.replenish_money(1, user_id=passport.id, amount=bet)
    else: await message.answer(texts.NO_MONEY)

async def get_bet(message: Message, state: FSMContext):
    await states.KavunBall.get_bet_pass.set()
    your_passport = await DB.get_passport(id=message.from_user.id)
    enemy_passport = await DB.get_passport(id=message.reply_to_message.from_user.id)
    if your_passport and enemy_passport:
        await state.update_data(your_passport=your_passport, enemy_passport=enemy_passport)
        await message.answer('👀 <b>Введіть ставку для початку кидання</b>')
        await states.KavunBall.next()
    else:
        await message.answer(texts.PASSPORT_DO_NOT_EXIST)
        await state.finish()

async def bet_proposal(message: Message, state: FSMContext):
    async with state.proxy() as data:
        try: data['bet'] = int(message.text)
        except: state.finish(); return
        await message.answer(
            "🤯 <b>Користувач надіслав вам пропозицію кинути кавуна</b>",
            reply_markup=buttons.kavunball_bet_buttons(
                data["your_passport"].id,
                data["enemy_passport"].id,
                data["your_passport"].balance,
                data["enemy_passport"].balance,
                data['bet'])
        )
        await state.finish()

async def bet_declined(query: CallbackQuery, state: FSMContext):
    await query.answer()
    data = query.data.split(":")
    id1, id2 = int(data[1]), int(data[2])
    #print("ВІДХИЛЕНО")
    if query.from_user.id == id2:
        await query.message.answer("Ставку відхилено")
        await query.message.edit_reply_markup(InlineKeyboardMarkup())

async def bet_accepted(query: CallbackQuery):
    await query.answer()
    qdata = query.data.split(":")
    id1, id2, your_balance, enemy_balance, bet = int(qdata[1]), int(qdata[2]), int(qdata[3]), int(qdata[4]), int(qdata[5])
    #print("ПРИЙНЯТО")
    if query.from_user.id != id2: return
    await query.message.edit_reply_markup(InlineKeyboardMarkup())
    if your_balance >= bet and enemy_balance >= bet:
        your_kavun = random.randint(0,20)
        enemy_kavun = random.randint(0,20)
        result = 1
        if your_kavun > enemy_kavun: result = 0; your_balance += bet; enemy_balance -= bet
        elif your_kavun == enemy_kavun: result = 1
        else: result = 2; your_balance -= bet; enemy_balance += bet
        text = texts.KAVUNBALL.format(
            your_kavun = your_kavun,
            your_kavun_map = "<u>" + "_" * your_kavun + "</u>🍉<u>" + "_" * (50 - your_kavun) + "</u>",
            enemy_kavun = enemy_kavun,
            enemy_kavun_map = "<u>" + "_" * enemy_kavun + "</u>🍉<u>" + "_" * (50 - enemy_kavun) + "</u>",
            result = variables.KAVUNS[result])
        await query.message.answer(text)
        await DB.update_passport(column="balance", id=id1, data=your_balance)
        await DB.update_passport(column="balance", id=id2, data=enemy_balance)
    else: await query.message.answer(texts.NO_MONEY)
