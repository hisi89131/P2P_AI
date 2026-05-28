import re
import asyncio

def extract_order(text):

    if not text:
        return None

    match = re.search(
        r"\b\d{6}\b",
        text
    )

    if match:
        return match.group()

    return None

async def auto_delete_message(
    client,
    chat_id,
    msg_id,
    seconds
):

    try:

        await asyncio.sleep(seconds)

        await client.delete_messages(
            chat_id,
            msg_id
        )

    except Exception as e:

        print(
            f"AUTO DELETE ERROR => {e}"
        )

def generate_message_link(
    chat,
    chat_id,
    msg_id
):

    try:

        if chat.username:

            return (
                f"https://t.me/"
                f"{chat.username}/"
                f"{msg_id}"
            )

        clean_id = str(chat_id).replace(
            "-100",
            ""
        )

        return (
            f"https://t.me/c/"
            f"{clean_id}/"
            f"{msg_id}"
        )

    except:

        return "No Link"
