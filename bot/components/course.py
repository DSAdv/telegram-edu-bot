import bot.message as msg
import pandas as pd

from aiogram import types
from aiogram.dispatcher import filters
from bot.core import dp


@dp.message_handler(filters.Regexp(msg.course_msg))
async def process_course_command(message: types.Message):
    await message.reply("Список статей:")