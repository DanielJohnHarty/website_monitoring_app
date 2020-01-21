import pytest
import itertools
from web_stats import WebStat
from console_writer import ConsoleWriter, WebPerformanceDashboard
from website import Website
from collections import deque
import datetime

"""
Fixtures
"""


@pytest.fixture
def console_writer():
    """Returns a ConsoleWriter obj with 1 db"""
    console_writer = ConsoleWriter()

    db = WebPerformanceDashboard()
    db.data = {
        "url": "https://learning.oreilly.com/home/",
        "availability": 0.9285714285714286,
        "avg_response_time": datetime.timedelta(seconds=0.92),
        "max_response_time": datetime.timedelta(seconds=1.24),
    }
    console_writer.add_dashboard(db)

    return console_writer


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
    return WebStat(max_observation_window=-120)


@pytest.fixture
def WebStat_25mins():
    """Returns a 2 minute observation window webstat"""
    return WebStat(max_observation_window=-1500)


@pytest.fixture
def datapoint():
    """Returns a 2 minute observation window webstat"""
    return {"response_code": 200, "response_time": 0.05}


@pytest.fixture
def WebStat_2mins_datapoints_25():
    """Returns 25 datapoints"""
    WebStat_2mins = WebStat(-600)

    for i in range(24):
        WebStat_2mins.update({"response_code": 200, "response_time": 0.05})

    # Last datapoint increases avg
    WebStat_2mins.update({"response_code": 200, "response_time": 1})

    return WebStat_2mins


@pytest.fixture
def WebStat_10mins_balanced_datapoints(datetimes_dict):
    """Returns a 10 min max observation time webstat"""
    WebStat_2mins = WebStat(600)

    # Manually add to force average
    for dt_key, response_time in [
        ("minus_10", -10.5),
        ("minus_2", -2.5),
        ("plus_2", 2.5),
        ("plus_10", 10.5),
    ]:

        WebStat_2mins.data_points.append(
            {
                "response_code": 200,
                "response_time": response_time,
                "received_at": datetimes_dict[dt_key],
            }
        )

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
        "now_minus_2": datetime.datetime.now() + datetime.timedelta(minutes=-2),
        "now_minus_10": datetime.datetime.now() + datetime.timedelta(minutes=-10),
        "now": datetime.datetime.now(),
        "now_plus_2": datetime.datetime.now() + datetime.timedelta(minutes=2),
        "now_plus_10": datetime.datetime.now() + datetime.timedelta(minutes=10),
    }

    return d


@pytest.fixture(scope="session")
def website():
    """Returns a an empty generator built from a deque obj"""
    website = Website(url="http://google.com", check_interval=5)
    return website


@pytest.fixture
def WebStat_10mins_recent_datapoints(datetimes_dict):
    """Returns 25 datapoints"""
    ws = WebStat(600)

    for k in ["now_minus_2", "now_minus_10", "now_plus_2", "now_plus_10"]:

        ws.data_points.append(
            {
                "response_code": 200,
                "response_time": 0.05,
                "received_at": datetimes_dict[k],
            }
        )

    # Last datapoint increases avg
    ws.data_points.append(
        {
            "response_code": 200,
            "response_time": 1.5,
            "received_at": datetimes_dict["now"],
        }
    )

    return ws
