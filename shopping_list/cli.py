from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser, Namespace
from pathlib import Path

from loguru import logger

from . import __version__ as VERSION
from .items import ItemManager
from .log import setup_logging

HELP_FORMATTER = ArgumentDefaultsHelpFormatter


def parse_args() -> Namespace:
    parser = ArgumentParser("shopping-list-cli", formatter_class=HELP_FORMATTER)
    parser.add_argument("--version", action="version", version=VERSION)
    parser.add_argument("-q", "--quiet", action="store_true", help="Log less")
    parser.add_argument("-d", "--debug", action="store_true", help="Log more")
    parser.add_argument(
        "-l",
        "--log-root",
        help="Log root path (specify '' to suppress logging to a file)",
        type=lambda s: Path(s) if s else None,
        metavar="PATH",
        default="logs",
    )
    parser.add_argument(
        "-i",
        "--db-file",
        help="Input file",
        type=Path,
        metavar="PATH",
        default="~/.local/state/shopping-list.db",
    )
    parser.add_argument("-c", "--closed", action="store_true", help="Show closed items too")

    commands = parser.add_subparsers(
        dest="command", required=False, description="If no command specified, only list items"
    )

    parse_command = commands.add_parser(
        "add",
        formatter_class=HELP_FORMATTER,
        help="Add item(s)",
        description="Add item(s) to shopping list",
    )
    parse_command.add_argument(
        "item",
        help="Item title",
        nargs="+",
    )

    parse_command = commands.add_parser(
        "done",
        formatter_class=HELP_FORMATTER,
        help="Close item(s)",
        description="Mark item(s) as done",
    )
    parse_command.add_argument(
        "item",
        help="Item ID as returned from list",
        nargs="+",
    )

    parse_command = commands.add_parser(
        "rm",
        formatter_class=HELP_FORMATTER,
        help="Delete item(s)",
        description="Delete item(s) from shopping list",
    )
    parse_command.add_argument(
        "item",
        help="Item ID as returned from list",
        nargs="+",
    )

    return parser.parse_args()


def cli() -> None:
    args = parse_args()
    setup_logging(args)
    logger.debug("args={}", args)
    # handle the args
    manager = ItemManager(args)
    return manager.dispatch()
