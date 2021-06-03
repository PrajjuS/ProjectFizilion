import asyncio
import random 
from random import choice
from userbot.events import register
from asyncio import sleep

TRD_NAMES=[
  "[Vinaya](https://t.me/Vin02vin)",
  "[Srinidhi](https://t.me/venomsamurai)",
  "[Sai Sharan](https://t.me/Iamsaisharan)",
  "[Prajwal](https://t.me/PrajjuS)",
]

animation_chars=[
  "**Truth**",
  "**or**",
  "**Dare**",
  "**Choosing Random Person....**",
  "**..........**",
  "**.....**",
  "**Done**",
]
  
@register(outgoing=True, pattern="^.trd$")
async def truthordare(trd):
  """T R D Chooser"""
  max_ani = len(animation_chars)
  for i in range(max_ani):
      await sleep(2)
      msg=await trd.edit(animation_chars[i % max_ani])
  await msg.sleep(3)
  await msg.edit("**Truth or Dare**\n\n**Name:** " + choice(TRD_NAMES))
