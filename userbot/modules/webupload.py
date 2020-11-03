import asyncio
import time
from userbot import CMD_HELP
from userbot.events import register


@register(pattern="^.webupload ?(.+?|) (?:--)(anonfiles|transfer|filebin|anonymousfiles|megaupload|bayfiles|openload|file.io|vshare)")
async def _(event):
    if event.fwd_from:
        return
    await event.edit("work in progress 🛰")
    PROCESS_RUN_TIME = 100
    input_str = event.pattern_match.group(1)
    selected_transfer = event.pattern_match.group(2)
    if input_str:
        file_name = input_str
    else:
        reply = await event.get_reply_message()
        file_name = await bot.download_media(reply.media, Var.TEMP_DOWNLOAD_DIRECTORY)
    event.message.id
    CMD_WEB = {
        "anonfiles": "curl -F \"file=@{}\" https://anonfiles.com/api/upload",
        "transfer": "curl --upload-file \"{}\" https://transfer.sh/{os.path.basename(file_name)}",
        "anonymousfiles": "curl -F file=\"@{}\" https://api.anonymousfiles.io/",
        "megaupload": "curl -F file=\"@{}\" https://megaupload.is/api/upload",
        "bayfiles": "curl -F file=\"@{}\" https://bayfiles.com/api/upload",
        "openload": "curl -F file=\"@{}\" https://api.openload.cc/upload",
        "file.io": "curl -F file=\"@{}\" https://file.io",
        "vshare": "curl -F file=\"@{}\" https://api.vshare.is/upload"}
    try:
        selected_one = CMD_WEB[selected_transfer].format(file_name)
    except KeyError:
        await event.edit("Invalid selected Transfer")
    cmd = selected_one
    time.time() + PROCESS_RUN_TIME
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    await event.edit(f"{stdout.decode()}")
CMD_HELP.update({"webupload":
                 "`.webupload` (filename) `--anonfiles` | `transfer` | `anonymousfiles` | `megaupload` | `bayfiles` | `openload` | `file.io` | `vshare` "})
