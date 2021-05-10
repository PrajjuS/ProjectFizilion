# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot help command """

from userbot import CMD_HELP, TIMEOUT
from userbot.events import register
from asyncio import sleep
@register(outgoing=True, pattern=r"^\.help(?: |$)(.*)")
async def help(event):
    """ For .help command,"""
    args = event.pattern_match.group(1).lower()
    # Prevent Channel Bug to get any information and command from all modules
    if event.is_channel and not event.is_group:
        await event.edit("`Help command isn't permitted on channels`")
        return
    
    if TIMEOUT:
        if args:
            if args in CMD_HELP:
                msg=await event.edit(str(CMD_HELP[args]))
                await sleep(10)
                await msg.delete()
                
            else:
                msg=await event.edit("Please specify a valid module name.")
                await sleep(10)
                await msg.delete()
                           
        else:
            final = "**List of all loaded module(s)**\n\
                 \nSpecify which module do you want help for! \
                 \n**Usage:** `.help` <module name>\n\n"
            temp = "".join(str(i) + " " for i in CMD_HELP)
            temp = sorted(temp.split())
            for i in temp:
                final += "`" + str(i)
                final += "`\t\t\t•\t\t\t"
            msg=await event.edit(f"{final[:-5]}")
            await sleep(10)
            await msg.delete()   
    
    
    if not TIMEOUT:
        if args:
            if args in CMD_HELP:
                msg=await event.edit(str(CMD_HELP[args]))
                
            else:
                msg=await event.edit("Please specify a valid module name.")
                           
        else:
            final = "**List of all loaded module(s)**\n\
                 \nSpecify which module do you want help for! \
                 \n**Usage:** `.help` <module name>\n\n"
            temp = "".join(str(i) + " " for i in CMD_HELP)
            temp = sorted(temp.split())
            for i in temp:
                final += "`" + str(i)
                final += "`\t\t\t•\t\t\t"
            msg=await event.edit(f"{final[:-5]}")
  
