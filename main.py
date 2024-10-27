import os
import copy
import time
from datetime import datetime
from physicsLab import web

TIMEOUT: int = 600
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
user = web.User()
with open(os.path.join(PROJECT_DIR, "searched_id")) as f:
    searched_id: set = eval(f.read())
with open(os.path.join(PROJECT_DIR, "all_id")) as f:
    all_id: set = eval(f.read())

def search(user_id: str):
    if user_id not in searched_id:
        statistic = user.get_user(user_id)['Data']['Statistic']
        for a_id in web.RelationsIter(
            user, user_id, force_success=True, amount=statistic['FollowerCount']
        ):
            all_id.add(a_id["User"]["ID"])
        for a_id in web.RelationsIter(
            user, user_id, "Following", force_success=True, amount=statistic['FollowingCount']
        ):
            all_id.add(a_id["User"]["ID"])
        searched_id.add(user_id)

def save_data():
    with open(os.path.join(PROJECT_DIR, "searched_id"), 'w') as f:
        f.write(str(searched_id))
    with open(os.path.join(PROJECT_DIR, "all_id"), 'w') as f:
        f.write(str(all_id))
    now = datetime.now()
    print(
        f"[[{now.month}/{now.day} {now.hour}:{now.minute}:{now.second}]]"
        f" searched_id: {len(searched_id)}, all_id: {len(all_id)}"
    )

def main():
    while True:
        all_id_copy = copy.deepcopy(all_id)
        start = time.time()
        for a_id in all_id_copy:
            search(a_id)
            if time.time() - start > TIMEOUT:
                save_data()
                break
        if len(all_id) == len(searched_id):
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        save_data()
