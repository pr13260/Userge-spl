""" auto buy spl """

import os

from pyrogram import enums
from asyncio import sleep
from userge import userge, Message, filters, config, get_collection


IS_ENABLED = False
IS_ENABLED_FILTER = filters.create(lambda _, __, ___: IS_ENABLED)

USER_DATA = get_collection("CONFIGS")
CHANNEL = userge.getCLogger(__name__)


@userge.on_start
async def _init() -> None:
    global IS_ENABLED  # pylint: disable=global-statement
    data = await USER_DATA.find_one({'_id': 'AUTO_BUY_SPL'})
    if data:
        IS_ENABLED = data['on']


@userge.on_cmd("autobuyspl", about={
    'header': "Auto Buy Spl",
    'description': "enable or disable auto buy Spl response",
    'usage': "{tr}autospl"},
    allow_channels=False, allow_via_bot=False)
async def autobuyspl(msg: Message):
    """ Auto Spl Response """
    global IS_ENABLED  # pylint: disable=global-statement
    IS_ENABLED = not IS_ENABLED
    await USER_DATA.update_one({'_id': 'AUTO_BUY_SPL'},
                               {"$set": {'on': IS_ENABLED}}, upsert=True)
    await msg.edit(
        "Auto Buy Spl Response has been **{}** Successfully...".format(
            "Enabled" if IS_ENABLED else "Disabled"
        ),
        log=True, del_in=5
    )

async def normalize_text(text):
    mapping = {
        'ᴀ': 'a',
        'ʙ': 'b',
        'ᴄ': 'c',
        'ᴅ': 'd',
        'ᴇ': 'e',
        'ꜰ': 'f',
        'ɢ': 'g',
        'ʜ': 'h',
        'ɪ': 'i',
        'ᴊ': 'j',
        'ᴋ': 'k',
        'ʟ': 'l',
        'ᴍ': 'm',
        'ɴ': 'n',
        'ᴏ': 'o',
        'ᴘ': 'p',
        'ǫ': 'q',
        'ʀ': 'r',
        'ꜱ': 's',
        'ᴛ': 't',
        'ᴜ': 'u',
        'ᴠ': 'v',
        'ᴡ': 'w',
        'x': 'x',
        'ʏ': 'y',
        'ᴢ': 'z'
    }
    normalized_text = ''
    for char in text:
        normalized_char = mapping.get(char, char)
        normalized_text += normalized_char.lower()
    return normalized_text

@userge.on_filters(IS_ENABLED_FILTER & filters.group & filters.photo & filters.incoming
                   & filters.user([6069158574, 6124076947, 5816562737, 6090076323, 6201702225, 5843179980, 5912985290, 5824026395, 6013874987, 5607854181, 5986932374]),  # Bot ID
                   group=-1, allow_via_bot=False)
async def fastly_handler(msg: Message):
 if "🌴 New character is available for purchase" in msg.caption:
  if "Example : /purchase [char_name]" in msg.caption:
    tetr=await msg.click(0)
    textr= await normalize_text(textr)
    try:
        text = textr.message.split("{")[0].strip()
    except:
        text = extr.message
    parsed = "/purchase "+text
    try:
        text = parsed
        text = text.replace("\n", "").replace("\r", "").replace("{🤵🏻‍♂️}", "")
        if text:
                await sleep(1)
                y=await msg.reply_text(text)
                await sleep(1)
                await y.delete()
                await CHANNEL.log(f'Auto Buy Spl Responded in {msg.chat.title} [{msg.chat.id}] \nIt bought {text}')
    except Exception as e_x:  # pylint: disable=broad-except
        await CHANNEL.log(str(e_x))
