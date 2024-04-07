import asyncio
import sys


async def robot(start: int):
    curr = start
    while True:
        print(curr)
        curr += 1
        await asyncio.sleep(1)


async def event_loop(start):
    task1 = asyncio.create_task(robot(start))
    await task1


if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            start = int(sys.argv[1])
            asyncio.run(event_loop(start))
        except ValueError:
            print("Start value is not integer. Program Stopped.")
    else:
        asyncio.run(event_loop(0))
