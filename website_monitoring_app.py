import asyncio
from website import Website
from console_writer import ConsoleWriter
import sys


class App:
    def __init__(self):
        self.console_writer = ConsoleWriter()
        self.console_writer.greet()
        self.websites_to_monitor = self.get_websites_to_monitor()
        self.schedules = schedules

    def start_app(self, schedules):

        asyncio.run(self.monitor_websites())

        print("n")

    def get_websites_to_monitor(self):
        """
        Enables user to input website url and check_interval
        which are used to create Website instances. These are
        returned as the list variable, websites.

        PARAMETERS: None
        RETURNS: list
        """
        websites = []

        while True:

            website_instance = self.create_website()
            if website_instance:
                websites.append(website_instance)
                self.console_writer.add_dashboard(website_instance.dashboard)
                print(f"Your website has been added to the monitoring list")

            if not self.user_wants_more(websites):
                break

        return websites

    def close_app(self):
        self.console_writer.goodbye()
        sys.exit()

    def create_website(self):
        """
        Creates an instance of the Website class based on
        user input.

        PARAMETERS: None
        RETURNS: Website instance or None
                depending on success of instantiation
        """
        url = self.get_user_url()
        check_interval = self.get_user_check_interval()
        website = self.get_website(url, check_interval)

        if website:
            return website

    def user_wants_more(self, websites):
        """
        Displays current number of items in the websites parameter
        and asks use for input.

        RETURNS: True is user inputs something equating to 'yes' else False
        """

        print(f"In total that makes {len(websites)}. Add another? [y/n]")

        return input().lower() in ["yes", "y"]

    def get_website(self, url: str, check_interval: int):
        """
        Instantiates Website instance. Safely returns 
        instance or None depending on success.

        PARAMETERS: check_interval: Positive integer in seconds.
                        Ping refresh freuency e.g. 30 would 
                        equate to check every 30 seconds
                    url: String e.g. http://google.fr
        Instantiates Website instance.

        RETURNS: Website instance or None.
        """
        try:

            website = Website(url=url, check_interval=check_interval)

        except Exception:
            print(
                "I wasn't able to connect with that URL.\n"
                + "Please revise it, including 'http://'"
                + " or 'https://' as appropriate)."
            )
            return None

        return website

    def get_user_url(self):
        """
        Returns user input after being asked for a url.
        Checking is done on Website isntance instatiation
        but user url is expected to be of the form
        http://google.fr

        RETURNS: String
        """
        print("Please enter the a website you wish to monitor")
        url = input().lower()
        return url

    def get_user_check_interval(self):
        """
        Get check_interval from user input.

        PARAMETERS: None
        RETURNS: Int or None depending on input capture success
        """
        check_interval = None
        print("How many seconds between consequetive checks?:")
        while not check_interval:
            try:
                check_interval = int(input())
            except ValueError:
                print("That doesn't look like a number. Try again please.")
                continue
        return check_interval

    async def create_monitor(self):
        pass

    async def monitor_websites(self):
        """
        Collects all coroutines in to a list and runs them asyncronously.
        More can be added here.

        PARAMETERS: websites_to_monitor is a list of Webstite instances
                    console_writer is a ConsoleWriter instance
                    schedules: List of schedules objects
        """

        coros = [
            asyncio.create_task(
                website.all_async_tasks(self.schedules, self.console_writer)
            )
            for website in self.websites_to_monitor
        ]

        print(f"Beginning website monitoring...")

        # loop = asyncio.get_event_loop()
        # Add to event loop
        await asyncio.gather(*coros)


if __name__ == "__main__":

    # Define reporting schedules (in seconds))
    schedule1 = {"frequency": 10, "timeframe": -600}
    schedule2 = {"frequency": 60, "timeframe": -60 * 60}
    schedules = [schedule1, schedule2]

    # Instantiate app
    app = App()
    app.start_app(schedules=schedules)
