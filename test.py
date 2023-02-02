# SuperFastPython.com
# example of a sleep in a periodic task
import asyncio
import time



async def periodic1():
    cou = int()
    #asyncio.create_task(periodic3())
    #await asyncio.sleep(0)

    while True:
        cou += 1
        print('periodic1:', cou)





async def periodic2():
    cou = int()

    while True:
        await asyncio.sleep(3)
        cou += 1
        print("periodic2:", cou)

async def periodic3():
    cou = int()

    while True:
        await asyncio.sleep(2)
        cou += 1
        print("periodic3:", cou)
async def gg_wp():
    #asyncio.run()
    await loop.create_task(periodic2())


def doof():
    return loop.create_task(periodic2())

    return 1

loop1 = asyncio.new_event_loop()


#loop = asyncio.eve
    
import nest_asyncio
nest_asyncio.apply()


async def main():
    #asyncio.create_task(periodic2())
    #loop.create_task(gg_wp())
    loop.create_task(periodic1())

    print("main")

    while True:
        await asyncio.sleep(10)
        print("main після 10 секунд")

loop = asyncio.new_event_loop()


async def go():
    await asyncio.sleep(1)

    loop.run_forever()



async def periodic1():
    cou = int()
    #asyncio.create_task(periodic3())
    #await asyncio.sleep(0)

    while cou < 5:
        cou += 1
        print('periodic1:', cou)

async def periodic2():
    cou = int()

    while True:
        await asyncio.sleep(3)
        cou += 1
        print("AAAAAAAAAAAAAAAAA:", cou)


loop.create_task(periodic1())

print("AAAA")

loop.create_task(periodic2())

#loop.run_forever()
loop.run_forever()


#loop.run_until_complete(main())
    

#asyncio.run(periodic1())


#main()
#asyncio.run(main())

#loop = asyncio.new_event_loop()
#
#asyncio.set_event_loop(loop)