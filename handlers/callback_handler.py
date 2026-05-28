from telethon import events

from core.clients import bot

from config import OWNER_IDS


@bot.on(events.CallbackQuery)
async def callbacks(event):

    try:

        data = event.data.decode()

        if not data.startswith("handle_"):
            return

        order_id = data.replace(
            "handle_",
            ""
        )

        sender = await event.get_sender()

        sender_name = (
            sender.first_name
            or "Unknown"
        )

        sender_username = (
            f"@{sender.username}"
            if sender.username
            else str(sender.id)
        )

        await event.answer(
            "Order handled.",
            alert=True
        )

        current = await event.get_message()

        new_text = (
            current.raw_text
            + "\n\n━━━━━━━━━━━━━━━\n\n"
            + "✅ HANDLED BY\n\n"
            + f"{sender_name}\n"
            + f"{sender_username}"
        )

        await event.edit(
            new_text,
            buttons=None,
            parse_mode="html"
        )

        for owner_id in OWNER_IDS:

            if owner_id == sender.id:
                continue

            try:

                await bot.send_message(
                    owner_id,
                    (
                        "⚡ ORDER HANDLED\n\n"
                        f"📦 Order ID:\n"
                        f"<code>{order_id}</code>\n\n"
                        f"👤 Handled By:\n"
                        f"{sender_username}"
                    ),
                    parse_mode="html"
                )

            except:
                pass

    except Exception as e:

        print(
            f"BUTTON ERROR => {e}"
        )
