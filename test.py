# SuperFastPython.com
# example of a sleep in a periodic task
import asyncio
import time
 
# periodic task
async def periodic1():
    cou = int()
    
    # loop forever
    while True:
        await asyncio.sleep(2)
        cou += 1
        print('periodic1:', cou)


async def periodic2():
    cou = int()

    while True:
        await asyncio.sleep(4)
        cou += 1
        print("periodic2:", cou)
 
async def main():
    _2 = asyncio.create_task(periodic2())
    _1 = asyncio.create_task(periodic1())

    print("main")

    while True:
        await asyncio.sleep(0)
 
asyncio.run(main())