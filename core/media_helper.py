import os

async def remove_file(path):

    try:

        if os.path.exists(path):
            os.remove(path)

    except:
        pass
