# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
import os

from requests import exceptions, get, post

from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP, TEMP_DOWNLOAD_DIRECTORY
from userbot.events import register

BIN_URL = https://nekobin.com/"


@register(outgoing=True, pattern=r"^.paste(?: |$)([\s\S]*)")
async def paste(pstl):
    """ For .paste command, pastes the text directly to nekobin. """
    nekobin_final_url = ""
    match = pstl.pattern_match.group(1).strip()
    reply_id = pstl.reply_to_msg_id

    if not match and not reply_id:
        await pstl.edit("`Elon Musk said I cannot paste void.`")
        return

    if match:
        message = match
    elif reply_id:
        message = await pstl.get_reply_message()
        if message.media:
            downloaded_file_name = await pstl.client.download_media(
                message,
                TEMP_DOWNLOAD_DIRECTORY,
            )
            m_list = None
            with open(downloaded_file_name, "rb") as fd:
                m_list = fd.readlines()
            message = ""
            for m in m_list:
                message += m.decode("UTF-8")
            os.remove(downloaded_file_name)
        else:
            message = message.message

    await pstl.edit("`Pasting text . . .`")
    resp = post(BIN_URL + "documents", data=message.encode("utf-8"))

    if resp.status_code == 200:
        response = resp.json()
        key = response["key"]
        bin_final_url = BIN_URL + key

        if response["isUrl"]:
            reply_text = (
                "`Pasted successfully!`\n\n"
                f"[Shortened URL]({bin_final_url})\n\n"
                "`Original(non-shortened) URLs`\n"
                f"`•`[Nekobin URL]({BIN_URL}v/{key})\n"
                f"`•`[RAW]({BIN_URL}raw/{key})"
            )
        else:
            reply_text = ( 
                "`Pasted successfully!`\n\n" 
                f"`•`[Nekobin URL]({BIN_URL}v/{key})\n"
                f"`•`[RAW]({BIN_URL}raw/{key})"
            )
    else:
        reply_text = "`Failed to reach Nekobin`"

    await pstl.edit(reply_text)
    if BOTLOG:
        await pstl.client.send_message(
            BOTLOG_CHATID,
            f"Paste query was executed successfully",
        )


@register(outgoing=True, pattern="^.getpaste(?: |$)(.*)")
async def get_nekobin_content(neko_url):
    """ For .getpaste command, fetches the content of a nekobin URL. """
    textx = await neko_url.get_reply_message()
    message = neko_url.pattern_match.group(1)
    await neko_url.edit("`Getting nekobin content...`")

    if textx:
        message = str(textx.message)

    format_normal = f"{BIN_URL}"
    format_view = f"{BIN_URL}v/"

    if message.startswith(format_view):
        message = message[len(format_view) :]
    elif message.startswith(format_normal):
        message = message[len(format_normal) :]
    elif message.startswith("nekobin.com/"):
        message = message[len("nekobin.com/") :]
    else:
        await neko_url.edit("`Is that even a nekobin url?`")
        return

    resp = get(f"{BIN_URL}raw/{message}")

    try:
        resp.raise_for_status()
    except exceptions.HTTPError as HTTPErr:
        await neko_url.edit(
            "Request returned an unsuccessful status code.\n\n" + str(HTTPErr)
        )
        return
    except exceptions.Timeout as TimeoutErr:
        await neko_url.edit("Request timed out." + str(TimeoutErr))
        return
    except exceptions.TooManyRedirects as RedirectsErr:
        await neko_url.edit(
            "Request exceeded the configured number of maximum redirections."
            + str(RedirectsErr)
        )
        return

    reply_text = "`Fetched nekobin URL content successfully!`\n\n`Content:` " + resp.text

    await neko_url.edit(reply_text)
    if BOTLOG:
        await neko_url.client.send_message(
            BOTLOG_CHATID,
            "Get nekobin content query was executed successfully",
        )


CMD_HELP.update(
    {
        "paste": ".paste <text/reply>\ 
        \nUsage: Create a paste or a shortened url using [Nekobin](https://nekobin.com/)\
        \n\n.getpaste\ 
        \nUsage: Gets the content of a paste or shortened url from [Nekobin](https://nekobin.com/)"
