import re

from telethon.tl.types import User

from core.clients import user_client

from config import SEARCH_GROUP


async def find_merchant(order_id):

    async for msg in user_client.iter_messages(
        SEARCH_GROUP,
        limit=500
    ):

        try:

            text = msg.raw_text or ""

            lower_text = text.lower()

            if order_id not in text:
                continue

            if "complete" not in lower_text:
                continue

            username_match = re.search(
                r'@([A-Za-z0-9_]+)',
                text
            )

            if not username_match:
                continue

            username = username_match.group(1)

            try:

                entity = await user_client.get_entity(
                    username
                )

            except Exception as e:

                print(
                    f"USERNAME ENTITY ERROR => {e}"
                )

                continue

            if not isinstance(
                entity,
                User
            ):
                continue

            return {

                "id": entity.id,

                "username": entity.username,

                "name": (
                    entity.first_name
                    or "Unknown"
                )
            }

        except Exception as e:

            print(
                f"SEARCH ERROR => {e}"
            )

    return None
