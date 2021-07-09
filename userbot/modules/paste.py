from requests import post
from telethon.tl.types import MessageMediaWebPage

from userbot import CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern=r"^\.paste(?:\s|$)([\s\S]*)")
async def paste(event):
    """Pastes given text to Nekobin"""
    await event.edit("**Pasting to Nekobin...**")

    if event.is_reply:
        reply = await event.get_reply_message()
        if reply.media and not isinstance(reply.media, MessageMediaWebPage):
            return await event.edit("**Reply to some text!**")
        message = reply.message

    elif event.pattern_match.group(1).strip():
        message = event.pattern_match.group(1).strip()

    else:
        return await event.edit("**Read** `.help paste`**.**")

    response = post("https://nekobin.com/api/documents", json={"content": message}).json()

    if response["msg"] == "Successfully created paste":
        await event.edit(
            f"**Pasted successfully:** [Nekobin](https://nekobin.com/raw/{response['paste_id']})\n"
        )
    else:
        await event.edit("**Nekobin seems to be down.**")


CMD_HELP.update(
    {"paste": ">`.paste` <text/reply>" "\nUsage: Pastes given text to Nekobin."}
)
