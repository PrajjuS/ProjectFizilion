import asyncio
from collections import deque
from userbot.events import register
from userbot import CMD_HELP


@register(outgoing=True, pattern="^.earth(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    deq = deque(list("🌏🌍🌎🌎🌍🌏🌍🌎"))
    for _ in range(48):
        await asyncio.sleep(0.1)
        await event.edit("".join(deq))
        deq.rotate(1)
CMD_HELP.update({
    "earth":
    "earth live emoji."
})
