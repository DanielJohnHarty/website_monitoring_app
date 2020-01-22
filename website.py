import httpx
import datetime
from web_stats import WebStat
import asyncio
from console_writer import ConsoleWriter
from console_writer import WebPerformanceDashboard


class Website:
    def __init__(self, url=None, check_interval=None, max_observation_window=-600):
        """
        PARAMETERS: url: String. Must include protocol prefix e.g. http://
        """
        # Both raise exceptions if not compliant
        self.validate_url(url)
        self.validate_check_interval(check_interval)
        self.url = url
        self.check_interval = check_interval
        self.stats = WebStat(max_observation_window)
        self.dashboard = WebPerformanceDashboard()

    def validate_url(self, url):
        try:
            _ = httpx.get(url)
        except Exception:
            raise Exception("URL error")

    def validate_check_interval(self, check_interval: int):
        """
        Check_interval must be a +ve integer
        """
        if check_interval < 1:
            raise Exception("check_interval must be a positive integer")

    def update_alert_process(self, availability: float):
        """
        Takes as availability % and sends it to the self.stats Stat
        instance. An alert will be returned if alert criteria are triggered

        RETURNS: String or None
        """
        # Don't send a None value
        # but 0.0 is ok
        if availability is not None:
            alert = self.stats.alert_coro.send(availability)
            if alert:
                # Alerts are saved to the dashboard
                self.dashboard.persisted_messages.append(alert)

    async def produce_report(self, timeframe: int, writer: ConsoleWriter):
        """
        Retrieves updated stats from the self.stats instance
        and forwards to the ConsoleWriter instance writer
        for formatting before writing to the console

        PARAMETERS: timeframe: In seconds as int e.g. 
                              -60 datapoints from previous minute
                              writer: ConsoleWriter instance responsible 
                              formatting reports and writing to the console
        """

        updated_stats = self.stats.get_updated_stats(timeframe=timeframe)
        updated_stats["url"] = self.url
        timestamp = datetime.datetime.now().strftime("%c")  # Local time format
        updated_stats["timestamp"] = timestamp
        updated_stats["timeframe"] = timeframe

        self.dashboard.data = updated_stats

        # Adds alert message if needed
        self.update_alert_process(updated_stats["availability"])

        # Outputs all dashboards attached to the writer
        writer.write_dashboards_to_console()
        await asyncio.sleep(0)

    async def update(self):
        r = await self.ping_url(self.url)
        datapoint = {"response_code": r.status_code, "response_time": r.elapsed}
        # Only updating stats here.
        # No query until reports are generated.
        self.stats.update(datapoint)

    async def periodic_data_update_process(self):
        """
        Simply updates stats every check interval period
        """
        while True:
            await asyncio.sleep(self.check_interval)
            await asyncio.create_task(self.update())

    async def periodic_report_production_process(
        self, frequency: int, timeframe: int, writer: ConsoleWriter
    ):
        """
        Coroutine to schedule a report every {frequency} seconds
        using data over the last {timeframe} minutes.

        PARAMETERS: frequency and timeframe fixed for challenge
                    but can be changed in 
                    website_monitoring_application instantiation
        """
        while True:
            await asyncio.sleep(frequency)
            await asyncio.create_task(self.produce_report(timeframe, writer))

    async def all_async_tasks(self, schedules: dict, writer: ConsoleWriter):
        """
        A coroutine pulling update and reporting tasks from the queues.

        schedules are dicts with the following format:

            schedule1 = {"frequency": 10, "timeframe": -600}
            schedule2 = {"frequency": 60, "timeframe": -60 * 60}

        Fixed for the challenge.
        """
        # Every Website instance shares the same writer instance
        self.writer = writer

        # Data update process
        coros = [self.periodic_data_update_process()]

        # Adds task for each scheduled report
        for schedule in schedules:

            freq = schedule["frequency"]
            timef = schedule["timeframe"]

            coros.extend(
                [
                    # Reporting Process
                    self.periodic_report_production_process(freq, timef, writer)
                ]
            )

        await asyncio.gather(*coros)

    async def ping_url(self, url) -> None:
        """
        Responsible for making a single request to
        self.url after the delay and returning
        the response

        PARAMETERS: delay:int, how many seconds to 
                    wait until execution
                    client: httpx session object
                    url: url to ping
        RETURNS: httpx reauest response object
        """
        async with httpx.AsyncClient() as client:
            return await client.get(url, timeout=None)
