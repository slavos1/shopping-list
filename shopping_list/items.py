from argparse import Namespace
from typing import Any, Dict, Generator, Tuple

from loguru import logger
from peewee import DoesNotExist
from tabulate import tabulate

from .models import MODELS, Item, db_init


class ItemManager:
    def __init__(self, args: Namespace) -> None:
        self.args = args
        self.db = db_init(args.db_file)
        self.items = set(getattr(args, "item", ()))

    def _list(self) -> Tuple[Dict[str, Any], ...]:
        done_status = set([False])
        if self.args.closed:
            done_status.add(True)
        logger.debug("done_status={}", done_status)

        def _iter() -> Generator[Dict[str, Any], None, None]:
            for i in (
                Item.select()  # type: ignore
                .filter(Item.done.in_(done_status))
                .order_by(Item.updated_at.desc())
                .limit()
            ):
                yield {
                    "#": i.id,
                    "done": f"[{'x' if i.done else ' '}]",
                    "title": i.title,
                    "created": i.created_at,
                    "updated": i.updated_at,
                }

        return tuple(_iter())

    def dispatch(self) -> None:
        with self.db.bind_ctx(MODELS):
            self.db.create_tables(MODELS)
            command = self.args.command
            if command == "add":
                for title in self.items:
                    logger.info("Adding {!r}", title)
                    Item.create(title=title)  # type: ignore
            elif command == "done":
                for item_id in self.items:
                    logger.info("Marking {!r} as done", item_id)
                    try:
                        item = Item.get_by_id(item_id)  # type: ignore
                        item.done = True
                        item.set_updated()
                    except DoesNotExist:
                        logger.warning("Item {} not present", item_id)
            elif command == "rm":
                for item_id in self.items:
                    logger.info("Removing {!r}", item_id)
                    try:
                        item = Item.get_by_id(item_id)  # type: ignore
                        item.delete_instance()
                    except DoesNotExist:
                        logger.warning("Item {} does not exist", item_id)
            elif command:
                logger.warning("{!r} command not implemented yet", command)

            rows = self._list()
            if rows:
                print(tabulate(rows, headers="keys"))
            print(f"\nShowed {len(rows)} row(s)")
