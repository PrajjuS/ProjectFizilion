import asyncio
from userbot.events import register
from userbot import CMD_HELP

@register(outgoing=True, pattern="^.hack$")
async def _(event):
    if event.fwd_from:
    return
    animation_interval = 3
    animation_ttl = range(0, 12)
    input_str = event.pattern_match.group(1)
    if input_str == "hack":
    await event.edit(input_str)
    animation_chars = [
        "```Connecting To Private Server \\```",
        "```Connecting To Private Server |```",
        "```Connecting To Private Server /```",
        "```Connecting To Private Server \\```",
        "```Connection Established ```",
        "```Target Selected```",
        "```Backdoor Found In Target```",
        "```Trying To Hack```",
        "```Hacking... 0%\n▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒```",
        "```Hacking... 4%\n█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒```",
        "```Hacking... 8%\n██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒```",
        "```Hacking... 20%\n█████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒```",
        "```Hacking... 36%\n█████████▒▒▒▒▒▒▒▒▒▒▒▒▒```",
        "```Hacking... 52%\n█████████████▒▒▒▒▒▒▒▒▒```",
        "```Hacking... 70%\n█████████████████▒▒▒▒▒```",
        "```Hacking... 88%\n█████████████████████▒```",
        "```Hacking... 100%\n███████████████████████```",
        "```Preparing Data... 1%\n▒██████████████████████```",
        "```Preparing Data... 14%\n████▒██████████████████```",
        "```Preparing Data... 30%\n████████▒██████████████```",
        "```Preparing Data... 55%\n████████████▒██████████```",
        "```Preparing Data... 72%\n████████████████▒██████```",
        "```Preparing Data... 88%\n████████████████████▒██```",
        "```Prepared Data... 100%\n███████████████████████```",
        "```Uploading Data to Server... 12%\n███▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒```",
        "```Uploading Data to Server... 44%\n█████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒```",
        "```Uploading Data to Server... 68%\n███████████████▒▒▒▒▒▒▒▒```",
        "```Uploading Data to Server... 89%\n████████████████████▒▒▒```",
        "```Uploaded Data to Server... 100%\n███████████████████████```",
        "**User Data Upload Completed:** Target's User Data Stored "
        "at `downloads/victim/telegram-authuser.data.sql`",
        "**Targeted Account Hacked**\n\n```Pay 69$ To```This User``` /n ```To Remove This Hack```"
    ]
            for i in animation_ttl:
            await asyncio.sleep(animation_interval)
            await event.edit(animation_chars[i % 12])

CMD_HELP.update({
    "hack":
    ".hack :- hacking Animation"
})
