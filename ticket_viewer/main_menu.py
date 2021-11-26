import click
import ticket_viewer.all_tickets.cli as all_tickets
import ticket_viewer.single_ticket.cli as single_ticket


@click.group(invoke_without_command=True)
def cli():
    while True:
        option = click.prompt(
            "Enter your input",
            type=click.Choice(list(cli.commands.keys()) + ["exit"]),
        )

        print("")  # For formatting

        if option == "exit":
            break
        else:
            cli.commands[option](standalone_mode=False)


# @click.pass_context
# def help(ctx):
#     print()
#     breakpoint()


@cli.command(name="all_tickets")
def all_tickets_cmd():
    all_tickets.main()


@cli.command(name="single_ticket")
def single_ticket_cmd():
    single_ticket.main()


def main():
    cli(standalone_mode=False)


if __name__ == "__main__":
    main()
