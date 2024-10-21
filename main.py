import atexit
import os
import copy
import time
from datetime import datetime
from physicsLab import web

TIMEOUT = 1200
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
user = web.User()
with open(os.path.join(PROJECT_DIR, "searched_id")) as f:
    searched_id: set = eval(f.read())
with open(os.path.join(PROJECT_DIR, "all_id")) as f:
    all_id: set = eval(f.read())

def search(user_id: str):
    if user_id not in searched_id:
        searched_id.add(user_id)
        all_id.add(user_id)
        for a_id in web.RelationsIter(user, user_id):
            all_id.add(a_id["User"]["ID"])
        for a_id in web.RelationsIter(user, user_id, "Following"):
            all_id.add(a_id["User"]["ID"])

def exit_callback():
    with open(os.path.join(PROJECT_DIR, "searched_id"), 'w') as f:
        f.write(str(searched_id))
    with open(os.path.join(PROJECT_DIR, "all_id"), 'w') as f:
        f.write(str(all_id))
    print(f"searched_id: {len(searched_id)}, all_id: {len(all_id)}")
    now = datetime.now()
    print(f"program shutdown at {now.month}/{now.day}/{now.hour}:{now.minute}:{now.second}")

def main():
    all_id_copy = copy.deepcopy(all_id)
    start = time.time()
    for a_id in all_id_copy:
        search(a_id)
        if TIMEOUT is not None and time.time() - start > TIMEOUT:
            break

if __name__ == "__main__":
    atexit.register(exit_callback)

    main()
