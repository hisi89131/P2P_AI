import asyncio
import random

from telethon import events

from core.clients import (
    user_client,
    bot
)

from memory.multi_order_map import (
    MERCHANT_ORDERS
)

from core.storage import (
    ACTIVE_ORDERS,
    USER_WAITING
)

from core.helpers import (
    extract_order,
    generate_message_link,
    auto_delete_message
)

from core.merchant_finder import (
    find_merchant
)

from core.reminder import (
    reminder_loop
)

from core.timeout import (
    order_timeout
)

from core.smart_reply import (
    random_thinking,
    random_wait_message
)

from ai.ai_engine import (
    train_ai,
    generate_reply
)

from config import (
    SOURCE_GROUPS,
    BOT_LOG_GROUP,
    BOT_ALERT_CHAT
)


@user_client.on(
    events.NewMessage(
        chats=SOURCE_GROUPS
    )
)
async def group_handler(event):

    try:

        text = event.raw_text or ""

        # AI LEARNING

        try:

            if event.reply_to_msg_id:

                replied = await event.get_reply_message()

                if replied:

                    q = replied.raw_text or ""

                    a = text

                    train_ai(q, a)

        except:
            pass

        order_id = extract_order(text)

        if not order_id:

            ai_reply = generate_reply(text)

            if ai_reply:

                await asyncio.sleep(
                    random.randint(5, 15)
                )

                await user_client.send_message(

                    entity=event.chat_id,

                    message=ai_reply,

                    reply_to=event.id
                )

            else:

                try:

                    await bot.send_message(

                        BOT_LOG_GROUP,

                        f"UNKNOWN MESSAGE:\n\n{text}"
                    )

                except:
                    pass

            return

        sender = await event.get_sender()

        user_id = sender.id

        # DUPLICATE CHECK

        if order_id in ACTIVE_ORDERS:

            if (
                user_id
                in ACTIVE_ORDERS[order_id]["users"]
            ):
                return

        # FIND MERCHANT

        merchant = await find_merchant(
            order_id
        )

        # =========================
        # MERCHANT NOT FOUND
        # =========================

        if not merchant:

            try:

                msg_link = generate_message_link(
                    event.chat,
                    event.chat_id,
                    event.id
                )

                sender_name = (
                    sender.first_name
                    or "Unknown"
                )

                sender_username = (
                    f"@{sender.username}"
                    if sender.username
                    else "No Username"
                )

                fail_text = (

                    "❌ <b>MERCHANT NOT FOUND</b>\n\n"

                    f"📦 <b>Order ID:</b>\n"
                    f"<code>{order_id}</code>\n\n"

                    "━━━━━━━━━━━━━━━\n\n"

                    "👤 <b>User Details</b>\n\n"

                    f"📝 <b>Name:</b>\n"
                    f"{sender_name}\n\n"

                    f"🔹 <b>Username:</b>\n"
                    f"{sender_username}\n\n"

                    f"📂 <b>Group:</b>\n"
                    f"{event.chat.title}\n\n"

                    f"🔗 <b>Message Link:</b>\n"
                    f"{msg_link}"
                )

                # LOG GROUP

                log_msg = await bot.send_message(
                    BOT_LOG_GROUP,
                    fail_text,
                    parse_mode="html"
                )

                asyncio.create_task(
                    auto_delete_message(
                        bot,
                        BOT_LOG_GROUP,
                        log_msg.id,
                        300
                    )
                )

                # BOT ALERT

                bot_msg = await bot.send_message(
                    BOT_ALERT_CHAT,
                    fail_text,
                    parse_mode="html"
                )

                asyncio.create_task(
                    auto_delete_message(
                        bot,
                        BOT_ALERT_CHAT,
                        bot_msg.id,
                        300
                    )
                )

            except Exception as e:

                print(
                    f"NOT FOUND ERROR => {e}"
                )

            return

        # =========================
        # MERCHANT FOUND
        # =========================

        merchant_id = merchant["id"]

        merchant_username = merchant["username"]

        merchant_name = merchant["name"]

        # CREATE ORDER

        if order_id not in ACTIVE_ORDERS:

            ACTIVE_ORDERS[order_id] = {

                "merchant_id": merchant_id,

                "merchant_username": merchant_username,

                "merchant_name": merchant_name,

                "group_name": event.chat.title,

                "group_link": generate_message_link(
                    event.chat,
                    event.chat_id,
                    event.id
                ),

                "users": {},
            }

            if merchant_id not in MERCHANT_ORDERS:

                MERCHANT_ORDERS[merchant_id] = []

            MERCHANT_ORDERS[merchant_id].append(
                order_id
            )

            # SEND DM TO MERCHANT

            try:

                await user_client.send_message(
                    merchant_id,
                    f"Order ID: {order_id}"
                )

                await asyncio.sleep(1)

                await user_client.send_message(
                    merchant_id,
                    "Send payment screenshot"
                )

            except Exception as e:

                print(
                    f"MERCHANT DM ERROR => {e}"
                )

            # START TASKS

            asyncio.create_task(
                reminder_loop(order_id)
            )

            asyncio.create_task(
                order_timeout(order_id)
            )

        # SAVE USER

        ACTIVE_ORDERS[order_id]["users"][user_id] = {

            "chat_id": event.chat_id,

            "msg_id": event.id,
        }

        USER_WAITING[user_id] = True

        # GROUP REPLY

        reply_msg = await user_client.send_message(

            entity=event.chat_id,

            message=random_thinking(),

            reply_to=event.id
        )

        # EXTRA GROUP REPLY

        if event.reply_to_msg_id or len(text.split()) <= 6:

            text_lower = text.lower()

            small_words = [

                "ok",
                "fast",
                "jaldi",
                "bro",
                "bhai",
                "wait",
                "hello"
            ]

            if any(
                x in text_lower
                for x in small_words
            ):

                await user_client.send_message(

                    entity=event.chat_id,

                    message=random_wait_message(),

                    reply_to=event.id
                )

    except Exception as e:

        print(
            f"GROUP ERROR => {e}"
        )
