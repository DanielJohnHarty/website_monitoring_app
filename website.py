import httpx
import datetime
from asyncio import CancelledError

# import aiohttp
# from stat import Stat


class Website:
    def __init__(self, url=None, check_interval=None):
        self.url = url
        self.check_interval = check_interval
        # self.stats = Stat()

    def get_next_ping_time(self, dt: datetime = None) -> datetime:
        """
        Increments the time of the reference datetime parameter by
        the self.check_interval value in seconds.

        If no reference datetime value is passed, it returns the current
        datetime.

        PARAMETERS:
            dt: A datetime object
        RETURNS: A datetime object
        """
        if dt:
            next_ping_at = dt + datetime.timedelta(seconds=self.check_interval)
        else:
            next_ping_at = datetime.datetime.now()

        return next_ping_at

    def generate_update(period: int) -> str:
        """
        Generates a string describing the stats
        of the Website instance over the period
        passed as a parameter e.g. over 10 minutes
        or over 2 minutes

        PARAMETERS:
            period: In minutes as int

        RETURNS: str
        """
        return "Placeholder result string"

    async def monitor_website(self) -> None:
        """
        Async loop sending requests to self.url
        at the freauency of the self.check_interval.

        It is in charge of keeping self.stats up to date.

        PARAMETERS: None
        RETURNS: None
        """

        # async with aiohttp.ClientSession() as session:
        async with httpx.AsyncClient() as client:

            next_ping_time = self.get_next_ping_time()

            while True:


                if next_ping_time <= datetime.datetime.now():
                    # asyncio.sleep(self.check_interval)
                    
                    r = await self.ping_url(client, self.url)
                    
                    print(f"Pinged {self.url}:{r} in {str(r.elapsed)}.")
                    next_ping_time = self.get_next_ping_time(next_ping_time)


    async def ping_url(self, client, url) -> None:
        """
        Responsible for making a single reauest to
        self.url and updating self.stats with the
        results

        PARAMETERS: None
        RETURNS: None
        """
        # async with client.get(url) as response:
        #   return await response

        return await client.get(url, timeout=None)

