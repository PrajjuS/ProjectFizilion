
"""
✘ Commands Available -

• `{i}compress <reply to video>`
    optional `crf` and `stream`
    Example : `{i}compress 27 | stream` or `{i}compress 28`
    Encode the replied video according to CRF value.
    Less CRF == High Quality, More Size
    More CRF == Low Quality, Less Size
    CRF Range = 20-51
    Default = 27

"""

import asyncio
import os
import re
import time
from datetime import datetime as dt

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from telethon.errors.rpcerrorlist import MessageNotModifiedError
from telethon.tl.types import DocumentAttributeVideo

from userbot import CMD_HELP, LOGS, TEMP_DOWNLOAD_DIRECTORY
from userbot.events import register
from userbot.utils import humanbytes, progress, run_cmd
from userbot.utils.FastTelethon import download_file, upload_file




@register(pattern=r"\.encode(?: |$)(.*)", outgoing=True)
async def _(e):
        crf = e.pattern_match.group(1)
        if not crf:
            crf = 27
        #to_stream = e.pattern_match.group(2)
        media = await e.get_reply_message()
        try:
            media = replied.media
            if hasattr(media, "document"):
                file = media.document
                mime_type = file.mime_type
                filename = replied.file.name
                if not filename:
                    if "audio" in mime_type:
                        filename = (
                            "audio_" + datetime.now().isoformat("_", "seconds") + ".ogg"
                        )
                    elif "video" in mime_type:
                        filename = (
                            "video_" + datetime.now().isoformat("_", "seconds") + ".mp4"
                        )
                outdir = TEMP_DOWNLOAD_DIRECTORY + filename
                c_time = time.time()
                start_time = datetime.now()
                with open(outdir, "wb") as f:
                    result = await download_file(
                        client=e.client,
                        location=file,
                        out=f,
                        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                            progress(
                                d,
                                t,
                                e,
                                c_time,
                                "Telegram - Download",
                                input_str,
                            )
                        ),
                    )
            else:
                start_time = datetime.now()
                result = await e.client.download_media(
                    media, TEMP_DOWNLOAD_DIRECTORY
                )
            dl_time = (datetime.now() - start_time).seconds
        except Exception as e:  # pylint:disable=C0103,W0703
            await e.edit(str(e))
    
            o_size = os.path.getsize(file.name)
            d_time = time.time()
            diff = time_formatter((d_time - c_time) * 1000)
            file_name = (file.name).split("/")[-1]
            out = file_name.replace(file_name.split(".")[-1], " compressed.mkv")
            await e.edit(
                f"`Downloaded {file.name} of {humanbytes(o_size)} in {diff}.\nNow Compressing...`"
            )
            x, y = await run_cmd(
                f'mediainfo --fullscan """{file.name}""" | grep "Frame count"'
            )
            total_frames = x.split(":")[1].split("\n")[0]
            progress = "progress.txt"
            with open(progress, "w") as fk:
                pass
            proce = await asyncio.create_subprocess_shell(
                f'ffmpeg -hide_banner -loglevel quiet -progress {progress} -i """{file.name}""" -preset ultrafast -vcodec libx265 -crf {crf} """{out}""" -y',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            while proce.returncode != 0:
                await asyncio.sleep(3)
                with open(progress, "r+") as fil:
                    text = fil.read()
                    frames = re.findall("frame=(\\d+)", text)
                    size = re.findall("total_size=(\\d+)", text)

                    if len(frames):
                        elapse = int(frames[-1])
                    if len(size):
                        size = int(size[-1])
                        per = elapse * 100 / int(total_frames)
                        time_diff = time.time() - int(d_time)
                        speed = round(elapse / time_diff, 2)
                        eta = time_formatter(
                            ((int(total_frames) - elapse) / speed) * 1000
                        )
                        text = f"`Compressing {file_name} at {crf} CRF.\n`"
                        progress_str = "`[{0}{1}] {2}%\n\n`".format(
                            "".join(["●" for i in range(math.floor(per / 5))]),
                            "".join(["" for i in range(20 - math.floor(per / 5))]),
                            round(per, 2),
                        )
                        e_size = humanbytes(size)
                        try:
                            await e.edit(
                                text
                                + progress_str
                                + "`"
                                + e_size
                                + "`"
                                + "\n\n`"
                                + eta
                                + "`"
                            )
                        except MessageNotModifiedError:
                            pass
            os.remove(file.name)
            c_size = os.path.getsize(out)
            f_time = time.time()
            difff = time_formatter((f_time - d_time) * 1000)
            await e.edit(
                f"`Compressed {humanbytes(o_size)} to {humanbytes(c_size)} in {difff}\nTrying to Upload...`"
            )
            differ = 100 - ((c_size / o_size) * 100)
            caption = f"**Original Size: **`{humanbytes(o_size)}`\n"
            caption += f"**Compressed Size: **`{humanbytes(c_size)}`\n"
            caption += f"**Compression Ratio: **`{differ:.2f}%`\n"
            caption += f"\n**Time Taken To Compress: **`{difff}`"
            #mmmm = await uploader(
            #    out,
            #    out,
            #    f_time,
            #    e,
            #    "Uploading " + out + "...",
            #)
            with open(out, "rb") as f:
                result = await upload_file(
                    client=e.client,
                    file=f,
                    name=file_name,
                    progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                        progress(d, t, e, f_time, "Telegram - Upload", out)
                    ),
                )
            if to_stream and "| stream" in to_stream:
                metadata = extractMetadata(createParser(out))
                duration = metadata.get("duration").seconds
                hi, _ = await run_cmd(f'mediainfo "{out}" | grep "Height"')
                wi, _ = await run_cmd(f'mediainfo "{out}" | grep "Width"')
                height = int(hi.split(":")[1].split()[0])
                width = int(wi.split(":")[1].split()[0])
                attributes = [
                    DocumentAttributeVideo(
                        duration=duration, w=width, h=height, supports_streaming=True
                    )
                ]
                await e.client.send_file(
                    e.chat_id,
                    result,
                   
                    caption=caption,
                    attributes=attributes,
                    force_document=False,
                    reply_to=e.reply_to_msg_id,
                )
            else:
                await e.client.send_file(
                    e.chat_id,
                    result,
                    
                    caption=caption,
                    force_document=True,
                    reply_to=e.reply_to_msg_id,
                )
            await e.delete()
            os.remove(out)
#        else:
#            await e.edit("`Reply To Video File Only`")
#    else:
#        await e.edit("`Reply To Video File Only`")
