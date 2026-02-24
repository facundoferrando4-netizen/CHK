from pyrogram import Client, filters
from plugins.utility.db import *

@Client.on_message(filters.command("buy", prefixes=["/", "."]))
async def buy_command(bot, message):
    user_id = message.from_user.id
    if not await is_user_registered(user_id):
        await message.reply_text("You are not registered. Use /register to register.")
        return
    text = f'''<b>
Prices :-
━━━━━━━━━━━━━
1 days - 7 USDT  ||  
7 days - 15 USDT  ||  
15 days - 20 USDT  ||  
30 days - 35 USDT  ||  
━━━━━━━━━━━━━
Low anti-spam , cheap , fast,  added HQ gates  ⚡️

Payment Methods - Binance / Crypto
━━━━━━━━━━━━━
For more details join @XxFakundoxX
Price list - <a href="https://t.me/+9CBJ9211b3pkMzNh">Click here</a>
━━━━━━━━━━━━━
If you interested to buy contact @XxFakundoxX. ⭐
</b>'''
    await message.reply_text(text, quote=True, disable_web_page_preview=True)