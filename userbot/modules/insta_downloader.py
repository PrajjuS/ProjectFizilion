#Copyright @arshsisodiya
#https://github.com/arshsisodiya
#https://twitter.com/arshsisodiya

#Created by arshsisodiya for ProjectHelios

import asyncio
from asyncio.exceptions import TimeoutError
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from userbot import CMD_HELP, bot
from userbot.events import register

@register(outgoing=True, pattern=r"^\.insta(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    msg_link = await event.get_reply_message()
    query = event.pattern_match.group(1)

    if msg_link:
        query = msg_link.text
        await event.edit("`Fetching Data from instagram`")
    elif ".com" not in query:
        await event.edit("`Enter a valid link to download from`")

    elif "reel" in query:
        await event.edit("`Reel is downloading......`")
    elif "stories" in query:
        await event.edit("`Sorry but story downloading is not supported yet`")
    else:
        await event.edit("`fetching post from instagram...`")
    chat = "@allsaverbot"
    try:
        async with bot.conversation(chat) as conv:
            try:
                msg_start = await conv.send_message("/start")
                response = await conv.get_response()
                send_query = await conv.send_message(query)
                garbagetext = await conv.get_response()
                anothergarbagetext = await conv.get_response()
                video = await conv.get_response()
                """- don't spam notif -"""
                await bot.send_read_acknowledge(conv.chat_id)
            except YouBlockedUserError:
                await event.edit("`Unblock `@allsaverbot` and retry`")
                return
            await event.client.send_file(event.chat_id, video, caption=send_query.text)
            await event.client.delete_messages(
                conv.chat_id, [msg_start.id, response.id, send_query.id, video.id, garbagetext.id, anothergarbagetext.id]
            )
            await event.delete()
    except TimeoutError:
        return await event.edit("`Error: `@allsaverbot` is not responding or you are trying to downloading instagram stories")
CMD_HELP.update(
    {
        "insta": ".insta <instagram link>"
                "\nUsage: Reply to a instagram link or paste instagram link to "
                "download the file using `@allsaverbot`"
    }
)
