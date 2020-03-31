import bot.message as msg

from aiogram import types
from aiogram.dispatcher import filters

from bot.core import dp
from bot.database import DBDriver
from bot.referral_link import ReferralLink


@dp.message_handler(filters.Regexp(msg.partner_msg))
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