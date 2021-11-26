import io
from contextlib import redirect_stdout

import ticket_viewer.all_tickets.cli as all_tickets
from ticket_viewer.constants.config import ZENDESK_SUBDOMAIN


def test_get_tickets(mock_responses):
    state_obj = {}

    tickets = all_tickets._get_tickets(
        state_obj,
        f"{ZENDESK_SUBDOMAIN}/api/v2/tickets_1",  # tickets_1 is a custom URL for testing.
    )

    assert state_obj["previous_page_url"] is None
    assert state_obj["next_page_url"] is None
    assert len(tickets) == 2


def test_print_tickets():
    with io.StringIO() as buf, redirect_stdout(buf):
        all_tickets._print_tickets(
            [
                {
                    "id": 1,
                    "created_at": "2021-11-19T20:08:24Z",
                    "requester_id": 422048676431,
                    "subject": "Subject",
                }
            ]
        )

        assert (
            buf.getvalue().strip()
            == "Ticket #1 with subject 'Subject' opened by 422048676431 on 19 November, 2021 20:08:24"
        )


def test_prev():
    with io.StringIO() as buf, redirect_stdout(buf):
        all_tickets.prev(obj={"previous_page_url": None}, standalone_mode=False)
        assert buf.getvalue().strip() == "You are already on the first page."


def test_next():
    with io.StringIO() as buf, redirect_stdout(buf):
        all_tickets.prev(obj={"next_page_url": None}, standalone_mode=False)
        assert buf.getvalue().strip() == "You are already on the last page."