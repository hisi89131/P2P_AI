import asyncio
import time

from telethon import events

from core.clients import user_client

from core.storage import (
    USER_WAITING,
    LAST_SCREENSHOT_TIME
)

from core.smart_reply import (
    random_wait_message
)

LAST_REPLY = {}


@user_client.on(events.NewMessage(incoming=True))
async def dm_handler(event):

    try:

        if not event.is_private:
            return

        sender = await event.get_sender()

        user_id = sender.id

        # =========================
        # IGNORE MEDIA MESSAGES
        # =========================

        if event.photo:
            return

        if event.document:
            return

        # =========================
        # USER NOT IN WAITING
        # =========================

        if user_id not in USER_WAITING:
            return

        if not USER_WAITING[user_id]:
            return

        # =========================
        # SCREENSHOT DELAY CHECK
        # =========================

        last_ss = LAST_SCREENSHOT_TIME.get(user_id)

        if last_ss:

            passed = time.time() - last_ss

            # 60 sec silence after screenshot
            if passed < 60:
                return

        # =========================
        # NORMAL COOLDOWN
        # =========================

        now = asyncio.get_event_loop().time()

        last = LAST_REPLY.get(user_id, 0)

        # 10 sec cooldown

        if now - last < 10:
            return

        LAST_REPLY[user_id] = now

        # =========================
        # HUMAN DELAY
        # =========================

        await asyncio.sleep(10)

        # =========================
        # FINAL CHECK
        # =========================

        if USER_WAITING.get(user_id):

            await event.reply(
                random_wait_message()
            )

    except Exception as e:

        print(f"DM ERROR => {e}")
