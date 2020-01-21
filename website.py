import httpx
import datetime
from web_stats import WebStat
import asyncio
from console_writer import ConsoleWriter
from console_writer import WebPerformanceDashboard


class Website:
    def __init__(self, url=None, check_interval=None):
        """
        PARAMETERS: url: String. Must include protocol prefix e.g. http://
        """
        # Both raise exceptions if not compliant
        self.validate_url(url)
        self.validate_check_interval(check_interval)
        self.url = url
        self.check_interval = check_interval
        self.stats = WebStat(max_observation_window=-600)

        self.dashboard = WebPerformanceDashboard()

    def validate_url(self, url):
        try:
            # Test url connection
            _ = httpx.get(url)
        except Exception:
            raise Exception("URL error")

    def validate_check_interval(self, check_interval):
        if check_interval < 1:
            raise Exception("check_interval must be a positive integer")

    def get_relative_datetime(
        self, reference_datetime: datetime = None, timedelta_in_seconds: int = None
    ) -> datetime:
        """
        Returns the datetime at reference_datetime
        adjusted by timedelta_in_seconds

        A negative timedelta_in_seconds returns a datetime in the past.

        If no reference datetime value is passed, it returns the current
        datetime.

        PARAMETERS:
            dt: A datetime object
        RETURNS: A datetime object
        """

        if not timedelta_in_seconds and timedelta_in_seconds != 0:
            timedelta_in_seconds = self.check_interval

        if not reference_datetime:
            reference_datetime = datetime.datetime.now()

        return reference_datetime + datetime.timedelta(seconds=timedelta_in_seconds)

    async def generate_update(
        self, timespan: int, writer: ConsoleWriter, schedules: list
    ) -> None:
        """
        Generates a string describing the stats
        of the Website instance over the period
        passed as a parameter e.g. over 10 minutes
        would be oberservation_period = 10*60

        PARAMETERS:
            timespan: In seconds as int.
            Represents how far back in the raw data
            the update should report on e.g timespan
            = 60 to report on the past 60 seconds of datapoints.

            recurrence_in_seconds: List of integers specifying long to wait after the generation of one
                                   update to generate the next one

            timeframes: a list of integers representing the number of 
                        seconds to report over. [60, 600] means to report
                        over both the past minute and the past 10 minutes

        RETURNS: None
        """
        for s in schedules:
            freq = s["frequency"]  # How often there is an update on screen
            timeframe = s["timeframe"]  # What timeframe of data to be reported on
            await self.schedule_report(freq, timeframe, writer)

    async def schedule_report(self, delay, timeframe, writer):
        """
        Calls produce_report after a delay of 'delay' seconds, then recursively calls itself.
        Effect of infinite calls of the schedule report function. 
        
        PARAMETERS: delay: int, how long to wait before producing the report
                    timeframe: negative int, how many seconds ago is the data
                                cut off date
                    writer: ConsoleWriter instance which preforms all writing
                            command line.
        """
        await asyncio.sleep(delay)
        self.produce_report(timeframe, writer)
        asyncio.create_task(self.schedule_report(delay, timeframe, writer))
        # After creating a new task, end the current one.
        return

    def produce_report(self, timeframe, writer):
        """
        Retrieves updated stats from the self.stats instance
        and forwards to the ConsoleWriter instance writer
        for formatting before writing to the console

        PARAMETERS: timespan: In seconds as int e.g. 
                                -60 datapoints from previous minute
                             writer: ConsoleWriter instance responsible 
                                formatting reports and writing to the console
        """
        updated_stats = self.stats.get_updated_stats(timeframe=timeframe)
        updated_stats["url"] = self.url

        writer.update(data=updated_stats, dashboard=self.dashboard)

    async def monitor_website(self) -> None:
        """
        Async loop sending requests to self.url
        at the freauency of the self.check_interval.

        It is in charge of keeping self.stats up to date.

        PARAMETERS: None
        RETURNS: None
        """
        async with httpx.AsyncClient() as client:

            ping_time = datetime.datetime.now()

            while True:

                if ping_time <= datetime.datetime.now():

                    r = await client.get(self.url, timeout=None)

                    datapoint = {
                        "response_code": r.status_code,
                        "response_time": r.elapsed,
                    }

                    self.stats.update(datapoint)

                    # Move ping_time forward by the instances check_interval
                    ping_time = ping_time + datetime.timedelta(
                        seconds=self.check_interval
                    )

                else:
                    await asyncio.sleep(1)

    async def ping_url(self, client, url) -> None:
        """
        Responsible for making a single reauest to
        self.url and updating self.stats with the
        results

        PARAMETERS: None
        RETURNS: None
        """
        return await client.get(url, timeout=None)

