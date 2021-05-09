from asyncio
from userbot.events import register

T_R_D = [
    "Prajwal",
    "Vinaya",
    "Sharan",
    "Srinidhi",
]

@register(outgoing=True, pattern="^.trd$")
async def truthrdare(trd):
    """Truth or Dare"""
    await trd.edit(choice(T_R_D))
