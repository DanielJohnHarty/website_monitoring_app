import asyncio
from website import Website
from console_writer import ConsoleWriter


def get_websites_to_monitor():
    """
    Enables user to input website data which is
    used to create Website instances as part of a
    list.

    PARAMETERS: None
    RETURNS: list
    """
    websites = []
    while True:
        print("Please enter the a website you wish to monitor")

        # try:
        #     url = input().lower()
        # except Exception("URL not valid"):
        #     continue
        url = 'http://google.com'#input().lower()
        print("How many seconds between consequetive checks?:")
        check_interval = 25#int(input())
        website = Website(url=url, check_interval=check_interval)
        if website.valid_url:
            websites.append(website)
            print(f"Your website has been added to the monitoring list.")
            print(f"In total that makes {len(websites)}. Add another? [y/n]")

            if input().lower() in ["yes", "y"]:
                continue
            else:
                break

        else:
            continue

    return websites


async def monitor_websites(websites_to_monitor, console_writer):

    coros = [
        asyncio.create_task(website.monitor_website())
        for website in websites_to_monitor
    ]

    for website in websites_to_monitor:
        coro = website.generate_update(timespan=-300, writer=console_writer)
        coros.append(coro)

    print(f"Beginning website monitoring...")

    await asyncio.gather(*coros)


# async def update_stats(websites_to_monitor, console_writer):

#     coros = [
#         asyncio.create_task(

#             website.generate_update(
#                 timespan=-300,
#                 console_writer=console_writer
#                 )
#         )

#         for website in websites_to_monitor
#     ]

#     print(f"Beginning website stat reporting...")

#     await asyncio.gather(*coros)


if __name__ == "__main__":

    console_writer = ConsoleWriter()

    console_writer.greet()

    websites_to_monitor = get_websites_to_monitor()

    try:
        asyncio.run(monitor_websites(websites_to_monitor, console_writer))

    except KeyboardInterrupt:

        console_writer.goodbye()


"""
http://google.com

http://ign.com
http://office.com
"""
