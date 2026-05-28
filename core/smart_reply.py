import random

WAIT_MESSAGES = [

    "Please wait for merchant response...",
    "Merchant response pending...",
    "Please wait...",
    "Waiting for screenshot...",
    "Merchant will respond soon...",
]

CHECK_DM_MESSAGES = [

    "Please check your DM.",
    "Screenshot sent in DM.",
    "Check your private messages.",
    "Payment screenshot send.",
]

THINKING_REPLIES = [

    "Checking order...",
    "Please wait...",
    "Checking payment details.",
    "Ok wait...",
]


def random_wait_message():

    return random.choice(
        WAIT_MESSAGES
    )


def random_dm_reply():

    return random.choice(
        CHECK_DM_MESSAGES
    )


def random_thinking():

    return random.choice(
        THINKING_REPLIES
    )
