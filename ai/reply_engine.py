import random

THINKING = [

    "Checking order...",
    "Please wait...",
    "Checking payment details...",
    "Merchant response pending...",
]

WAITING = [

    "Please wait.",
    "Merchant will respond soon.",
    "Please wait for confirmation.",
]

DM_REPLIES = [

    "Screenshot sent in DM.",
    "Please check your DM.",
    "Payment screenshot sent.",
]

def thinking_reply():

    return random.choice(
        THINKING
    )

def waiting_reply():

    return random.choice(
        WAITING
    )

def dm_reply():

    return random.choice(
        DM_REPLIES
    )
