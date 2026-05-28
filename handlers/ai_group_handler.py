from telethon import events

from config import *

from ai.ai_engine import (
    train_ai,
    generate_reply
)

from telethon.tl.types import Message


LAST_MESSAGES = {}


async def ai_group_handler(event):

    try:

        if not AI_ENABLE:
            return

        if event.chat_id not in AI_ANALYZE_GROUPS:
            return

        if not event.raw_text:
            return

        text = event.raw_text.strip()

        sender = await event.get_sender()

        if not sender:
            return


        # =========================
        # TRAINING SYSTEM
        # =========================

        if event.is_reply:

            reply_msg = await event.get_reply_message()

            if reply_msg:

                old_text = reply_msg.raw_text

                if old_text:

                    train_ai(
                        old_text,
                        text
                    )


        # =========================
        # IGNORE OWN MESSAGES
        # =========================

        if sender.bot:
            return


        # =========================
        # AI REPLY SYSTEM
        # =========================

        reply = generate_reply(text)

        print(
            f"AI INPUT => {text}"
        )

        print(
            f"AI OUTPUT => {reply}"
        )

        if reply:

            await event.reply(reply)

            return


        # =========================
        # UNKNOWN ALERT
        # =========================

        if AI_LOG_UNKNOWN:

            try:

                await event.client.send_message(

                    BOT_LOG_GROUP,

                    f"""
❌ UNKNOWN MESSAGE

GROUP:
{event.chat_id}

MESSAGE:
{text}
"""
                )

            except:
                pass

    except Exception as e:

        print(
            f"AI GROUP ERROR => {e}"
        )
