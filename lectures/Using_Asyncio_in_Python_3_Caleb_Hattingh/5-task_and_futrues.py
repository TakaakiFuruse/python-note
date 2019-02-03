# みんな同じことをしている

import asyncio


async def background_job():
    print("doing background works!!")


async def option_a(loop):
    loop.create_task(background_job())


async def option_b():
    # このやり方は楽だが本来はAPI製作者用の関数
    asyncio.ensure_future(background_job())


async def option_c():
    loop = asyncio.get_event_loop()
    loop.create_task(background_job())


async def option_d():
    # これが一番簡単
    asyncio.create_task(background_job())


loop = asyncio.get_event_loop()

t1 = loop.create_task(option_a(loop))
t2 = loop.create_task(option_b())
t3 = loop.create_task(option_c())
t4 = loop.create_task(option_d())

tasks = asyncio.gather(t1, t2, t3, t4)
loop.run_until_complete(tasks)
