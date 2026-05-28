import re
from collections import defaultdict

from core.storage import (
    AI_GROUP_MEMORY
)


def clean_text(text):

    if not text:
        return ""

    text = text.lower()

    text = re.sub(
        r"http\S+",
        "",
        text
    )

    text = re.sub(
        r"[^a-zA-Z0-9 ]",
        "",
        text
    )

    return text.strip()


def learn_message(
    group_id,
    question,
    answer
):

    if not question:
        return

    if not answer:
        return

    q = clean_text(question)

    a = answer.strip()

    if group_id not in AI_GROUP_MEMORY:

        AI_GROUP_MEMORY[group_id] = []

    AI_GROUP_MEMORY[group_id].append({

        "question": q,

        "answer": a
    })

    # LIMIT MEMORY

    if len(
        AI_GROUP_MEMORY[group_id]
    ) > 20000:

        AI_GROUP_MEMORY[group_id] = (
            AI_GROUP_MEMORY[group_id][-20000:]
        )


def find_reply(
    group_id,
    text
):

    if group_id not in AI_GROUP_MEMORY:
        return None

    cleaned = clean_text(text)

    best = None

    best_score = 0

    for item in AI_GROUP_MEMORY[group_id]:

        q = item["question"]

        score = 0

        for word in cleaned.split():

            if word in q:
                score += 1

        if score > best_score:

            best_score = score

            best = item["answer"]

    if best_score >= 2:
        return best

    return None
