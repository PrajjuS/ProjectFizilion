# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
# Random RGB Sticklet by @PhycoNinja13b
# modified by @UniBorg
# Port From UniBorg to UserBot by @ElytrA8

import io
import os
import random
import textwrap

from PIL import Image, ImageDraw, ImageFont
from telethon.tl.types import InputMessagesFilterDocument
from userbot import CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern=r"^.stk(.*)")
async def sticklet(event):
    R = random.randint(0,256)
    G = random.randint(0,256)
    B = random.randint(0,256)

    # get the input text
    # the text on which we would like to do the magic on
    sticktext = event.pattern_match.group(1)

    # delete the userbot command,
    # i don't know why this is required
    await event.edit("Processing.....")

    # https://docs.python.org/3/library/textwrap.html#textwrap.wrap
    sticktext = textwrap.wrap(sticktext, width=10)
    # converts back the list to a string
    sticktext = '\n'.join(sticktext)
    
    image = Image.new("RGBA", (512, 512), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    fontsize = 230
    
    await event.edit("Wait Plox.....\nNeed some time")
    
    FONT_FILE = "/resources/Aerospace.ttf"

    font = ImageFont.truetype(FONT_FILE, size=fontsize)
    
    await event.edit("Processing...........Kek")
    
    while draw.multiline_textsize(sticktext, font=font) > (512, 512):
        fontsize -= 3
        font = ImageFont(FONT_FILE, size=fontsize)

    width, height = draw.multiline_textsize(sticktext, font=font)
    draw.multiline_text(((512-width)/2,(512-height)/2), sticktext, font=font, fill=(R, G, B))
    

    
    image_stream = io.BytesIO()
    image_stream.name = "@Fizilion.webp"
    image.save(image_stream, "WebP")
    image_stream.seek(0)
    
    await event.delete()
    # finally, reply the sticker
    await event.reply(file=image_stream)

    # cleanup
    try:
        os.remove(FONT_FILE)
    except:
        pass

async def get_font_file(client, channel_id):
    # first get the font messages
    font_file_message_s = await client.get_messages(
        entity=channel_id,
        filter=InputMessagesFilterDocument,
        # this might cause FLOOD WAIT,
        # if used too many times
        limit=None
    )
    

    # get a random font from the list of fonts
    # https://docs.python.org/3/library/random.html#random.choice
    font_file_message = random.choice(font_file_message_s)
    # download and return the file path
    return await client.download_media(font_file_message)

CMD_HELP.update({
        "sticklet":
        ".stk \
            \nUsage: Enhance ur sticker"
})
