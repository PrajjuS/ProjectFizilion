# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module for executing code and terminal commands from Telegram. """

import asyncio
import re

import os
import io
import sys
import traceback
from os import remove
from sys import executable

from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP, USER_TERM_ALIAS
from userbot.events import register


@register(outgoing=True, pattern=r"^\.eval(?: |$|\n)(.*)")
async def evaluate(query):
    """ For .eval command, evaluates the given Python expression. """
    if query.is_channel and not query.is_group:
        return await query.edit("`Eval isn't permitted on channels`")

    if query.pattern_match.group(1):
        expression = query.pattern_match.group(1)
    else:
        return await query.edit("``` Give an expression to evaluate. ```")

    for i in ("userbot.session", "env"):
        if expression.find(i) != -1:
            return await query.edit("`That's a dangerous operation! Not Permitted!`")

    try:
        evaluation = str(eval(expression))
        if evaluation:
            if isinstance(evaluation, str):
                if len(evaluation) >= 4096:
                    with open("output.txt", "w+") as file:
                        file.write(evaluation)
                    await query.client.send_file(
                        query.chat_id,
                        "output.txt",
                        reply_to=query.id,
                        caption="`Output too large, sending as file`",
                    )
                    remove("output.txt")
                    return
                await query.edit(
                    "**Query: **\n`"
                    f"{expression}"
                    "`\n**Result: **\n`"
                    f"{evaluation}"
                    "`"
                )
        else:
            await query.edit(
                "**Query: **\n`"
                f"{expression}"
                "`\n**Result: **\n`No Result Returned/False`"
            )
    except Exception as err:
        await query.edit(
            "**Query: **\n`" f"{expression}" "`\n**Exception: **\n" f"`{err}`"
        )

    if BOTLOG:
        await query.client.send_message(
            BOTLOG_CHATID, f"Eval query {expression} was executed successfully."
        )


@register(outgoing=True, pattern=r"^\.exec(?: |$|\n)([\s\S]*)")
async def run(run_q):
    """ For .exec command, which executes the dynamically created program """
    code = run_q.pattern_match.group(1)

    if run_q.is_channel and not run_q.is_group:
        return await run_q.edit("`Exec isn't permitted on channels!`")

    if not code:
        return await run_q.edit(
            "``` At least a variable is required to"
            "execute. Use .help exec for an example.```"
        )

    for i in ("userbot.session", "env"):
        if code.find(i) != -1:
            return await run_q.edit("`That's a dangerous operation! Not Permitted!`")

    if len(code.splitlines()) <= 5:
        codepre = code
    else:
        clines = code.splitlines()
        codepre = (
            clines[0] +
            "\n" +
            clines[1] +
            "\n" +
            clines[2] +
            "\n" +
            clines[3] +
            "...")

    command = "".join(f"\n {l}" for l in code.split("\n.strip()"))
    process = await asyncio.create_subprocess_exec(
        executable,
        "-c",
        command.strip(),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    result = str(stdout.decode().strip()) + str(stderr.decode().strip())

    if result:
        if len(result) > 4096:
            with open("output.txt", "w+") as file:
                file.write(result)
            await run_q.client.send_file(
                run_q.chat_id,
                "output.txt",
                reply_to=run_q.id,
                caption="`Output too large, sending as file`",
            )
            remove("output.txt")
            return
        await run_q.edit(
            "**Query: **\n`" f"{codepre}" "`\n**Result: **\n`" f"{result}" "`"
        )
    else:
        await run_q.edit(
            "**Query: **\n`" f"{codepre}" "`\n**Result: **\n`No result returned/False`"
        )

    if BOTLOG:
        await run_q.client.send_message(
            BOTLOG_CHATID, "Exec query " + codepre + " was executed successfully."
        )


@register(outgoing=True, pattern="^.shell(?: |$)(.*)")
async def terminal_runner(term):
    """ For .shell command, runs bash commands and scripts on your server. """
    curruser = USER_TERM_ALIAS
    command = term.pattern_match.group(1)
    try:
        from os import geteuid

        uid = geteuid()
    except ImportError:
        uid = "This ain't it chief!"

    if term.is_channel and not term.is_group:
        return await term.edit("`Shell commands aren't permitted on channels!`")

    for i in ("userbot.session", "env"):
        if command.find(i) != -1:
            return await term.edit("`That's a dangerous operation! Not Permitted!`")

    if not re.search(r"echo[ \-\w]*\$\w+", command) is None:
        return await term.edit("`That's a dangerous operation! Not Permitted!`")

    process = await asyncio.create_subprocess_shell(
        command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    result = str(stdout.decode().strip()) + str(stderr.decode().strip())

    if len(result) > 4096:
        with open("output.txt", "w+") as output:
            output.write(result)
        await term.client.send_file(
            term.chat_id,
            "output.txt",
            reply_to=term.id,
            caption="`Output too large, sending as file`",
        )
        remove("output.txt")
        return

    if uid == 0:
        await term.edit("`" f"{curruser}:~# {command}" f"\n{result}" "`")
    else:
        await term.edit("`" f"{curruser}:~$ {command}" f"\n{result}" "`")

    if BOTLOG:
        await term.client.send_message(
            BOTLOG_CHATID, "Shell command " + command + " was executed sucessfully.",
        )
        
@register(outgoing=True, pattern="^.exe(?: |$)(.*)")        
async def eval(event):
    await event.reply("Processing ...")
    cmd = event.text.split(" ", maxsplit=1)[1]
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, event)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"
    final_output = "**EVAL**: `{}` \n\n **OUTPUT**: \n`{}` \n".format(cmd, evaluation)
    if len(final_output) > 4095:
        with io.BytesIO(str.encode(final_output)) as out_file:
            out_file.name = "eval.text"
            await event.client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=cmd,
            )
            await event.delete()
    else:
        await event.reply(final_output)


async def aexec(code, event):
    exec(f"async def __aexec(event): " + "".join(f"\n {l}" for l in code.split("\n")))
    return await locals()["__aexec"](event)


CMD_HELP.update({"eval": ">`.eval 2 + 3`"
                 "\nUsage: Evalute mini-expressions.",
                 "exec": ">`.exec print('hello')`"
                 "\nUsage: Execute small python scripts.",
                 "shell": ">`.shell <cmd>`"
                 "\nUsage: Run bash commands and scripts on your server.",
                 })
