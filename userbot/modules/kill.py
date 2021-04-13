#Ported from userge by @PrajjuS
import asyncio
from asyncio import sleep
from userbot.events import register
from userbot import CMD_HELP

@register(outgoing=True, pattern="^.kill$")
async def kill_func(message):
    animation_chars = [
        "killing...",
        "Ｆｉｉｉｉｉｒｅ",
        "(　･ิω･ิ)︻デ═一-->",
        "------>_____________",
        "--------->___⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠_______",
        "-------------->_____",
        "------------------->",
        "------>;(^。^)ノ",
        "(￣ー￣) DED",
        "<b>Target killed successfully (´°̥̥̥̥̥̥̥̥ω°̥̥̥̥̥̥̥̥｀)</b>",
    ]
    for i in range(10):
        await sleep(0.6)
        await message.edit(animation_chars[i % 10], parse_mode="html")

CMD_HELP.update({
    "kill":
    "'.kill'"
    "\nUsage: Kill Meme"
    })
