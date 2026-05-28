from core.clients import bot

from config import BOT_LOG_GROUP


async def log_unknown_case(
    group_name,
    text
):

    try:

        msg = (

            "⚠️ AI UNKNOWN CASE\n\n"

            f"GROUP:\n{group_name}\n\n"

            f"MESSAGE:\n{text}"
        )

        await bot.send_message(
            BOT_LOG_GROUP,
            msg
        )

    except Exception as e:

        print(
            f"UNKNOWN LOG ERROR => {e}"
        )
