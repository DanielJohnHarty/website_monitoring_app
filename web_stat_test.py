import datetime
import pytest

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
@pytest.mark.parametrize("threshold_seconds_ago, expected", datapoints_since_time_boundary_params)
def test_get_datapoints_since_time_boundary(WebStat_2mins, datetimes_dict, threshold_seconds_ago, expected):

    for i in ["now_minus_10", "now_minus_2", "now", "now_plus_2", "now_plus_10"]:
        WebStat_2mins.data_points.append(
            {
                "response_code": 200,
                "response_time": 0.05,
                "received_at": datetimes_dict[i],
            }
        )

    func_results = list(WebStat_2mins.get_datapoints_since_time_boundary(threshold_seconds_ago))
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
