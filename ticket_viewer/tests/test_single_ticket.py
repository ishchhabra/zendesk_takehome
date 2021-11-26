import io
from contextlib import redirect_stdout

import pytest
import ticket_viewer.single_ticket.cli as single_ticket


def test_get_ticket(mock_responses):
    ticket = single_ticket._get_ticket(1)
    assert ticket["id"] == 1

    with pytest.raises(AssertionError):
        single_ticket._get_ticket(2)  # The fixture has status_code 404 for ticket ID 2.


def test_pretty_print():
    with io.StringIO() as buf, redirect_stdout(buf):
        single_ticket._pretty_print("Key", 5, "Value", 10)
        assert buf.getvalue().strip("\n") == "Key   : Value     "
