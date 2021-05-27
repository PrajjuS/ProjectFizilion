from telethon import events
from userbot.utils import admin_cmd

@register(outgoing=True, pattern="^.all (?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    input_str = event.pattern_match.group(1)

    if not input_str:
     if event.fwd_from:
         return
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    mentions = "`Tagged all`"
    chat = await event.get_input_chat()
    async for x in borg.iter_participants(chat, 100):
        mentions += f"[\u2063](tg://user?id={x.id})"
    await reply_to_id.reply(mentions)
    await event.delete()
    
    if input_str:
      mentions = input_str 
      chat = await event.get_input_chat()
      async for x in borg.iter_participants(chat, 100):
          mentions += f"[\u2063](tg://user?id={x.id})"
      await reply_to_id.reply(mentions)
      await event.delete()
      
      
CMD_HELP.update(
    {
      "tagall": ">`.all` <custom msg/reply>"
      "\nUsage: Tag all member in the group chat."
    }
)
      
