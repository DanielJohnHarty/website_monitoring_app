import asyncio
from website import Website

LINE_LENGTH = 60
BOLD_LINE = "=" * LINE_LENGTH
SINGLE_LINE = "-" * LINE_LENGTH
WELCOME_MSG = "Website monitoring application"
GOODBYE_MSG = "Come back soon!"


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
        url = input().lower()
        print("How many seconds between consequetive checks?:")
        check_interval = int(input())
        website = Website(url=url, check_interval=check_interval)
        websites.append(website)
        print(f"Your website has been added to the monitoring list.")
        print(f"In total that makes {len(websites)}. Add another? [y/n]")

        if input().lower() in ["yes", "y"]:
            continue
        else:
            break

    return websites


async def monitor_websites(websites_to_monitor):

    coros = [
        asyncio.create_task(website.monitor_website())
        for website in websites_to_monitor
    ]

    print(f"Beginning website monitoring...")


    await asyncio.gather(*coros)




if __name__ == "__main__":

    print(f"{BOLD_LINE}\n{WELCOME_MSG}\n{SINGLE_LINE}")

    websites_to_monitor = get_websites_to_monitor()

    try:
        asyncio.run(monitor_websites(websites_to_monitor))
    
    except KeyboardInterrupt:

        print(f"{SINGLE_LINE}\n{GOODBYE_MSG}\n{BOLD_LINE}")




"""
http://google.com
http://ign.com
http://office.com
"""
