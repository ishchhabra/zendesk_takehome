import io
from contextlib import redirect_stdout

import ticket_viewer.all_tickets.cli as all_tickets
from ticket_viewer.constants.config import ZENDESK_SUBDOMAIN


def test_get_tickets(mock_responses):
    state_obj = {}

    tickets = all_tickets._get_tickets(
        state_obj,
        f"{ZENDESK_SUBDOMAIN}/api/v2/tickets_1?per_page=25",
    )

    assert state_obj["previous_page_url"] is None
    assert state_obj["next_page_url"] is None
    assert len(tickets) == 2


def test_print_tickets():
    with io.StringIO() as buffer, redirect_stdout(buffer):
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
            buffer.getvalue().strip()
            == "Ticket #1 with subject 'Subject' opened by 422048676431 on 19 November, 2021 20:08:24"
        )


def test_prev_page(mock_responses):

    with io.StringIO() as buffer, redirect_stdout(buffer):
        state = {"previous_page_url": None, "current_page_number": 100}
        all_tickets.prev_page(
            obj=state,
            standalone_mode=False,
        )

        assert buffer.getvalue().strip() == "[ERROR] You are already on the first page."
        assert state["current_page_number"] == 100

        buffer.truncate(0)
        buffer.seek(0)

        state = {
            "previous_page_url": f"{ZENDESK_SUBDOMAIN}/api/v2/tickets_1?per_page=25",
            "current_page_number": 100,
        }
        all_tickets.prev_page(
            obj=state,
            standalone_mode=False,
        )

        # Notice the (99/1). The current page number is just a counter without any additional checks!
        assert (
            buffer.getvalue().strip()
            == "Ticket #1 with subject 'Sample ticket: Meet the ticket' opened by 422048676431 on 19 November, 2021 20:08:24\nTicket #2 with subject 'velit eiusmod reprehenderit officia cupidatat' opened by 422048674091 on 19 November, 2021 20:24:27\n\nPage (99/1)\n        \n\nTo view the next page, type 'next'\nTo view the previous page, type 'prev'\nTo return to the main menu, type 'main'"
        )
        assert state["current_page_number"] == 99


def test_next_page(mock_responses):
    with io.StringIO() as buffer, redirect_stdout(buffer):
        state = {"next_page_url": None, "current_page_number": 100}
        all_tickets.next_page(obj={"next_page_url": None}, standalone_mode=False)

        assert buffer.getvalue().strip() == "[ERROR] You are already on the last page."
        assert state["current_page_number"] == 100

        buffer.truncate()
        buffer.seek(0)

        state = {
            "next_page_url": f"{ZENDESK_SUBDOMAIN}/api/v2/tickets_1?per_page=25",
            "current_page_number": 100,
        }
        all_tickets.next_page(
            obj=state,
            standalone_mode=False,
        )

        assert (
            buffer.getvalue().strip()
            == "Ticket #1 with subject 'Sample ticket: Meet the ticket' opened by 422048676431 on 19 November, 2021 20:08:24\nTicket #2 with subject 'velit eiusmod reprehenderit officia cupidatat' opened by 422048674091 on 19 November, 2021 20:24:27\n\nPage (101/1)\n        \n\nTo view the next page, type 'next'\nTo view the previous page, type 'prev'\nTo return to the main menu, type 'main'"
        )
        assert state["current_page_number"] == 101
