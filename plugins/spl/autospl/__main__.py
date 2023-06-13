""" auto spl """


import os

from pyrogram import enums

from userge import userge, Message, filters, config, get_collection
from ...ocr import ocr

IS_ENABLED = False
IS_ENABLED_FILTER = filters.create(lambda _, __, ___: IS_ENABLED)

USER_DATA = get_collection("CONFIGS")
CHANNEL = userge.getCLogger(__name__)


@userge.on_start
async def _init() -> None:
    global IS_ENABLED  # pylint: disable=global-statement
    data = await USER_DATA.find_one({'_id': 'AUTO_SPL'})
    if data:
        IS_ENABLED = data['on']


@userge.on_cmd("autospl", about={
    'header': "Auto Spl Response",
    'description': "enable or disable auto Spl response",
    'usage': "{tr}autospl"},
    allow_channels=False, allow_via_bot=False)
async def autofastly(msg: Message):
    """ Auto Spl Response """
    global IS_ENABLED  # pylint: disable=global-statement
    if ocr.OCR_SPACE_API_KEY is None:
        await msg.edit(
            "<code>Get the OCR API</code> ",
            disable_web_page_preview=True,
            parse_mode=enums.ParseMode.HTML, del_in=0)
        return

    IS_ENABLED = not IS_ENABLED
    await USER_DATA.update_one({'_id': 'AUTO_SPL'},
                               {"$set": {'on': IS_ENABLED}}, upsert=True)
    await msg.edit(
        "Auto Spl Response has been **{}** Successfully...".format(
            "Enabled" if IS_ENABLED else "Disabled"
        ),
        log=True, del_in=5
    )


@userge.on_filters(IS_ENABLED_FILTER & filters.group & filters.photo & filters.incoming
                   & filters.user([6069158574, 6124076947, 5816562737, 6090076323, 6201702225, 5843179980, 5912985290, 5824026395, 6013874987, 5607854181, 5986932374]),  # Bot ID
                   group=-1, allow_via_bot=False)
async def fastly_handler(msg: Message):
    img = await msg.download(config.Dynamic.DOWN_PATH)
    parse = await ocr.ocr_space_file(img)
    try:
        text = parse["ParsedResults"][0]["ParsedText"]
        if "@spl" in text.lower():
            text = text.split("\n")[1].replace("\n", "").replace("\r", "").replace(" ", "")
            if text:
                await msg.reply_text(text.capitalize())
                await CHANNEL.log(f'Auto Spl Responded in {msg.chat.title} [{msg.chat.id}]')
        os.remove(img)
    except Exception as e_x:  # pylint: disable=broad-except
        await CHANNEL.log(str(e_x))
        if os.path.exists(img):
            os.remove(img)
