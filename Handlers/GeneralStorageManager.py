from typing import Callable

from ZODB.Connection import Connection
from ZODB.DB import DB
from transaction import TransactionManager

from Utilities.config import Config


class GeneralStorageManager:
    db: DB = DB(Config.SETTINGS['db_path'])

    def __init__(self):
        self._transaction: TransactionManager = TransactionManager()
        self._connection: Connection = self.db.open(self._transaction)
        self.root = self._connection.root()
        self.commit: Callable = self._transaction.commit
        self.sync: Callable = self._connection.sync

    def close(self) -> None:
        self._connection.close()
        self.db.close()
