import pytest

DASHBOARD_WIDTH = 50


# Input, Expected
params = [
    ("http://google.com", DASHBOARD_WIDTH, True),
    ("https://docs.python.org", DASHBOARD_WIDTH, True),
    ("http://google.com", DASHBOARD_WIDTH, False),
    ("https://docs.python.org", DASHBOARD_WIDTH, False),
]


@pytest.mark.parametrize("input, expected_len, close_lines", params)
def test_console_writer_format_line_pads_and_closes_correctly(
    console_writer, input, expected_len, close_lines
):
    actual = console_writer.format_line(
        input, close_lines, pad_lines=True, max_length=DASHBOARD_WIDTH
    )

    assert len(actual) == expected_len

    if close_lines:
        assert actual[0] == "|" and actual[-1] == "|"
