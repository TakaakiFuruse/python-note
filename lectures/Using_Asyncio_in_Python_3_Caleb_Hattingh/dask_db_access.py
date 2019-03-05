import asyncio
import datetime
import sqlite3
import time

import aiosqlite
from dask import dataframe as dd

path = "sqlite:////home/data.db"


table = dd.read_sql_table("fin_data", path, index_col="code")


async def query_factory(code):
    yield code, table


async def main1():
    codes = ["極洋", "トヨタ", "扶桑化学"]
    result = []

    for code in codes:
        async for code, table in query_factory(code):
            result.append(table[table["name"].str.contains(code)].head())
    print(result)


print("========main1=======")
now1 = datetime.datetime.now()
asyncio.get_event_loop().run_until_complete(main1())
done1 = datetime.datetime.now()

print("async queries", done1 - now1)
