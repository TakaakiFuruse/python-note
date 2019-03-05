import asyncio
import datetime
import sqlite3
import time

import aiosqlite
import pandas as pd

path = "my.db"

"""
Factoryを使ってクエリーを出すパターン

========main1=======
[[1301, 1301, 1301], [7203, 7203, 7203], [2501, 2501, 2501]]
async queries 0:00:03.103346
"""

async def conn(query):
    async with aiosqlite.connect(path) as db:
        async with db.execute(query) as cursor:
            return [row[0] async for row in cursor][0:3]


async def query_factory(code):
    query = f"SELECT * from fds_fin where SECURITY_CODE = {code};"
    await asyncio.sleep(1)
    yield query, conn


async def main1():
    codes = [1301, 7203, 2501]
    result = []

    for code in codes:
        async for query, conn in query_factory(code):
            result.append(await conn(query))
    print(result)


print("========main1=======")
now1 = datetime.datetime.now()
asyncio.get_event_loop().run_until_complete(main1())
done1 = datetime.datetime.now()

print("async queries", done1 - now1)
