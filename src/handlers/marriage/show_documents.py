from pyexpat.errors import messages
from aiogram.types import Message
from datetime import date

import texts
import variables

from main import DB

async def show_marriage_certificate(message:Message):
    marriage_certificate()
