from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

import texts, buttons, states

from main import DB, MAIN_CHAT, bot

async def create_vote(message: Message, state: FSMContext):
    #print header
    await states.Vote.create_vote_pass.set()
    await message.answer(text=texts.VOTE_STEPS[0])
    await states.Vote.next()

async def add_text(message: Message, state: FSMContext):
    #save header. print text
    async with state.proxy() as data: data['title'] = message.text
    await message.answer(text=texts.VOTE_STEPS[1])
    await states.Vote.next()

async def save_vote(message: Message, state: FSMContext):
    #save vote
    text = message.text
    async with state.proxy() as data: await DB.save_vote_info(data['title'], text)
    await message.answer(text=texts.VOTE_STEPS[2])
    await state.finish()

async def add_candidate(message: Message):
    command, id, candidate = message.text.split(" ", 2)
    await DB.save_candidates(id, candidate)
    await message.answer("Додано")

async def update_candidate(message: Message):
    command, id, candidate = message.text.split(" ", 2)
    await DB.update_candidates(id, candidate)
    await message.answer("Змінено")

async def list_candidates(message: Message):
    id = message.from_user.id
    VotedFor = await DB.get_voted_for()
    VoteInfo = await DB.get_vote_info()
    Candidates = await DB.get_candidates()
    #print("\n\n", VotedFor, "\n\n")
    Passport = await DB.get_passport(id)
    if Passport.status < 2:
        await message.answer("Тільки громадяні починая з середнього статусу мають право голосувати.")
        return 0
    
    if VotedFor != 0:
        for i in VotedFor:
            if i[0] == id:
                await message.answer("Ви не можете проголосувати в другий раз")
                return 0
    if VoteInfo != 0 and Candidates != 0:
        await message.answer(
            f"<b>{VoteInfo[0]}</b>\n\n{VoteInfo[1]}",
            reply_markup=buttons.candidates_keyboard(Candidates)  # type: ignore
        )
    else: await message.answer("Наразі голосування неможливе")

async def vote(query: CallbackQuery):
    await query.answer()
    id = int(query.data.removeprefix("vote:"))
    res = await DB.save_vote(query.from_user.id, id)
    if res == 0:
        await query.message.delete()
        await query.message.answer("Ви успішно проголосували")

async def end_vote(message: Message):
    VotedFor = await DB.get_voted_for()
    VoteInfo = await DB.get_vote_info()
    Candidates = await DB.get_candidates()
    results = {}
    #0: ["Генерал", 0]
    for i in Candidates: results[i[0]] = [i[1], 0]
    for i in VotedFor:
        Passport = await DB.get_passport(i[0])
        results[i[1]] = [results[i[1]][0], results[i[1]][1] + Passport.status-1]
    text = f"<b>{VoteInfo[0]}</b>\n\n{VoteInfo[1]}\n"
    for i in results: text += f'\n{results[i][0]} - {results[i][1]}'
    message = await bot.send_message(MAIN_CHAT, text)
    await message.pin(disable_notification=False)
    await DB.delete_vote()
