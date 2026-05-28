import asyncio
import random
import time

from core.storage import (
    ACTIVE_ORDERS,
    PAYMENT_CACHE
)

from core.clients import user_client


REMINDER_MESSAGES = [

    "Please send screenshot",

    "Kindly send screenshot",

    "Please respond fast",

    "Waiting for payment screenshot",

    "Please update payment status"
]


async def reminder_loop(order_id):

    while True:

        await asyncio.sleep(40)

        if order_id not in ACTIVE_ORDERS:
            return

        data = ACTIVE_ORDERS[order_id]

        merchant_id = data["merchant_id"]

        # STOP SPAM AFTER SCREENSHOT

        cache = PAYMENT_CACHE.get(
            order_id,
            {}
        )

        if cache.get(
            "screenshot_received"
        ):

            last_time = cache.get(
                "last_screenshot_time",
                0
            )

            now = time.time()

            # WAIT 60 SEC AFTER SCREENSHOT

            if now - last_time < 60:
                continue

        try:

            await user_client.send_message(
                merchant_id,
                random.choice(
                    REMINDER_MESSAGES
                )
            )

        except Exception as e:

            print(
                f"REMINDER ERROR => {e}"
            )
