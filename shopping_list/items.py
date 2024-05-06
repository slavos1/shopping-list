from argparse import Namespace
from typing import Any, Dict, Iterable

from loguru import logger
from peewee import DoesNotExist
from tabulate import tabulate

from .models import MODELS, Item, db_init


class ItemManager:
    def __init__(self, args: Namespace) -> None:
        self.args = args
        self.db = db_init(args.db_file)

    def _list(self) -> None:
        done_status = set([False])
        if self.args.closed:
            done_status.add(True)
        logger.debug("done_status={}", done_status)

        def _iter() -> Iterable[Dict[str, Any]]:
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

        rows = list(_iter())
        if rows:
            print(tabulate(rows, headers="keys"))
        print(f"\nShowed {len(rows)} row(s)")

    def dispatch(self) -> None:
        with self.db.bind_ctx(MODELS):
            self.db.create_tables(MODELS)
            command = self.args.command
            if command == "add":
                for title in self.args.item:
                    logger.info("Adding {!r}", title)
                    Item.create(title=title)  # type: ignore
            elif command == "done":
                for item_id in self.args.item:
                    logger.info("Marking {!r} as done", item_id)
                    try:
                        item = Item.get_by_id(item_id)  # type: ignore
                        item.done = True
                        item.set_updated()
                    except DoesNotExist:
                        logger.warning("Item {} not present", item_id)
            elif command == "rm":
                for item_id in self.args.item:
                    logger.info("Removing {!r}", item_id)
                    try:
                        item = Item.get_by_id(item_id)  # type: ignore
                        item.delete_instance()
                    except DoesNotExist:
                        logger.warning("Item {} does not exist", item_id)
            elif command:
                logger.warning("{!r} command not implemented yet", command)
            self._list()
