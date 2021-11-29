# Zendesk Ticket Viewer

## Requirements

The CLI requires `Python 3.8.10`.

## How to run

1. Clone the repository using `git clone https://github.com/ishchhabra/zendesk_takehome`

2. Install dependencies using `pip install -r requirements.txt`

3. To run the CLI, use the following command:

   ```sh
   python -m src.ticket_viewer.main_menu
   ```

   Alternatively, the single_ticket and all_tickets sub-modules could be accessed directly
   with `src.ticket_viewer.all_tickets.cli` and `src.ticket_viewer.single_ticket.cli`
