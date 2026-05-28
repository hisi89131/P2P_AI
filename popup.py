import asyncio
from telethon import Button
from config import OWNER_IDS, POPUP_DELETE_SECONDS

active_alerts = {}


async def send_popup(client, text, alert_id):

    buttons = [
        [
            Button.inline(
                "✅ HANDLE",
                data=f"handle_{alert_id}"
            )
        ]
    ]

    sent_messages = []

    for owner in OWNER_IDS:

        try:

            msg = await client.send_message(
                owner,
                text,
                buttons=buttons
            )

            sent_messages.append(msg)

        except Exception as e:
            print(e)

    active_alerts[alert_id] = sent_messages

    await asyncio.sleep(
        POPUP_DELETE_SECONDS
    )

    for msg in sent_messages:

        try:
            await msg.delete()
        except:
            pass
