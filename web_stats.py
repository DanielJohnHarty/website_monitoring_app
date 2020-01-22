from collections import deque
import datetime


class WebStat:
    """
    WebStat holds enough datapoints to report on
    the maximum observation window (default is -600 seconds
    i.e. 10 minutes ago).

    Provides methods to generate statistics and a coroutine
    which acts as a state machine, returning warnings if
    certain conditions are met.
    """

    def __init__(self, max_observation_window: int = -600):
        """
        PARAMETERS:
        max_observation_window:
            A negative integer representing the number of seconds
            of historical datapoints should be kept in self.data_points.

            Defaults to 10 minutes.
        """
        self.data_points = deque()
        self.mandatory_datapoint_keys = {"response_time", "response_code"}
        self.max_observation_window = max_observation_window
        self.alert_coro = self.get_alert_coro()

    def get_alert_coro(self):
        """
        Returns a primed alert coroutine.
        """
        alert_generator = self.alert_generator()
        next(alert_generator)
        return alert_generator

    def alert_generator(self):
        """
        Receives availability values as floats.
        Calculates whether received availability
        should trigger an alert message to be sent 
        back to the caller.

        Condition 1:
        If availability is less than 80% for at least 2
        minutes, send an alert that the site is down.

        Condition 2:
        If a down website is at 80% or more availability
        for at least 2 minutes, send an alert that is is
        no longer down.
        """

        # No alert exists yet
        alert = None

        # Set to True after condition 1
        awaiting_recovery = False

        # Tracks time in a particular state
        in_state_since = datetime.datetime.now()

        # Is availability higher than 80%
        site_available = None

        is_available = lambda availability_pct: availability_pct >= 0.8

        while True:
            # % value. Sent to the coroutine as a float
            # The previous cycle's alert is yielded back to the caller
            latest_availability = yield alert

            # Reset alert to None each loop
            alert = None

            # Did the state change since last time?
            availability_state_change = site_available != is_available(
                latest_availability
            )

            # Reset each time state changes
            if availability_state_change:
                in_state_since = datetime.datetime.now()

            site_available = is_available(latest_availability)

            time_in_state = datetime.datetime.now() - in_state_since

            more_than_2_minutes_in_state = time_in_state.seconds > 120

            # Condition 1
            if (
                not site_available
                and more_than_2_minutes_in_state
                and not awaiting_recovery
            ):
                alert = f"Site is down {datetime.datetime.now()}"
                awaiting_recovery = True

            # Condition 2
            if site_available and more_than_2_minutes_in_state and awaiting_recovery:
                alert = f"Site is back {datetime.datetime.now()}"
                awaiting_recovery = False

    def get_datapoints_since_time_boundary(self, threshold_seconds_ago: int):
        """
        Generator function. Yields one by one only the values from
        self.data_points which are within the time_boundary parameter

        PARAMETERS: time_boundary: In seconds. Yields only 
                    datapoints received no more than this number of 
                    seconds ago.
        RETURNS: None
        YIELDS: datapoint dictionaries
        """
        for datapoint in self.data_points:

            datapoint_too_old = self.is_older_than_threshold(
                datapoint["received_at"], threshold_seconds_ago=threshold_seconds_ago
            )

            if not datapoint_too_old:
                yield datapoint

    def get_max_response_time(self, threshold_seconds_ago: int):
        """
        Iterates over datapoints finding and returning the max response time.

        PARAMETERS: threshold_seconds_ago: Include data since this number of seconds
        RETURNS: float
        """
        timebound_datapoints = self.get_datapoints_since_time_boundary(
            threshold_seconds_ago
        )

        max_response_time = None

        for dp in timebound_datapoints:

            if max_response_time:
                max_response_time = max(dp["response_time"], max_response_time)
            else:
                max_response_time = dp["response_time"]

        return max_response_time

    def get_avg_response_time(self, threshold_seconds_ago: int) -> datetime.timedelta:
        """
        Iterates over datapoints building average response time.

        PARAMETERS: threshold_seconds_ago: Negative integer representing
                    to number of seconds ago from which to include data_points

        RETURNS: datetime.timedelta
        """
        timebound_datapoints = self.get_datapoints_since_time_boundary(
            threshold_seconds_ago
        )
        response_time_sum = None
        datapoint_count = 0
        avg_response_time = None

        for dp in timebound_datapoints:
            datapoint_count += 1

            if response_time_sum:
                response_time_sum += dp["response_time"]
            else:
                response_time_sum = dp["response_time"]

        try:
            avg_response_time = response_time_sum / datapoint_count
        except (ZeroDivisionError, TypeError):
            avg_response_time = None

        return avg_response_time

    def get_availability(self, threshold_seconds_ago: int):
        """
        Iterates over datapoints. Where response_codes are equal to 200
        the website is considered to be available. In any other case 
        the website is considered that the website is down.

        PARAMETERS: threshold_seconds_ago: Include data since this number of seconds
        RETURNS: float
        """
        timebound_datapoints = self.get_datapoints_since_time_boundary(
            # datapoint_datetime=datetime.datetime.now(),
            threshold_seconds_ago=threshold_seconds_ago
        )
        available_count = 0
        datapoint_count = 0

        for dp in timebound_datapoints:
            if dp["response_code"] == 200:
                available_count += 1

            datapoint_count += 1

        try:
            availability = available_count / datapoint_count
        except ZeroDivisionError:
            availability = None

        return availability

    def update(self, new_datapoint: dict):
        """
        Adds received datapoint and pops datapoints outside the 
        max_observed_time.

        PARAMETERS: new_datapoint
        RETURNS: None
        """
        self.add_new_datapoint(new_datapoint)

        if self.data_points:
            self.pop_old_datapoints()

    def add_new_datapoint(self, new_datapoint: dict):
        """
        Checks passed datapoint for compilence with Stat class
        mandatory_datapoint_keys. Adds a 'received_at' datetime object
        and appends to datapoints if all correct, else raises exception.

        PARAMETERS:
            new_datapoint: dictionary like obj with 
            'response_time' and 'response_code' keys
        RETURNS: None
        """

        # Only accepts complient datapoints
        correct_structure = self.mandatory_datapoint_keys == set(new_datapoint)

        if correct_structure:

            new_datapoint["received_at"] = datetime.datetime.now()
            self.data_points.append(new_datapoint)

        else:
            raise Exception(
                "Datapoint does not compy with "
                + "Stat classes mandatory_datapoint_keys"
            )

    def is_older_than_threshold(
        self, datapoint_datetime: datetime, threshold_seconds_ago: int = None
    ):
        """
        Returns True if passed parameter falls outside time peridod
        defined by the threshold_minutes_ago parameter. 
        If the threshold_minutes_ago parameter is not passed,
        the class instance's max_observed_time is used as the threshold.

        PARAMETERS: datapoint_datetime
        RETURNS: bool
        """
        if not threshold_seconds_ago:
            threshold_seconds_ago = self.max_observation_window

        now = datetime.datetime.now()
        threshold = now + datetime.timedelta(seconds=threshold_seconds_ago)
        out_of_time_bounds = datapoint_datetime < threshold
        return out_of_time_bounds

    def pop_old_datapoints(self):
        """
        Iterate over the self.data_points from
        the left (i.e. oldest first), popping those whose 'received_at'
        value is older than the calculated time boundary

        PARAMETERS: None
        RETURNS: None
        """

        while self.is_older_than_threshold(self.data_points[0]["received_at"]):
            self.data_points.popleft()

    def get_updated_stats(self, timeframe):

        updated_stats = {
            "availability": self.get_availability(timeframe),
            "avg_response_time": self.get_avg_response_time(timeframe),
            "max_response_time": self.get_max_response_time(timeframe),
        }

        return updated_stats
