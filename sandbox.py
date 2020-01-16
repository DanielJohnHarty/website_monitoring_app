import asyncio
import random


async def slow_func(s):
    r = random.randint(1, 5)
    await asyncio.sleep(r)
    print(" "*s+f"it took me {r} second to finish this")


async def main():

    await asyncio.gather(slow_func(), slow_func(), slow_func())


async def monitor():
    while True:
        r = random.randint(1, 5)
        print(f"I will wait {r} seconds before calling slow_func.")
        await asyncio.sleep(r)
        await slow_func(r)


if __name__ == "__main__":
    asyncio.run(monitor())
