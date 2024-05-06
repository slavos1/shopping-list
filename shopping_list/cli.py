from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser, Namespace
from pathlib import Path

from loguru import logger

from . import __version__ as VERSION
from .log import setup_logging
from .parse import parse
from .report import report

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
        "--input-file",
        help="Input file",
        type=Path,
        metavar="PATH",
        required=True,
    )

    commands = parser.add_subparsers(dest="command", required=True)

    parse_command = commands.add_parser(
        "parse",
        formatter_class=HELP_FORMATTER,
        help="Parse data",
        description="Parse data from input",
    )
    parse_command.add_argument(
        "-o",
        "--output-file",
        help="Output file",
        type=Path,
        metavar="PATH",
        required=True,
    )

    report_command = commands.add_parser(
        "report",
        formatter_class=HELP_FORMATTER,
        help="Make report",
        description="Make report from data produced by 'parse'",
    )
    report_command.add_argument(
        "-o",
        "--output-dir",
        help="Output directory",
        type=Path,
        metavar="PATH",
        required=True,
    )

    return parser.parse_args()


DISPATCH = {
    "parse": parse,
    "report": report,
}


def cli() -> None:
    args = parse_args()
    setup_logging(args)
    logger.debug("args={}", args)
    # handle the args
    DISPATCH[args.command](args)
