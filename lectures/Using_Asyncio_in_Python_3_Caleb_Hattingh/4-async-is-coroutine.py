# yeild をつかったcoroutineと同じ

import asyncio


async def f():
    try:
        while True:
            await asyncio.sleep(0)
    except asyncio.CancelledError:
        print("I was cancelled!")
    else:
        print(111)


coro = f()
coro.send(None)
coro.send(None)
coro.throw(asyncio.CancelledError)

# 簡単にするとこうなる


async def f2():
    await asyncio.sleep(0)
    print(111)


loop = asyncio.get_event_loop()
coro = f2()
loop.run_until_complete(coro)
