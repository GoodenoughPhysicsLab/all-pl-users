import os
import time
from physicsLab import web
from physicsLab.web._threadpool import ThreadPool, _Task

user = web.token_login(
    token="dqQXBDflrOYV4a82HMbNjFtz9k3C5hWL",
    auth_code="aUKltj1Nq7JOz0EWHDnXoYP6fk3G4rRd",
)

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(SCRIPT_PATH, "all_id")) as f:
    all_id: list = eval(f.read())[44_000:]

with ThreadPool(max_workers=4) as pool:
    tasks: list[_Task] = []
    for id in all_id:
        tasks.append(pool.submit(user.follow, id))
    pool.submit_end()

    i = 0
    while i < len(tasks):
        a_task = tasks[i]
        try:
            a_task.result()
        except Exception as e:
            print('\n', e, flush=True)
        else:
            print(f"{i}/{len(tasks)}          ", end='\r', flush=True)
            i += 1
