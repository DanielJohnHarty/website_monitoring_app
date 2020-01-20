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

        url = get_url()
        check_interval = get_check_interval()



        try:
            website = get_website(url, check_interval)
        except Exception:
            # Failed. Try again.
            continue

        websites.append(website)

        if get_more_websites(websites):
            continue
        else:
            return websites


def get_more_websites(websites):
    """
    """
    print(f"Your website has been added to the monitoring list.")
    print(f"In total that makes {len(websites)}. Add another? [y/n]")

    if input().lower() in ["yes", "y"]:
        res = True
    else:
        res = False

    return res


def get_website(url, check_interval):
    try:
        website = Website(url=url, check_interval=check_interval)

    except Exception:
        print(
            "I wasn't able to connect with that URL.\n"
            + "Please revise it, including 'http://'"
            + " or 'https://' as appropriate)."
        )
        raise Exception

    return website


def get_url():
    print("Please enter the a website you wish to monitor")
    url = input().lower()
    return url


def get_check_interval():
    check_interval = None
    print("How many seconds between consequetive checks?:")
    while not check_interval:
        try:
            check_interval = int(input())  # 25#
        except ValueError:
            print("That doesn't look like a number. Try again please.")
            continue
    return check_interval


async def monitor_websites(websites_to_monitor, console_writer):

    coros = [
        asyncio.create_task(website.monitor_website())
        for website in websites_to_monitor
    ]

    for website in websites_to_monitor:
        coro = website.generate_update(
            timespan=-300, writer=console_writer, recurrence_in_seconds=10
        )
        coros.append(coro)

    print(f"Beginning website monitoring...")

    await asyncio.gather(*coros)


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
