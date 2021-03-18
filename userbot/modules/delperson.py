from asyncio import sleep
from random import choice, randint

from telethon.events import StopPropagation

from userbot import (BOTLOG, BOTLOG_CHATID, CMD_HELP, COUNT_MSG,
                     DELMSG, PM_AUTO_BAN, USERS)
from userbot.events import register

@register(incoming=True, disable_edited=True)
async def on_dm(dom):
    global COUNT_MSG
    global USERS
    global DELMSG
    if dom.message.mentioned and DELMSG:
        is_bot = False
        if (sender := await mention.get_sender()):
            is_bot = sender.bot
        if not is_bot and mention.sender_id not in USERS:
            USERS.update({mention.sender_id: 1})
        else:
            if not is_bot and sender:
                if USERS[mention.sender_id] % randint(2, 4) == 0:
                  USERS[mention.sender_id] = USERS[mention.sender_id] + 1
        COUNT_MSG = COUNT_MSG + 1


@register(incoming=True, disable_errors=True)
async def delmsg_on_pm(sender):
    global DELMSG
    global USERS
    global COUNT_MSG
    if (
        sender.is_private
        and sender.sender_id != 777000
        and not (await sender.get_sender()).bot
    ):
        if PM_AUTO_BAN:
            try:
                from userbot.modules.sql_helper.pm_permit_sql import \
                    is_approved
                apprv = is_approved(sender.sender_id)
            except AttributeError:
                apprv = True
        else:
            apprv = True
        if apprv and DELMSG:
            if sender.sender_id not in USERS:
                USERS.update({sender.sender_id: 1})
            else:
                if USERS[sender.sender_id] % randint(2, 4) == 0:
                  USERS[sender.sender_id] = USERS[sender.sender_id] + 1
            COUNT_MSG = COUNT_MSG + 1
            
            
@register(outgoing=True, pattern=r"^\.dm(?: |$)(.*)")
async def set_delmsg(dm_e):
    dm_e.text
    string = dm_e.pattern_match.group(1)
    global DELMSG
    msg = await dm_e.edit("Turning on DELMSG")
    await sleep(2)
    await msg.delete()
    if BOTLOG:
        await dm_e.client.send_message(BOTLOG_CHATID, "#DELMSG\nYou turned on DELMSG!")
    DELMSG = True
    raise StopPropagation


@register(outgoing=True)
async def type_del_is_not_true(notdel):
    global DELMSG
    global COUNT_MSG
    global USERS
    if DELMSG:
        DELMSG = False
        msg = await notdel.respond("Delmsg turned off.")
        await sleep(2)
        await msg.delete()
        if BOTLOG:
            await notdel.client.send_message(
                BOTLOG_CHATID,
                "You've recieved "
                + str(COUNT_MSG)
                + " messages from "
                + str(len(USERS))
                + " chats while you were away",
            )
            for i in USERS:
                name = await notdel.client.get_entity(i)
                name0 = str(name.first_name)
                await notdel.client.send_message(
                    BOTLOG_CHATID,
                    "["
                    + name0
                    + "](tg://user?id="
                    + str(i)
                    + ")"
                    + " sent you "
                    + "`"
                    + str(USERS[i])
                    + " messages`",
                )
        COUNT_MSG = 0
        USERS = {}


CMD_HELP.update(
    {
        "dm": ">`.dm`"
        "\nUsage: Delete Msg history turns on. "
    }
)
