"""
Fixtures in conftest.py
"""


# Average
def test_get_avg_response_time_with_no_datapoints_returns_None(WebStat_2mins):
    assert WebStat_2mins.get_avg_response_time(60) is None


def test_get_avg_response_time_with_1_datapoint_returns_same_value(
    WebStat_2mins, datapoint
):
    expected = datapoint["response_time"]
    WebStat_2mins.update(datapoint)
    assert WebStat_2mins.get_avg_response_time(60) == expected


def test_get_avg_response_time_correct(WebStat_2mins_datapoints_25):
    wb_2_25 = WebStat_2mins_datapoints_25
    assert wb_2_25.get_avg_response_time(60) > 0.05


# Max
def test_get_max_response_time_correct(WebStat_2mins_datapoints_25):
    assert WebStat_2mins_datapoints_25.get_max_response_time(60) == 1


def test_get_max_response_time_returns_none_if_no_datapoints(WebStat_2mins):
    assert WebStat_2mins.get_max_response_time(60) is None


# Availability
def test_get_availability_returns_none_if_no_datapoints(WebStat_2mins):
    assert WebStat_2mins.get_availability(60) is None


"""
Datetime comparisons
"""


def test_is_older_than_threshold_when_true(WebStat_2mins, datetimes_dict):

    expected = True
    actual = WebStat_2mins.is_older_than_threshold(
        datapoint_datetime=datetimes_dict["minus_2"], threshold_seconds_ago=125
    )

    assert expected == actual


def test_is_not_older_than_threshold_when_not(WebStat_2mins, datetimes_dict):

    expected = False
    actual = WebStat_2mins.is_older_than_threshold(
        datapoint_datetime=datetimes_dict["now"], threshold_seconds_ago=100
    )

    assert expected == actual
