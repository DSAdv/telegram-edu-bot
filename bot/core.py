import json
import logging
import pandas as pd

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, filters
from aiogram.utils import executor


from bot.database import DBDriver
from bot.referral_link import ReferralLink
from bot import message
from config import Config


logging.basicConfig(level=logging.DEBUG)

bot = Bot(token=Config.TELEGRAM_TOKEN)
dp = Dispatcher(bot)


menu_keyboard = types.ReplyKeyboardMarkup()
menu_keyboard.add(types.KeyboardButton(message.course_msg))
menu_keyboard.add(types.KeyboardButton(message.partner_msg))
menu_keyboard.add(types.KeyboardButton(message.help_msg))


@dp.message_handler(commands=["start"])
async def process_start_command(message: types.Message):
    user_id = message.from_user.id
    if DBDriver.is_new_user(user_id):
        ref_code = ReferralLink.search_ref_code(message.text)
        user_dict = message.from_user.to_python()
        DBDriver.insert_user(user_dict, ref_code)
        logging.info(f"Added new user:\n {json.dumps(user_dict, indent=4)}")
    else:
        await message.reply(f"Привіт, {message.from_user.first_name}!\n"
                            f"Я допоможу тобі поринути в глибини Data Science.\n"
                            f"Все що потрібно від тебе, це лише трішки натхнення і систематичний підхід.",
                            reply_markup=menu_keyboard)


@dp.message_handler(filters.Regexp(message.partner_msg))
async def process_partner_msg(message: types.Message):
    user_id = message.from_user.id
    ref_code = DBDriver.get_user(user_id)["referral_code"]
    await message.reply(
        "Ти можеш дати своїм друзям можливість долучиться до бота\.\n"
        "Це дозволить отримати бонуси і тобі, і твоїм друзям\.\n\n"
        f"На даний момент у тебе запрошено: _{len(DBDriver.get_referral_users(ref_code))}_",
        parse_mode=types.ParseMode.MARKDOWN_V2
    )
    ref_link = ReferralLink.generate_ref_link(ref_code)
    await message.bot.send_message(
        message.from_user.id,
        f"Для любих друзів: {ref_link}"
    )




@dp.message_handler(content_types=["text"])
async def process(message: types.Message):
    await bot.send_message(message.from_user.id, message.text)


if __name__ == '__main__':
    executor.start_polling(dp)