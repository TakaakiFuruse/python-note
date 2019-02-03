import time
import asyncio


async def main():
    print(f"{time.ctime()} Hello")
    await asyncio.sleep(1.0)
    print(f"{time.ctime()} Bye")
    loop.stop()


# async def blocking():
#     await asyncio.sleep(0.5)
#     print(f"{time.ctime()} Hello from a thread!")


def blocking():
    time.sleep(0.5)
    print(f"{time.ctime()} Hello from a thread!")


loop = asyncio.get_event_loop()
loop.create_task(main())
# loop.create_task(blocking())
loop.run_in_executor(None, blocking)

loop.run_forever()

pending = asyncio.Task.all_tasks(loop=loop)
group = asyncio.gather(*pending)
loop.run_until_complete(group)

loop.close()
