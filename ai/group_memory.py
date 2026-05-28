GROUP_MEMORY = {}

def save_memory(chat_id, text):

    if chat_id not in GROUP_MEMORY:

        GROUP_MEMORY[chat_id] = []

    GROUP_MEMORY[chat_id].append(text)

    if len(GROUP_MEMORY[chat_id]) > 200:

        GROUP_MEMORY[chat_id].pop(0)

def search_memory(chat_id, query):

    if chat_id not in GROUP_MEMORY:
        return None

    query = query.lower()

    matches = []

    for msg in GROUP_MEMORY[chat_id]:

        if query in msg.lower():

            matches.append(msg)

    if not matches:
        return None

    return matches[-3:]
