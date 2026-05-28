import random

SMART_REPLIES = [

    "Please wait.",

    "Checking details.",

    "Verification in progress.",

    "Merchant response pending.",

    "Please wait for confirmation.",

    "Processing payment details."

]

FAST_REPLIES = [

    "Please wait.",

    "Checking.",

    "Processing.",

    "Wait a moment."

]

def smart_reply():

    return random.choice(
        SMART_REPLIES
    )

def fast_reply():

    return random.choice(
        FAST_REPLIES
    )
