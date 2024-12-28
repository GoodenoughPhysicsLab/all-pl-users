import os
import asyncio
from physicsLab import web, ResponseFail

user = web.User(
    token="dqQXBDflrOYV4a82HMbNjFtz9k3C5hWL",
    auth_code="aUKltj1Nq7JOz0EWHDnXoYP6fk3G4rRd",
)

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(SCRIPT_PATH, "all_id")) as f:
    all_id: list = eval(f.read())

with open(os.path.join(SCRIPT_PATH, "last_all_id")) as f:
    last_all_id: set = eval(f.read())

# for a_id in all_id:
#     if a_id not in last_all_id:
#         try:
#             user.follow(a_id)
#         except ResponseFail as e:
#             print(a_id, e)

async def main():
    tasks = []
    for a_id in all_id:
        if a_id not in last_all_id:
            tasks.append(asyncio.create_task(user.async_follow(a_id)))
    await asyncio.gather(*tasks)

asyncio.run(main())
