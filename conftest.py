import pytest
from web_stats import WebStat
from website import Website
from collections import deque
import datetime

"""
Fixtures
"""


@pytest.fixture
def empty_datapoints_gen():
    """Returns a an empty generator built from a deque obj"""
    datapoints = deque()
    return (i for i in datapoints)


@pytest.fixture
def empty_datapoints_data_points_deque():
    """Returns a an empty generator built from a deque obj"""
    datapoints = deque()
    return datapoints


@pytest.fixture
def WebStat_2mins():
    """Returns a 2 minute observation window webstat"""
    return WebStat(max_observation_window=120)


@pytest.fixture
def datapoint():
    """Returns a 2 minute observation window webstat"""
    return {"response_code": 200, "response_time": 0.05}


@pytest.fixture
def WebStat_2mins_datapoints_25():
    """Returns 25 datapoints"""
    WebStat_2mins = WebStat(2)

    for i in range(24):
        WebStat_2mins.update({"response_code": 200, "response_time": 0.05})

    # Last datapoint increases avg
    WebStat_2mins.update(({"response_code": 200, "response_time": 1}))

    return WebStat_2mins


@pytest.fixture(scope="session")
def datetimes_dict(year=2019, month=11, day=25, hour=23, minute=44, second=33):

    threshold = datetime.datetime(year, month, day, hour, minute, second)

    d = {
        "minus_10": threshold + datetime.timedelta(minutes=-10),
        "minus_2": threshold + datetime.timedelta(minutes=-2),
        "threshold": threshold,
        "plus_2": threshold + datetime.timedelta(minutes=2),
        "plus_10": threshold + datetime.timedelta(minutes=10),
        "now": datetime.datetime.now(),
        "now_minus_2": datetime.datetime.now() + datetime.timedelta(minutes=-2)
    }

    return d


@pytest.fixture(scope="session")
def website():
    """Returns a an empty generator built from a deque obj"""
    website = Website(url="http://google.com", check_interval=5)
    return website


