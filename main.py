import asyncio
from telethon import events
from config import BOT_TOKEN

from core.clients import (
    user_client,
    bot
)

# IMPORT HANDLERS

import handlers.group_handler
import handlers.dm_handler
import handlers.screenshot_handler
import handlers.callback_handler
from ai.ai_trainer import (
    train_from_groups
)
from handlers.ai_group_handler import ai_group_handler

print("BOT STARTED...")


async def main():

    await user_client.start()

    await bot.start(
        bot_token=BOT_TOKEN
    )

    print("MONITORING STARTED...")

    await train_from_groups()

    user_client.add_event_handler(
        ai_group_handler,
        events.NewMessage
    )

    await asyncio.gather(

        user_client.run_until_disconnected(),

        bot.run_until_disconnected()
    )


asyncio.run(main())
