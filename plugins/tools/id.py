from pyrogram import Client, filters
from plugins.utility.db import *

@Client.on_message(filters.command(commands=['id', 'info', 'me'], prefixes=['/', '.']))
async def get_id(bot, message):
    # By default, fetch the info of the user who sent the command
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    username = message.from_user.username
    chat_id = message.chat.id

    if message.chat.type in ['group', 'supergroup'] and message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        first_name = message.reply_to_message.from_user.first_name
        username = message.reply_to_message.from_user.username
        chat_id = message.reply_to_message.chat.id

    rank = await get_user_rank(user_id)
    expire = await get_user_expiry(user_id) if await get_user_expiry(user_id) else 'No expiry'

    if message.chat.type == 'private':
        await message.reply_text(f'''
<b>[<a href="https://t.me/Instuff_bot">⌥</a>]</b> 𝐔𝐬𝐞𝐫 𝐈𝐧𝐟𝐨𝐫𝐦𝐚𝐭𝐢𝐨𝐧
━━━━━━━━━━━━━━━━
<b>[<a href="https://t.me/Instuff_bot">⌬</a>]</b> 𝐍𝐚𝐦𝐞: {first_name}
<b>[<a href="https://t.me/Instuff_bot">⌬</a>]</b> 𝐔𝐬𝐞𝐫𝐧𝐚𝐦𝐞: @{username}
<b>[<a href="https://t.me/Instuff_bot">⌬</a>]</b> 𝐔𝐬𝐞𝐫 𝐈𝐃: <code>{user_id}</code>
<b>[<a href="https://t.me/Instuff_bot">⌬</a>]</b> 𝐂𝐡𝐚𝐭 𝐈𝐃: <code>{chat_id}</code>
<b>[<a href="https://t.me/Instuff_bot">⌬</a>]</b> 𝐑𝐚𝐧𝐤: <b>{rank}</b>
<b>[<a href="https://t.me/Instuff_bot">⌬</a>]</b> 𝐄𝐱𝐩𝐢𝐫𝐲: <b>{expire}</b>
━━━━━━━━━━━━━━━━
<b>[<a href="https://t.me/Instuff_bot">⌤</a>]</b> 𝐃𝐞𝐯 𝐛𝐲: <code>@XxFakundoxX</code> 🍀
''', quote=True, disable_web_page_preview=True)

    else:
        if message.reply_to_message:
            await message.reply_text(f'''
<b>[<a href="https://t.me/Instuff_bot">⌥</a>]</b> 𝐑𝐞𝐩𝐥𝐢𝐞𝐝 𝐔𝐬𝐞𝐫 𝐈𝐧𝐟𝐨𝐫𝐦𝐚𝐭𝐢𝐨𝐧
━━━━━━━━━━━━━━━━
<b>[<a href="https://t.me/Instuff_bot">⌬</a>]</b> 𝐍𝐚𝐦𝐞: {first_name}
<b>[<a href="https://t.me/Instuff_bot">⌬</a>]</b> 𝐔𝐬𝐞𝐫𝐧𝐚𝐦𝐞: @{username}
<b>[<a href="https://t.me/Instuff_bot">⌬</a>]</b> 𝐔𝐬𝐞𝐫 𝐈𝐃: <code>{user_id}</code>
<b>[<a href="https://t.me/Instuff_bot">⌬</a>]</b> 𝐂𝐡𝐚𝐭 𝐈𝐃: <code>{chat_id}</code>
<b>[<a href="https://t.me/Instuff_bot">⌬</a>]</b> 𝐑𝐚𝐧𝐤: <b>{rank}</b>
<b>[<a href="https://t.me/Instuff_bot">⌬</a>]</b> 𝐄𝐱𝐩𝐢𝐫𝐲: <b>{expire}</b>
━━━━━━━━━━━━━━━━
<b>[<a href="https://t.me/Instuff_bot">⌤</a>]</b> 𝐃𝐞𝐯 𝐛𝐲: <code>@XxFakundoxX</code> 🍀
''', quote=True,disable_web_page_preview=True)
        else:
            await message.reply_text(f'''
<b>[<a href="https://t.me/Instuff_bot">⌥</a>]</b> 𝐘𝐨𝐮𝐫 𝐈𝐧𝐟𝐨𝐫𝐦𝐚𝐭𝐢𝐨𝐧
━━━━━━━━━━━━━━━━
<b>[<a href="https://t.me/Instuff_bot">⌬</a>]</b> 𝐍𝐚𝐦𝐞: {first_name}
<b>[<a href="https://t.me/Instuff_bot">⌬</a>]</b> 𝐔𝐬𝐞𝐫𝐧𝐚𝐦𝐞: @{username}
<b>[<a href="https://t.me/Instuff_bot">⌬</a>]</b> 𝐔𝐬𝐞𝐫 𝐈𝐃: <code>{user_id}</code>
<b>[<a href="https://t.me/Instuff_bot">⌬</a>]</b> 𝐂𝐡𝐚𝐭 𝐈𝐃: <code>{chat_id}</code>
<b>[<a href="https://t.me/Instuff_bot">⌬</a>]</b> 𝐑𝐚𝐧𝐤: <b>{rank}</b>
<b>[<a href="https://t.me/Instuff_bot">⌬</a>]</b> 𝐄𝐱𝐩𝐢𝐫𝐲: <b>{expire}</b>
━━━━━━━━━━━━━━━━
<b>[<a href="https://t.me/Instuff_bot">⌤</a>]</b> 𝐃𝐞𝐯 𝐛𝐲: <code>@XxFakundoxX</code> 🍀
''', quote=True,disable_web_page_preview=True)
