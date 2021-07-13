# Copyright (C) 2020 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#

import io
import os
import os.path
import time
from os.path import exists, isdir
from pathlib import Path

from userbot import CMD_HELP
from userbot.events import register
from userbot.utils import humanbytes as hb

MAX_MESSAGE_SIZE_LIMIT = 4095


@register(outgoing=True, pattern=r"^\.ls ?(.*)")
async def lst(event):
    if event.fwd_from:
        return
    cat = event.pattern_match.group(1)
    if cat:
        path = cat
    else:
        path = os.getcwd()
    if not exists(path):
        await event.edit(
            f"There is no such directory or file with the name `{cat}` check again!"
        )
        return
    if isdir(path):
        if cat:
            msg = "Folders and Files in `{}` :\n\n".format(path)
            lists = os.listdir(path)
        else:
            msg = "Folders and Files in Current Directory :\n\n"
            lists = os.listdir(path)
        files = ""
        folders = ""
        for contents in sorted(lists):
            catpath = path + "/" + contents
            if not isdir(catpath):
                size = os.stat(catpath).st_size
                if contents.endswith((".mp3", ".flac", ".wav", ".m4a")):
                    files += "🎵 " + f"`{contents}`\n"
                if contents.endswith((".opus")):
                    files += "🎙 " + f"`{contents}`\n"
                elif contents.endswith(
                    (".mkv", ".mp4", ".webm", ".avi", ".mov", ".flv")
                ):
                    files += "🎞 " + f"`{contents}`\n"
                elif contents.endswith(
                    (".zip", ".tar", ".tar.gz", ".rar", ".7z", ".xz")
                ):
                    files += "🗜 " + f"`{contents}`\n"
                elif contents.endswith(
                    (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".ico", ". webp")
                ):
                    files += "🖼 " + f"`{contents}`\n"
                elif contents.endswith((".exe", ".deb")):
                    files += "⚙️ " + f"`{contents}`\n"
                elif contents.endswith((".iso", ".img")):
                    files += "💿 " + f"`{contents}`\n"
                elif contents.endswith((".apk", ".xapk")):
                    files += "📱 " + f"`{contents}`\n"
                elif contents.endswith((".py")):
                    files += "🐍 " + f"`{contents}`\n"
                else:
                    files += "📄 " + f"`{contents}`\n"
            else:
                folders += f"📁 `{contents}`\n"
        if files or folders:
            msg = msg + folders + files
        else:
            msg = msg + "__empty path__"
    else:
        size = os.stat(path).st_size
        msg = "The details of given file :\n\n"
        if path.endswith((".mp3", ".flac", ".wav", ".m4a")):
            mode = "🎵 "
        if path.endswith((".opus")):
            mode = "🎙 "
        elif path.endswith((".mkv", ".mp4", ".webm", ".avi", ".mov", ".flv")):
            mode = "🎞 "
        elif path.endswith((".zip", ".tar", ".tar.gz", ".rar", ".7z", ".xz")):
            mode = "🗜 "
        elif path.endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp", ".ico", ". webp")):
            mode = "🖼 "
        elif path.endswith((".exe", ".deb")):
            mode = "⚙️ "
        elif path.endswith((".iso", ".img")):
            mode = "💿 "
        elif path.endswith((".apk", ".xapk")):
            mode = "📱 "
        elif path.endswith((".py")):
            mode = "🐍 "
        else:
            mode = "📄 "
        time.ctime(os.path.getctime(path))
        time2 = time.ctime(os.path.getmtime(path))
        time3 = time.ctime(os.path.getatime(path))
        msg += f"**Location :** `{path}`\n"
        msg += f"**Icon :** `{mode}`\n"
        msg += f"**Size :** `{hb(size)}`\n"
        msg += f"**Last Modified Time:** `{time2}`\n"
        msg += f"**Last Accessed Time:** `{time3}`"

    if len(msg) > MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(msg)) as out_file:
            out_file.name = "ls.txt"
            await event.client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=path,
            )
            await event.delete()
    else:
        await event.edit(msg)
