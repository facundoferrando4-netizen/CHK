import re
import time
import asyncio
import httpx
from proxy import proxies_aiohttp
from pyrogram import Client, filters
from Gates.skbasedoff import skintoff  # Ensure this function is async and non-blocking
from plugins.utility.db import get_user_rank, is_user_authorized, OWNER_ID, is_user_registered, update_credits, get_user_credits
from plugins.utility.antispam import is_spamming
from plugins.utility.banbin import is_bin_banned
from luhn import luhn_verification
from commands_status import get_command_status

# Function to process a single card
async def process_card(cc_data, user_id):
    cc, mm, yy, cvv = cc_data
    if len(yy) == 2:
        yy = '20' + yy
    cccc = f"{cc}|{mm}|{yy}|{cvv}"

    if not luhn_verification(cc):
        return f"<code>{cccc}</code>\nStatus: Invalid card number (Luhn check failed)"
    
    is_ban = await is_bin_banned(cc[:6])
    if is_ban:
        return f'<code>{cccc}</code>\nStatus: Banned BIN'

    try:
        prx = await proxies_aiohttp()
        session = httpx.AsyncClient(proxies=prx, timeout= 30)
        msg = await skintoff(session,cc, mm, yy, cvv) 
    except Exception as e:
        return f"<code>{cccc}</code>\nStatus: Error: {str(e)}"

    status = '𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅' if any(
        error_msg in msg for error_msg in [
            "Your card's security code is incorrect.",
            'Succeeded',
            "Charged $1",
            'Your card has insufficient funds.',
            'Insufficient Funds',
            'Transaction Not Allowed',
            'Your card does not support this type of purchase.',
            '3D Secure authentication required',
            "Incorrect Cvc",
            "Invalid Cvc",
            "CVV Live",
        ]
    ) else '𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌'

    return f"<code>{cccc}</code>\n𝐒𝐭𝐚𝐭𝐮𝐬: {status}\n𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: {msg}"

@Client.on_message(filters.command("msv", prefixes=["/", "."]))
async def mst(client, message):
    user_id = message.from_user.id
    first_n = message.from_user.first_name
    mid = message.id

    # Check if command is turned off
    if get_command_status('msv') == 'off':
        await message.reply_text("Gate is on maintenance, come back later.", reply_to_message_id=mid)
        return

    # Check if the user is registered
    if not await is_user_registered(user_id):
        await message.reply_text("Please register first using the /register command.", reply_to_message_id=mid)
        return

    # Check if the user is authorized
    is_authorized = await is_user_authorized(user_id)
    if not is_authorized:
        await message.reply_text(
            "Free users are not allowed to use this command.\nTo purchase a bot subscription, use '/buy' for details.",
            reply_to_message_id=mid
        )
        return

    # Anti-spam mechanism for non-owner users
    if user_id != OWNER_ID:
        is_spam, spam_message = is_spamming(user_id, is_authorized)
        if is_spam:
            await message.reply_text(spam_message, reply_to_message_id=mid)
            return

    # Check if the user has enough credits
    user_credits = await get_user_credits(user_id) or 0

    # Parse and validate card details
    ccs = message.text.split('msv ', 1)[1].strip() if 'msv ' in message.text else (message.reply_to_message.text.strip() if message.reply_to_message else None)
    if not ccs:
        await message.reply('Please enter card details.', reply_to_message_id=mid)
        return

    # Reformat and validate card information
    ccs = re.sub(r'[ /\\:]', '|', ccs)
    cc_list = re.findall(r'\b(\d{15}|\d{16})\|(\d{2}|\d{4})\|(\d{4}|\d{2})\|(\d{4}|\d{3})', ccs)
    card_count = len(cc_list)

    if card_count == 0:
        await message.reply('Invalid format! Use: XXXXXXXXXXXXXXXX|MM|YYYY|CVV', reply_to_message_id=mid)
        return
    if user_id != OWNER_ID and card_count > 20:
        await message.reply(f"You can process a maximum of 20 cards at a time. You tried to process {card_count}.", reply_to_message_id=mid)
        return
    if user_credits < card_count:
        await message.reply(f"Insufficient credits. You have {user_credits} credits, but {card_count} cards require {card_count} credits.", reply_to_message_id=mid)
        return

    # Processing message
    a = await message.reply('Processing...', reply_to_message_id=mid)
    start_time = time.perf_counter()

    batch_size = max(10, min(20, card_count // 2))  # Adjust based on card count
    results = []
    tasks = [process_card(cc, user_id) for cc in cc_list]

    for i in range(0, len(tasks), batch_size):
        batch_tasks = tasks[i:i + batch_size]
        batch_results = await asyncio.gather(*batch_tasks)
        results.extend(batch_results)
        
    await update_credits(user_id, -card_count)
    rank = await get_user_rank(user_id)

    end_time = time.perf_counter()
    total_time = f"{end_time - start_time:.2f}"
    updated_credits = await get_user_credits(user_id)

    result_message = "\n<b>- - - - - - - - - - - - - - - - - - - - - - - -</b>\n".join(results)
    result_message += f'''\n\n<b>[<a href="https://t.me/Instuff_bot">ϟ</a>]</b> 𝐆𝐚𝐭𝐞𝐰𝐚𝐲: Sk Based $1 
<b>[<a href="https://t.me/Instuff_bot">ϟ</a>]</b> 𝐂𝐫𝐞𝐝𝐢𝐭𝐬: <code>{updated_credits}</code>
<b>[<a href="https://t.me/Instuff_bot">⌥</a>]</b> 𝐓𝐢𝐦𝐞: <code>{total_time}</code> 𝐬𝐞𝐜𝐨𝐧𝐝𝐬
<b>[<a href="https://t.me/Instuff_bot">⎇</a>]</b> 𝐂𝐡𝐞𝐜𝐤𝐞𝐝 𝐛𝐲: <a href="tg://user?id={user_id}">{first_n}</a> <b>[{rank}]</b>
━━━━━━━━━━━━
<b>[<a href="https://t.me/Instuff_bot">⌤</a>]</b> 𝐃𝐞𝐯 𝐛𝐲: <code>@XxFakundoxX</code> 🍀
'''

    # Edit the message with the final results
    await a.edit(result_message, disable_web_page_preview=True)
