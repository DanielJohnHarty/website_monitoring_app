import pytest
from website import Website


def test_bad_url_on_init_raises_exception():

    with pytest.raises(Exception):
        website = Website()


relative_date_params = [
    ("minus_2", -120),
    ("minus_10", -600),
    ("plus_2", 120),
    ("plus_10", 600),
    ("threshold", 0),
]
@pytest.mark.parametrize("expected,timedelta", relative_date_params)
def test_get_relative_datetime(website, datetimes_dict, expected, timedelta):

    expected = datetimes_dict[expected]

    actual = website.get_relative_datetime(
        reference_datetime=datetimes_dict["threshold"],
        timedelta_in_seconds=timedelta
    )

    assert expected == actual
