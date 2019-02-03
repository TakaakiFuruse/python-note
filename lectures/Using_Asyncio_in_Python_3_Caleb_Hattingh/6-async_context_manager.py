import asyncio
import datetime
import sqlite3
import time

import aiosqlite
import pandas as pd

"""
Each query takes 1 sec.
Sync and Async comparison

========main1=======
<aiosqlite.core.Cursor object at 0x7f609d589710>
<aiosqlite.core.Cursor object at 0x7f609d589748>
<aiosqlite.core.Cursor object at 0x7f609d589780>
<aiosqlite.core.Cursor object at 0x7f609d589400>
========main1_2=======
<aiosqlite.core.Cursor object at 0x7f609d589550>
<aiosqlite.core.Cursor object at 0x7f609d589358>
<aiosqlite.core.Cursor object at 0x7f609d589278>
<aiosqlite.core.Cursor object at 0x7f609d589710>
========main2=======
<sqlite3.Cursor object at 0x7f60b2408f80>
<sqlite3.Cursor object at 0x7f60b2408f80>
<sqlite3.Cursor object at 0x7f60b2408f80>
<sqlite3.Cursor object at 0x7f60b2408f80>
async queries 0:00:01.014877
async queries 2 (gather) 0:00:01.017471
sync queries 0:00:04.030824


"""

path = "my.db"


async def query(query):
    async with aiosqlite.connect(path) as db:
        async with db.execute(query) as cursor:
            print(cursor)


def sync_query(query):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    print(c.execute(query))


async def kyokuyo():
    await asyncio.sleep(1)
    await query("SELECT * from table1 where code = 1301;")


async def toyota():
    await asyncio.sleep(1)
    await query("SELECT * from table1 where code = 7203;")


def sync_kyokuyo():
    time.sleep(1)
    sync_query("SELECT * from table1 where code = 1301;")


def sync_toyota():
    time.sleep(1)
    sync_query("SELECT * from table1 where code = 7203;")


async def main1():
    tasks = [
        asyncio.create_task(kyokuyo()),
        asyncio.create_task(toyota()),
        asyncio.create_task(kyokuyo()),
        asyncio.create_task(toyota()),
    ]
    for t in tasks:
        await t


async def main1_2():
    # 1 とやってることは同じっぽい
    await asyncio.gather(kyokuyo(), toyota(), kyokuyo(), toyota())


def main2():
    sync_kyokuyo()
    sync_toyota()
    sync_kyokuyo()
    sync_toyota()


print("========main1=======")
now1 = datetime.datetime.now()
asyncio.run(main1())
done1 = datetime.datetime.now()

print("========main1_2=======")
now1_2 = datetime.datetime.now()
asyncio.run(main1_2())
done1_2 = datetime.datetime.now()

print("========main2=======")
now2 = datetime.datetime.now()
main2()
done2 = datetime.datetime.now()

print("async queries", done1 - now1)
print("async queries 2 (gather)", done1_2 - now1_2)
print("sync queries", done2 - now2)
