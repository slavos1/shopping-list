from argparse import Namespace

from loguru import logger


def report(args: Namespace) -> None:
    logger.info("Dump command, args={}", args)
