import asyncio

from telethon import Button

from core.storage import (
    ACTIVE_ORDERS,
    USER_WAITING
)

from core.clients import (
    user_client,
    bot
)

from core.helpers import (
    auto_delete_message
)

from config import (
    BOT_LOG_GROUP,
    BOT_ALERT_CHAT,
    OWNER_IDS
)


async def order_timeout(order_id):

    await asyncio.sleep(180)

    if order_id not in ACTIVE_ORDERS:
        return

    data = ACTIVE_ORDERS[order_id]

    try:

        first_user = list(
            data["users"].items()
        )[0]

        first_user_id = first_user[0]

        user_entity = await user_client.get_entity(
            first_user_id
        )

        user_name = (
            user_entity.first_name
            or "Unknown"
        )

        user_username = (
            f"@{user_entity.username}"
            if user_entity.username
            else "No Username"
        )

        timeout_text = (

            "⚠️ <b>ORDER TIMEOUT</b>\n\n"

            f"📦 <b>Order ID:</b>\n"
            f"<code>{order_id}</code>\n\n"

            "━━━━━━━━━━━━━━━\n\n"
            "👤 <b>User Details</b>\n\n"
            f"📝 <b>Name:</b>\n"
            f"{user_name}\n\n"
            f"🔹 <b>Username:</b>\n"
            f"{user_username}\n\n"
            f"📂 <b>Group:</b>\n"
            f"{data['group_name']}\n\n"
            f"🔗 <b>Message Link:</b>\n"
            f"{data['group_link']}\n\n"

            "━━━━━━━━━━━━━━━\n\n"
            "👨‍💻 <b>Merchant Details</b>\n\n"
            f"🔹 <b>Username:</b>\n"
            f"@{data['merchant_username']}\n\n"

            "━━━━━━━━━━━━━━━\n\n"
            "❌ Merchant did not respond in 3 minutes.\n"
            "Handle manually."
        )

        # LOG GROUP

        log_msg = await bot.send_message(
            BOT_LOG_GROUP,
            timeout_text,
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
            timeout_text,
            parse_mode="html",
            buttons=[
                [
                    Button.inline(
                        "⚡ Handle",
                        data=f"handle_{order_id}"
                    )
                ]
            ]
        )

        asyncio.create_task(
            auto_delete_message(
                bot,
                BOT_ALERT_CHAT,
                bot_msg.id,
                300
            )
        )

        # USER FINAL MSG

        for user_id in list(
            data["users"].keys()
        ):

            try:

                await user_client.send_message(
                    user_id,
                    (
                        "Merchant is not responding right now.\n\n"
                        "Admin is now handling this manually.\n\n"
                        "Please wait."
                    )
                )

            except Exception as e:

                print(
                    f"FINAL MSG ERROR => {e}"
                )

            USER_WAITING[user_id] = False

    except Exception as e:

        print(
            f"TIMEOUT ERROR => {e}"
        )

    ACTIVE_ORDERS.pop(
        order_id,
        None
    )
