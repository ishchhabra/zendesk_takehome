from datetime import datetime
from typing import Any, Dict

import click
from requests import get
from ticket_viewer.all_tickets.constants import config as at_config
from ticket_viewer.constants.config import (
    AGENT_EMAIL,
    API_TOKEN,
    CLI_DATETIME_FORMAT,
    ZENDESK_DATETIME_FORMAT,
    ZENDESK_SUBDOMAIN,
)


@click.group(invoke_without_command=True)
@click.pass_obj
def cli(state):
    tickets = _get_tickets(state, state["start_url"])
    _print_tickets(tickets)
    _print_options()

    while True:
        option = click.prompt(
            "Enter your input",
            type=click.Choice(list(cli.commands.keys()) + ["main"]),
        )

        print("")

        if option == "main":
            break
        else:
            cli.commands[option](obj=state, standalone_mode=False)
    pass


@cli.command(name="next")
@click.pass_obj
def next_page(state):
    if state["next_page_url"] is None:
        print("[ERROR] You are already on the last page.")
        print("")
    else:
        tickets = _get_tickets(state, state["next_page_url"])
        _print_tickets(tickets)
        _print_options()


@cli.command(name="prev")
@click.pass_obj
def prev_page(state):
    if state["previous_page_url"] is None:
        print("[ERROR] You are already on the first page.")
        print("")
    else:
        tickets = _get_tickets(state, state["previous_page_url"])
        # breakpoint()
        _print_tickets(tickets)
        _print_options()


def _get_tickets(state_obj, tickets_url: str) -> Dict:
    resp = get(tickets_url, auth=(f"{AGENT_EMAIL}/token", API_TOKEN))
    assert resp.status_code == 200, {
        "error": resp.status_code,
        "description": resp.text,
    }

    resp = resp.json()

    state_obj["next_page_url"] = resp["next_page"]
    state_obj["previous_page_url"] = resp["previous_page"]

    return resp["tickets"]


def _print_tickets(tickets: Dict):
    for ticket in tickets:
        print(
            "Ticket #{id} with subject '{subject}' opened by {requester_id} on {created_at}".format(
                id=ticket["id"],
                subject=ticket["subject"],
                requester_id=ticket["requester_id"],
                created_at=datetime.strptime(
                    ticket["created_at"], ZENDESK_DATETIME_FORMAT
                ).strftime(CLI_DATETIME_FORMAT),
            )
        )


def _print_options():
    print(
        """
To view the next page, type 'next'
To view the previous page, type 'prev'
To return to the main menu, type 'main'
    """
    )


def main():
    cli(
        obj={
            "start_url": f"{ZENDESK_SUBDOMAIN}/api/v2/tickets?per_page={at_config.TICKETS_PER_PAGE}",
            "next_page_url": None,
            "previous_page_url": None,
        },
        standalone_mode=False,
    )


if __name__ == "__main__":
    main()
