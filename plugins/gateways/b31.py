from pyrogram import Client, filters
from Gates.b31 import B3_Auth1
from plugins.utility.db import get_user_rank , is_user_authorized , OWNER_ID,is_user_registered
from plugins.utility.antispam import is_spamming
from plugins.utility.binreq import bin_data
from plugins.utility.banbin import is_bin_banned
from luhn import luhn_verification
from commands_status import get_command_status
import re,time
@Client.on_message(filters.command("chk" , prefixes=["/", "."]))
async def chk(client, message):
    user_id = message.from_user.id
    first_n = message.from_user.first_name
    mid = message.id

    if get_command_status('chk') == 'off':
         await message.reply_text("Gate is on maintenance, come back later.", reply_to_message_id=mid)
         return
    if not await is_user_registered(user_id):
         await message.reply_text("𝐏𝐥𝐞𝐚𝐬𝐞 𝐫𝐞𝐠𝐢𝐬𝐭𝐞𝐫 𝐟𝐢𝐫𝐬𝐭 𝐮𝐬𝐢𝐧𝐠 𝐭𝐡𝐞 /register 𝐜𝐨𝐦𝐦𝐚𝐧𝐝.", reply_to_message_id=mid)
         return
    
    is_authorized = await is_user_authorized(user_id)
    if not is_authorized:
        txt = f'''
𝐅𝐫𝐞𝐞 𝐮𝐬𝐞𝐫 𝐢𝐬 𝐧𝐨𝐭 𝐚𝐥𝐥𝐨𝐰𝐞𝐝 𝐭𝐨 𝐮𝐬𝐞 𝐭𝐡𝐢𝐬 𝐜𝐨𝐦𝐦𝐚𝐧𝐝.
━━━━━━━━━━━━
𝐈𝐟 𝐲𝐨𝐮 𝐰𝐚𝐧𝐭 𝐭𝐨 𝐩𝐮𝐫𝐜𝐡𝐚𝐬𝐞 𝐛𝐨𝐭 𝐬𝐮𝐛𝐬𝐜𝐫𝐢𝐩𝐭𝐢𝐨𝐧 𝐮𝐬𝐞 '/buy' 𝐜𝐨𝐦𝐦𝐚𝐧𝐝 𝐟𝐨𝐫 𝐦𝐨𝐫𝐞 𝐝𝐞𝐭𝐚𝐢𝐥𝐬.
'''
        await message.reply_text(txt, reply_to_message_id=mid)
        return
    if user_id != OWNER_ID:
        is_spam, spam_message = is_spamming(user_id, is_authorized)
        if is_spam:
            await message.reply_text(spam_message, reply_to_message_id=mid)
            return
    
    ccc = None
    if len(message.text.split('chk ')) > 1 and message.text.split('chk ')[1].strip():
            ccc = message.text.split('chk ')[1].strip()
    elif message.reply_to_message:
            ccc = message.reply_to_message.text.strip()
        
    if not ccc:
        await message.reply('Please enter card details. ', reply_to_message_id=mid)
        return
    ccc = re.sub(r'[ /\\:]', '|', ccc)
    ff = re.findall(r'\b(\d{15}|\d{16})\|(\d{2}|\d{4})\|(\d{4}|\d{2})\|(\d{4}|\d{3})', ccc) or re.findall(r'\b(\d{15}|\d{16}) (\d{2})/(\d{4}|\d{2}) (\d{4}|\d{3})', ccc)
        
    if not ff:
        await message.reply('Invalid format, type it CORRECTLY! Format: XXXXXXXXXXXXXXXX|MM|YYYY|CVV', reply_to_message_id=mid)
        return
    f = ff[0]
    cc = f[0]
    if not luhn_verification(cc):
        await message.reply('Invalid card number (Luhn check failed).', reply_to_message_id=mid)
        return
    mm = f[1]
    yy = f[2]
    if len(yy) == 2:
        yy = '20' + yy
    cvv = f[3]
    cccc = cc+'|'+mm+'|'+yy+'|'+cvv
    is_ban = await is_bin_banned(cc[:6])
    if is_ban:
        return await message.reply(f'''
<b>[<a href="https://t.me/Instuff_bot">⌥</a>]</b> 𝐁𝐢𝐧 𝐒𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐒𝐲𝐬𝐭𝐞𝐦
━━━━━━━━━━━━
<b>[<a href="https://t.me/Instuff_bot">↯</a>]</b> 𝐌𝐞𝐬𝐬𝐚𝐠𝐞: <code>{is_ban}</code>
━━━━━━━━━━━━
<b>[<a href="https://t.me/Instuff_bot">⌤</a>]</b> 𝐃𝐞𝐯 𝐛𝐲: <code>@XxFakundoxX</code> 🍀
''', quote=True, disable_web_page_preview=True)
    x = await message.reply('Processing...', reply_to_message_id=mid)
    start_time = time.perf_counter()
    msg = await B3_Auth1(cc,mm,yy,cvv)
    brand , type, level, bank, country, emoji = await bin_data(cc[:6])
    rank = await get_user_rank(user_id)
    end_time = time.perf_counter()
    elapsed_time = f"{end_time - start_time:.2f}"
    if 'Nice! New payment method added' in msg or 'Payment method successfully added.' in msg:
        status = '𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅'
        msg = 'Approved'
    elif 'Duplicate card exists in the vault.' in msg:
        status = '𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅'
        msg = 'Approved - Duplicate'
    elif 'Card Issuer Declined CVV' in msg or 'Insufficient Funds' in msg or 'Invalid postal code and cvv' in msg  or 'CVV' in msg:
        status = '𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅'
    else:
        status = '𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌'
    text = f'''
<b>#Braintree_Auth 🔥 [/chk]
- - - - - - - - - - - - - - - - - - - - - - - -</b>
<b>[<a href="https://t.me/Instuff_bot">ϟ</a>]</b> 𝐂𝐚𝐫𝐝: <code>{cccc}</code>
<b>[<a href="https://t.me/Instuff_bot">ϟ</a>]</b> 𝐒𝐭𝐚𝐭𝐮𝐬: {status}
<b>[<a href="https://t.me/Instuff_bot">ϟ</a>]</b> 𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: {msg}
<b>- - - - - - - - - - - - - - - - - - - - - - - -</b>
<b>[<a href="https://t.me/Instuff_bot">ϟ</a>]</b> 𝐈𝐧𝐟𝐨: <b><code>{brand}</code> - <code>{type}</code> - <code>{level}</code></b>
<b>[<a href="https://t.me/Instuff_bot">ϟ</a>]</b> 𝐁𝐚𝐧𝐤: <code>{bank}</code>
<b>[<a href="https://t.me/Instuff_bot">ϟ</a>]</b> 𝐂𝐨𝐮𝐧𝐭𝐫𝐲: {country} - [<code>{emoji}</code>]
<b>- - - - - - - - - - - - - - - - - - - - - - - -</b>
<b>[<a href="https://t.me/Instuff_bot">⌥</a>]</b> 𝐓𝐢𝐦𝐞: <code>{elapsed_time}</code> 𝐒𝐞𝐜. || 𝐏𝐫𝐨𝐱𝐲: <b><code>Live ✅</code></b>
<b>[<a href="https://t.me/Instuff_bot">⎇</a>]</b> 𝐑𝐞𝐪 𝐁𝐲: <a href="tg://user?id={user_id}">{first_n}</a> <b>[{rank}]</b>
<b>- - - - - - - - - - - - - - - - - - - - - - - -</b>
<b>[<a href="https://t.me/Instuff_bot">⌤</a>]</b> 𝐃𝐞𝐯 𝐛𝐲: <code>@XxFakundoxX</code> 🍀
'''
    await x.edit(text, disable_web_page_preview=True)    

