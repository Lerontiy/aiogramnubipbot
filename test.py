# SuperFastPython.com
# example of a sleep in a periodic task
import asyncio
import time
 
# periodic task
async def periodic1():
    # loop forever
    while True:
        await asyncio.sleep(1)
        print('periodic1')


async def periodic2():
    while True:
        await asyncio.sleep(2)
        print("periodic2")
 
async def main():
    _2 = asyncio.create_task(periodic2())
    _1 = asyncio.create_task(periodic1())

    while True:
        await asyncio.sleep(0)
 
asyncio.run(main())