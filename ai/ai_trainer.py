from telethon.tl.types import Message

from ai.ai_engine import train_ai

from config import AI_ANALYZE_GROUPS

from core.clients import user_client


async def train_from_groups():

    print("AI TRAINING STARTED...")

    total = 0

    for group in AI_ANALYZE_GROUPS:

        try:

            async for msg in user_client.iter_messages(
                group,
                limit=20000
            ):

                try:

                    if not isinstance(msg, Message):
                        continue

                    if not msg.raw_text:
                        continue

                    if not msg.reply_to_msg_id:
                        continue

                    replied = await msg.get_reply_message()

                    if not replied:
                        continue

                    q = replied.raw_text
                    a = msg.raw_text

                    if len(q) < 2:
                        continue

                    if len(a) < 2:
                        continue

                    train_ai(q, a)

                    total += 1

                    if total % 100 == 0:

                        print(
                            f"TRAINED: {total}"
                        )

                except:
                    pass

        except Exception as e:

            print(
                f"TRAIN GROUP ERROR => {e}"
            )

    print(
        f"AI TRAINING COMPLETE => {total}"
    )
