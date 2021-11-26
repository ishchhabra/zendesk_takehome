from typing import *

import click
from requests import get
from ticket_viewer.constants.config import AGENT_EMAIL, API_TOKEN, ZENDESK_SUBDOMAIN
from ticket_viewer.single_ticket.constants import config as st_config


@click.group(invoke_without_command=True)
def cli():
    while True:
        ticket_number = click.prompt("Enter your ticket number", type=int)

        print("")  # For formatting

        ticket = _get_ticket(ticket_number)
        _print_ticket(ticket)

        choice = click.confirm("Do you want to view another ticket?")

        print("")  #  For formatting

        if choice is False:
            break


def _get_ticket(ticket_number: int):
    resp = get(
        f"{ZENDESK_SUBDOMAIN}/api/v2/tickets/{ticket_number}",
        auth=(f"{AGENT_EMAIL}/token", API_TOKEN),
    )
    assert resp.status_code == 200, {
        "error": resp.status_code,
        "description": resp.text,
    }

    return resp.json()["ticket"]


def _print_ticket(ticket: Dict[str, str]):
    pretty_print(
        "ID",
        st_config.MAX_KEY_LENGTH,
        str(ticket["id"]),
        st_config.MAX_VALUE_LENGTH,
    )

    pretty_print(
        "Subject",
        st_config.MAX_KEY_LENGTH,
        ticket["subject"],
        st_config.MAX_VALUE_LENGTH,
    )

    pretty_print(
        "Requested",
        st_config.MAX_KEY_LENGTH,
        ticket["created_at"],
        st_config.MAX_VALUE_LENGTH,
    )

    pretty_print(
        "Updated",
        st_config.MAX_KEY_LENGTH,
        ticket["updated_at"],
        st_config.MAX_VALUE_LENGTH,
    )

    pretty_print(
        "Message",
        st_config.MAX_KEY_LENGTH,
        ticket["description"].replace(
            "\n", "\n" + " " * (st_config.MAX_KEY_LENGTH + 3)
        ),
        st_config.MAX_VALUE_LENGTH_DESCRIPTION,
    )


def pretty_print(key: str, key_len: int, value: str, value_len: int):
    print(
        "{key:<{key_len}} : {value:{value_len}}".format(
            key=key[:key_len],
            key_len=key_len,
            value=value[:value_len],
            value_len=value_len,
        )
    )


# Getting too complicated for a very simple task.
#
# def _get_min_valid_lengths(ticket, key_repr_map: Dict[str, str]):
#     min_key_length, min_value_length = 0, 0
#     for key, key_repr in key_repr_map.items():
#         assert key in ticket, f"Invalid key {key}"

#         min_key_length = min(max(key_repr, len(key)), st_config.MAX_KEY_LENGTH)
#         min_value_length = min(
#             max(min_value_length, len(ticket["key"])), st_config.MAX_VALUE_LENGTH
#         )

#     return min_key_length, min_value_length


def main():
    cli(standalone_mode=False)


if __name__ == "__main__":
    main()
