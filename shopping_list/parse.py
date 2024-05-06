from argparse import Namespace

from loguru import logger


def parse(args: Namespace) -> None:
    logger.info("Parse command, args={}", args)
