import os
import time
from physicsLab import web

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))

user = web.token_login(
    token="dqQXBDflrOYV4a82HMbNjFtz9k3C5hWL",
    auth_code="aUKltj1Nq7JOz0EWHDnXoYP6fk3G4rRd",
)

with open(os.path.join(SCRIPT_PATH, "all_id")) as f:
    lst: list = eval(f.read())

if os.path.exists(os.path.join(SCRIPT_PATH, "index")):
    with open(os.path.join(SCRIPT_PATH, "index")) as f:
        index = int(f.read())
else:
    index = 0

def main():
    try:
        for i, user_id in enumerate(lst[index:]):
            for a_user in web.RelationsIter(user, user_id=user_id, display_type="Following", max_retry=15):
                if a_user["User"]["ID"] not in lst:
                    lst.append(a_user["User"]["ID"])
            for a_user in web.RelationsIter(user, user_id=user_id,  display_type="Follower", max_retry=15):
                if a_user["User"]["ID"] not in lst:
                    lst.append(a_user["User"]["ID"])
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] index: {index + i}, amount: {len(lst)}", flush=True)
    finally:
        with open(os.path.join(SCRIPT_PATH, "all_id"), "w") as f:
            f.write(str(lst))
        with open(os.path.join(SCRIPT_PATH, "index"), "w") as f:
            f.write(str(index + i - 1))

if __name__ == "__main__":
    while True:
        try:
            main()
        except KeyboardInterrupt:
            break
        else:
            break
    print("")
