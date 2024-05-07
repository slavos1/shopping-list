from argparse import Namespace
from typing import Callable

import pytest

from shopping_list.items import ItemManager
from shopping_list.models import MODELS, Item


@pytest.fixture
def manager(tmp_path) -> Callable:
    def _make_manager(command, items) -> ItemManager:
        args = Namespace()
        args.db_file = tmp_path / "shop.db"
        args.command = command
        args.item = items
        args.closed = None
        return ItemManager(args)

    return _make_manager


def test_add(manager) -> None:
    m = manager("add", ("item1", "item2", "item1"))
    m.dispatch()
    with m.db.bind_ctx(MODELS):
        items = list(Item.select().order_by(Item.title))
        assert len(items) == 2
        assert items[0].title == "item1"
        assert items[1].title == "item2"
        assert all(i.done is False for i in items)


def test_done(manager) -> None:
    m = manager("add", ("item1", "item2", "item1"))
    m.dispatch()
    with m.db.bind_ctx(MODELS):
        items = {i.title: i.id for i in Item.select().order_by(Item.title)}

    m = manager(
        "done",
        (
            items["item1"],
            items["item1"],
        ),
    )
    m.dispatch()
    with m.db.bind_ctx(MODELS):
        assert Item.select().count() == 2
        assert Item.select().filter(Item.title == "item1").first().done
        assert not Item.select().filter(Item.title == "item2").first().done


def test_rm(manager) -> None:
    m = manager("add", ("item1", "item2", "item1"))
    m.dispatch()
    with m.db.bind_ctx(MODELS):
        items = {i.title: i.id for i in Item.select().order_by(Item.title)}

    m = manager(
        "rm",
        (
            items["item1"],
            items["item1"],
        ),
    )
    m.dispatch()
    with m.db.bind_ctx(MODELS):
        assert Item.select().count() == 1
        assert not Item.select().filter(Item.title == "item1").exists()
        assert Item.select().filter(Item.title == "item2").count() == 1
