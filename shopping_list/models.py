from datetime import datetime, timezone
from pathlib import Path

from loguru import logger
from peewee import BooleanField, CharField, Database, DateTimeField, Model, SqliteDatabase

DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"

db = SqliteDatabase(None)


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime(DATE_TIME_FORMAT)


class BaseModel(Model):
    class Meta:
        database = db


def db_init(db_file: Path) -> Database:
    logger.info("Opening DB {}", db_file)
    try:
        db_file = db_file.expanduser()
        db_file.parent.mkdir(parents=True, exist_ok=True)
    except Exception as exc:
        # assuming memory db
        logger.error("Unable to create {} ({})", db_file, exc)
    db.init(
        db_file,
        pragmas={
            "journal_mode": "WAL",
            "busy_timeout": 15 * 1000,
            "synchronous": "NORMAL",
            "cache_size": 1000000000,
            "foreign_keys": 1,
            "temp_store": "memory",
        },
    )
    return db


class Item(BaseModel):
    created_at = DateTimeField([DATE_TIME_FORMAT])
    updated_at = DateTimeField([DATE_TIME_FORMAT])
    title = CharField(max_length=4096)
    done = BooleanField(default=False, null=False)

    def __init__(self, *args, **kwargs) -> None:  # type: ignore
        now = utc_now()
        if "created_at" not in kwargs:
            kwargs["created_at"] = now
        if "updated_at" not in kwargs:
            kwargs["updated_at"] = now
        super().__init__(*args, **kwargs)

    def set_updated(self) -> None:
        self.updated_at = utc_now()  # type: ignore
        self.save()


MODELS = [Item]
