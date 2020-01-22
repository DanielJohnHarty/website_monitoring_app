import datetime
import pytest
from freezegun import freeze_time
import asyncio

"""
Fixtures in conftest.py
"""


# Average
def test_get_avg_response_time_with_no_datapoints_returns_None(WebStat_2mins):
    assert WebStat_2mins.get_avg_response_time(-60) is None


def test_get_avg_response_time_with_1_datapoint_returns_same_value(
    WebStat_25mins, datapoint
):
    expected = datapoint["response_time"]
    WebStat_25mins.update(datapoint)
    assert WebStat_25mins.get_avg_response_time(-60 * 25) == expected


def test_get_avg_response_time_correct(WebStat_2mins_datapoints_25):
    wb_2_25 = WebStat_2mins_datapoints_25
    assert wb_2_25.get_avg_response_time(-60) > 0.05


# Max
def test_get_max_response_time_correct(WebStat_10mins_recent_datapoints):
    expected = 1.5
    actual = WebStat_10mins_recent_datapoints.get_max_response_time(-60000)
    assert expected == actual


def test_get_max_response_time_returns_none_if_no_datapoints(WebStat_2mins):
    assert WebStat_2mins.get_max_response_time(60) is None


# Availability
def test_get_availability_returns_none_if_no_datapoints(WebStat_2mins):
    assert WebStat_2mins.get_availability(60) is None


"""
Datetime comparisons
"""


datapoints_since_time_boundary_params = [
    (-120, 3),
    (-700, 5),
    (100, 2),
    (-60, 3),
    (-200, 4),
]


@pytest.mark.parametrize(
    "threshold_seconds_ago, expected", datapoints_since_time_boundary_params
)
def test_get_datapoints_since_time_boundary(
    WebStat_2mins, datetimes_dict, threshold_seconds_ago, expected
):

    for i in ["now_minus_10", "now_minus_2", "now", "now_plus_2", "now_plus_10"]:
        WebStat_2mins.data_points.append(
            {
                "response_code": 200,
                "response_time": 0.05,
                "received_at": datetimes_dict[i],
            }
        )

    func_results = list(
        WebStat_2mins.get_datapoints_since_time_boundary(threshold_seconds_ago)
    )
    actual = len(func_results)
    assert expected == actual


def test_is_older_than_threshold_when_true(WebStat_2mins, datetimes_dict):

    expected = True
    actual = WebStat_2mins.is_older_than_threshold(
        datapoint_datetime=datetimes_dict["minus_2"], threshold_seconds_ago=125
    )

    assert expected == actual


def test_is_not_older_than_threshold_when_not(WebStat_2mins, datetimes_dict):

    expected = False
    actual = WebStat_2mins.is_older_than_threshold(
        datapoint_datetime=datetimes_dict["now"], threshold_seconds_ago=-100
    )

    assert expected == actual


