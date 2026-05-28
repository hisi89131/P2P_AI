import json
import os
import random

from rapidfuzz import fuzz


MEMORY_FILE = "ai/training/memory.json"

MEMORY = []


# LOAD MEMORY

def load_memory():

    global MEMORY

    if not os.path.exists(MEMORY_FILE):

        os.makedirs(
            os.path.dirname(MEMORY_FILE),
            exist_ok=True
        )

        with open(MEMORY_FILE, "w") as f:

            json.dump([], f)

    try:

        with open(MEMORY_FILE, "r") as f:

            MEMORY = json.load(f)

    except:

        MEMORY = []


# SAVE MEMORY

def save_memory():

    with open(MEMORY_FILE, "w") as f:

        json.dump(
            MEMORY[-50000:],
            f,
            indent=2
        )


# TRAIN AI

def train_ai(question, answer):

    global MEMORY

    if not question:
        return

    if not answer:
        return

    q = question.lower().strip()

    a = answer.strip()

    MEMORY.append({

        "q": q,

        "a": a
    })

    save_memory()


# FIND BEST REPLY

def generate_reply(text):

    global MEMORY

    text = text.lower().strip()

    best_score = 0

    best_reply = None

    random.shuffle(MEMORY)

    for item in MEMORY:

        try:

            q = item["q"]

            score = fuzz.token_sort_ratio(
                text,
                q
            )

            if score > best_score:

                best_score = score

                best_reply = item["a"]

        except:
            pass

    print(
        f"AI SCORE => {best_score}"
    )

    if best_score >= 55:

        return best_reply

    return None


load_memory()
