import pytest
from website import Website


def test_bad_url_on_init_raises_exception():

    with pytest.raises(Exception):
        website = Website()
