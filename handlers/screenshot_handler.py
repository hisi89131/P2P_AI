import os

from telethon import events

from core.clients import (
    user_client
)

from memory.multi_order_map import (
    MERCHANT_ORDERS
)

from memory.pending_images import (
    PENDING_IMAGES
)

from core.storage import (
    ACTIVE_ORDERS,
    USER_WAITING,
    LAST_SCREENSHOT_TIME
)


@user_client.on(events.NewMessage(incoming=True))
async def screenshot_handler(event):

    try:

        if event.is_group:
            return

        sender = await event.get_sender()

        if getattr(sender, "bot", False):
            return

        merchant_id = sender.id

        text = event.raw_text or ""

        # ===================================
        # IMAGE DETECTION
        # ===================================

        has_image = False

        if event.photo:
            has_image = True

        if (
            event.document
            and event.file
            and event.file.mime_type
            and "image" in event.file.mime_type
        ):
            has_image = True

        # ===================================
        # SAVE SCREENSHOT TEMP
        # ===================================

        if has_image:

            import time

            LAST_SCREENSHOT_TIME[
                merchant_id
            ] = time.time()

            file_path = await event.download_media()

            PENDING_IMAGES[
                merchant_id
            ] = file_path

            merchant_orders = MERCHANT_ORDERS.get(
                merchant_id,
                []
            )

            if not merchant_orders:
                return

            # AUTO SINGLE ORDER
            if len(merchant_orders) == 1:

                text = merchant_orders[0]

            else:

                pending_text = "\n".join(
                    merchant_orders
                )

                await user_client.send_message(

                    merchant_id,

                    "Which Order ID?\n\n"
                    f"Pending Orders:\n{pending_text}"
                )

                return

        # ===================================
        # ORDER ID CONFIRM
        # ===================================

        if text.isdigit():

            merchant_orders = MERCHANT_ORDERS.get(
                merchant_id,
                []
            )

            if text not in merchant_orders:
                return

            order_id = text

            # ===================================
            # CHECK SAVED IMAGE
            # ===================================

            file_path = PENDING_IMAGES.get(
                merchant_id
            )

            if not file_path:
                return

            # ===================================
            # GET ORDER DATA
            # ===================================

            data = ACTIVE_ORDERS.get(order_id)

            if not data:
                return

            users = data["users"]

            # ===================================
            # SEND TO USERS
            # ===================================

            for uid, udata in users.items():

                try:

                    caption = (

                        "✅ PAYMENT SCREENSHOT\n\n"

                        f"📦 Order ID:\n"
                        f"<code>{order_id}</code>\n\n"

                        "━━━━━━━━━━━━━━━\n\n"

                        "OK DONE ✅"
                    )

                    await user_client.send_file(

                        entity=uid,

                        file=file_path,

                        caption=caption,

                        parse_mode="html",

                        force_document=False
                    )

                    # GROUP REPLY

                    await user_client.send_message(

                        entity=udata["chat_id"],

                        message="Screenshot sent in DM.",

                        reply_to=udata["msg_id"]
                    )

                    USER_WAITING[uid] = False

                except Exception as e:

                    print(
                        f"FORWARD ERROR => {e}"
                    )

            # ===================================
            # REMOVE ORDER
            # ===================================

            if order_id in ACTIVE_ORDERS:

                del ACTIVE_ORDERS[order_id]

            try:

                MERCHANT_ORDERS[
                    merchant_id
                ].remove(order_id)

            except:
                pass

            # ===================================
            # REMOVE USED IMAGE
            # ===================================

            try:

                del PENDING_IMAGES[
                    merchant_id
                ]

            except:
                pass

            # ===================================
            # REMAINING ORDERS
            # ===================================

            remaining_orders = MERCHANT_ORDERS.get(
                merchant_id,
                []
            )

            # ===================================
            # ALL DONE
            # ===================================

            if not remaining_orders:

                await user_client.send_message(

                    merchant_id,

                    "All screenshots received.\n\n"
                    "Thank you ✅"
                )

            # ===================================
            # REMAINING
            # ===================================

            else:

                remaining_text = "\n".join(
                    remaining_orders
                )

                await user_client.send_message(

                    merchant_id,

                    "OK DONE ✅\n\n"
                    "Please send screenshot for remaining orders:\n\n"
                    f"{remaining_text}"
                )

    except Exception as e:

        print(
            f"SCREENSHOT ERROR => {e}"
        )