# alert_testing_datetimes
d = {
    "25_0": datetime.datetime(2020, 1, 22, 12, 25, 0),
    "25_1": datetime.datetime(2020, 1, 22, 12, 25, 1),
    "25_30": datetime.datetime(2020, 1, 22, 12, 25, 30),
    "25_31": datetime.datetime(2020, 1, 22, 12, 25, 31),
    "26_0": datetime.datetime(2020, 1, 22, 12, 26, 0),
    "26_1": datetime.datetime(2020, 1, 22, 12, 26, 1),
    "26_30": datetime.datetime(2020, 1, 22, 12, 26, 30),
    "26_31": datetime.datetime(2020, 1, 22, 12, 26, 31),
    "27_0": datetime.datetime(2020, 1, 22, 12, 27, 0),
    "27_1": datetime.datetime(2020, 1, 22, 12, 27, 1),
    "27_30": datetime.datetime(2020, 1, 22, 12, 27, 30),
    "27_31": datetime.datetime(2020, 1, 22, 12, 27, 31),
    "28_0": datetime.datetime(2020, 1, 22, 12, 28, 0),
    "28_1": datetime.datetime(2020, 1, 22, 12, 28, 1),
    "28_30": datetime.datetime(2020, 1, 22, 12, 28, 30),
    "28_31": datetime.datetime(2020, 1, 22, 12, 28, 31),
    "29_0": datetime.datetime(2020, 1, 22, 12, 29, 0),
    "29_1": datetime.datetime(2020, 1, 22, 12, 29, 1),
    "29_30": datetime.datetime(2020, 1, 22, 12, 29, 30),
    "29_31": datetime.datetime(2020, 1, 22, 12, 29, 31),
    "30_0": datetime.datetime(2020, 1, 22, 12, 30, 0),
    "30_1": datetime.datetime(2020, 1, 22, 12, 30, 1),
    "30_30": datetime.datetime(2020, 1, 22, 12, 30, 30),
    "30_31": datetime.datetime(2020, 1, 22, 12, 30, 31),
    "31_0": datetime.datetime(2020, 1, 22, 12, 31, 0),
    "31_1": datetime.datetime(2020, 1, 22, 12, 31, 1),
    "31_30": datetime.datetime(2020, 1, 22, 12, 31, 30),
    "31_31": datetime.datetime(2020, 1, 22, 12, 31, 31),
    "32_0": datetime.datetime(2020, 1, 22, 12, 32, 0),
    "32_1": datetime.datetime(2020, 1, 22, 12, 32, 1),
    "32_30": datetime.datetime(2020, 1, 22, 12, 32, 30),
    "32_31": datetime.datetime(2020, 1, 22, 12, 32, 31),
    "33_0": datetime.datetime(2020, 1, 22, 12, 33, 0),
    "33_1": datetime.datetime(2020, 1, 22, 12, 33, 1),
    "33_30": datetime.datetime(2020, 1, 22, 12, 33, 30),
    "33_31": datetime.datetime(2020, 1, 22, 12, 33, 31),
    "34_0": datetime.datetime(2020, 1, 22, 12, 34, 0),
    "34_1": datetime.datetime(2020, 1, 22, 12, 34, 1),
    "34_30": datetime.datetime(2020, 1, 22, 12, 34, 30),
    "34_31": datetime.datetime(2020, 1, 22, 12, 34, 31),
    "35_0": datetime.datetime(2020, 1, 22, 12, 35, 0),
    "35_1": datetime.datetime(2020, 1, 22, 12, 35, 1),
    "35_30": datetime.datetime(2020, 1, 22, 12, 35, 30),
    "35_31": datetime.datetime(2020, 1, 22, 12, 35, 31),
    "36_0": datetime.datetime(2020, 1, 22, 12, 36, 0),
    "36_1": datetime.datetime(2020, 1, 22, 12, 36, 1),
    "36_30": datetime.datetime(2020, 1, 22, 12, 36, 30),
    "36_31": datetime.datetime(2020, 1, 22, 12, 36, 31),
    "37_0": datetime.datetime(2020, 1, 22, 12, 37, 0),
    "37_1": datetime.datetime(2020, 1, 22, 12, 37, 1),
    "37_30": datetime.datetime(2020, 1, 22, 12, 37, 30),
    "37_31": datetime.datetime(2020, 1, 22, 12, 37, 31),
    "38_0": datetime.datetime(2020, 1, 22, 12, 38, 0),
    "38_1": datetime.datetime(2020, 1, 22, 12, 38, 1),
    "38_30": datetime.datetime(2020, 1, 22, 12, 38, 30),
    "38_31": datetime.datetime(2020, 1, 22, 12, 38, 31),
}


# List of (availability %, datetime) then expected alert result
input_params_alerts_and_persisted_msg_count = [
    ([(1.0, d["25_0"]), (0.79, d["25_30"]), (0.79, d["28_0"])], "site is down", 1),
    (
        [(0.0, d["25_0"]), (0.0, d["27_30"]), (0.85, d["28_0"]), (0.85, d["30_30"])],
        "site is back",
        2,
    ),
    (
        [(0.0, d["25_0"]), (0.0, d["29_30"]), (0.85, d["32_0"]), (0.85, d["34_30"])],
        "site is back",
        2,
    ),
]


@pytest.mark.parametrize(
    "gen_updates, expected_alert, _", input_params_alerts_and_persisted_msg_count
)
def test_alert_generator_alert_expected(WebStat_2mins, gen_updates, expected_alert, _):
    alert = None

    for i in gen_updates:
        av = i[0]
        dt = i[1]

        with freeze_time(dt):
            alert = WebStat_2mins.alert_coro.send(av)

    assert alert.lower().startswith(expected_alert)


@pytest.mark.parametrize(
    "gen_updates, _, expected_num_persisted_msgs",
    input_params_alerts_and_persisted_msg_count,
)
def test_alerts_are_persisted(website, gen_updates, _, expected_num_persisted_msgs):

    for i in gen_updates:
        av = i[0]
        dt = i[1]

        with freeze_time(dt):
            alert = website.update_alert_process(av)

    num_persisted_msgs = len(website.dashboard.persisted_messages)

    assert expected_num_persisted_msgs == num_persisted_msgs


input_params_no_alert_expected = [
    ([(0.0, d["25_0"]), (0.0, d["27_0"])], None),
    ([(1.0, d["30_30"]), (0.0, d["31_0"]), (1.0, d["31_30"]), (0.0, d["32_0"])], None),
]


@pytest.mark.parametrize("gen_updates, expected", input_params_no_alert_expected)
def test_alert_generator_no_alert_expected(WebStat_2mins, gen_updates, expected):

    for i in gen_updates:
        av = i[0]
        dt = i[1]

        with freeze_time(dt):
            alert = WebStat_2mins.alert_coro.send(av)

    assert not alert
