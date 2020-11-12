# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
# courtesy Yasir siddiqui

import time
from userbot import CMD_HELP
from userbot.events import register

@register(outgoing=True, pattern=r"^.sd(?: |$)")
async def selfdestruct(destroy):
    """ For .sd command, make seflf-destructable messages. """
    if not destroy.text[0].isalpha() and destroy.text[0] not in ("/", "#", "@", "!"):
        message = destroy.text
        counter = int(message[4:6])
        text = str(destroy.text[6:])
        text = (
            text
            + "\n\n`This message shall be self-destructed in "
            + str(counter)
            + " seconds`"
        )
        await destroy.delete()
        smsg = await destroy.client.send_message(destroy.chat_id, text)
        time.sleep(counter)
        await smsg.delete()

CMD_HELP.update(
    {
        "selfdestruct": ".sd <time in seconds> <text>
    }) 