@register(outgoing=True, pattern=r"^\.la ?(.*)")
async def lsta(e):
    path = Path(e.pattern_match.group(1))
    if not path:
        path = Path(".")
    else:
        if not os.path.isdir(path):
            return await e.edit("`Incorrect Directory.`")
        if not os.listdir(path):
            return await e.edit("`This Directory is Empty.`")
    files = path.iterdir()
    pyfiles = []
    jsons = []
    vdos = []
    audios = []
    pics = []
    others = []
    otherfiles = []
    folders = []
    text = []
    apk = []
    exe = []
    zip_ = []
    book = []
    for file in sorted(files):
        if os.path.isdir(file):
            folders.append("📂 " + str(file))
        elif str(file).endswith(".py"):
            pyfiles.append("🐍 " + str(file))
        elif str(file).endswith(".json"):
            jsons.append("🔮 " + str(file))
        elif str(file).endswith((".mkv", ".mp4", ".avi", ".gif")):
            vdos.append("🎥 " + str(file))
        elif str(file).endswith((".mp3", ".ogg", ".m4a")):
            audios.append("🔊 " + str(file))
        elif str(file).endswith((".jpg", ".jpeg", ".png", ".webp")):
            pics.append("🖼 " + str(file))
        elif str(file).endswith((".txt", ".text", ".log")):
            text.append("📄 " + str(file))
        elif str(file).endswith((".apk", ".xapk")):
            apk.append("📲 " + str(file))
        elif str(file).endswith(".exe"):
            exe.append("⚙ " + str(file))
        elif str(file).endswith((".zip", ".rar")):
            zip_.append("🗜 " + str(file))
        elif str(file).endswith((".pdf", ".epub")):
            book.append("📗 " + str(file))
        elif "." in str(file)[1:]:
            others.append("🏷 " + str(file))
        else:
            otherfiles.append("📒 " + str(file))
    omk = [
        *sorted(folders),
        *sorted(pyfiles),
        *sorted(jsons),
        *sorted(zip_),
        *sorted(vdos),
        *sorted(pics),
        *sorted(audios),
        *sorted(apk),
        *sorted(exe),
        *sorted(book),
        *sorted(text),
        *sorted(others),
        *sorted(otherfiles),
    ]
    text = ""
    fls, fos = 0, 0
    flc, foc = 0, 0
    for i in omk:
        emoji = i.split()[0]
        name = i.split(maxsplit=1)[1]
        nam = name.split("/")[-1]
        if os.path.isdir(name):
            size = 0
            for path, dirs, files in os.walk(name):
                for f in files:
                    fp = os.path.join(path, f)
                    size += os.path.getsize(fp)
            if hb(size):
                text += emoji + f" `{nam}`" + "  `" + hb(size) + "`\n"
                fos += size
            else:
                text += emoji + f" `{nam}`" + "\n"
            foc += 1
        else:
            if hb(int(os.path.getsize(name))):
                text += (
                    emoji + f" `{nam}`" + "  `" + hb(int(os.path.getsize(name))) + "`\n"
                )
                fls += int(os.path.getsize(name))
            else:
                text += emoji + f" `{nam}`" + "\n"
            flc += 1
    tfos, tfls, ttol = hb(fos), hb(fls), hb(fos + fls)
    if not hb(fos):
        tfos = "0 B"
    if not hb(fls):
        tfls = "0 B"
    if not hb(fos + fls):
        ttol = "0 B"
    text += f"\n\n`Folders` :  `{foc}` :   `{tfos}`\n`Files` :       `{flc}` :   `{tfls}`\n`Total` :       `{flc+foc}` :   `{ttol}`"
    if len(text) > MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(text)) as out_file:
            out_file.name = "ls.txt"
            await e.client.send_file(
                e.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=path,
            )
            await e.delete()
    else:
        await e.edit(text)


CMD_HELP.update(
    {
        "file": ".ls <directory>"
        "\nUsage: Get information about files in Userbot's Storage"
                
    }
)
