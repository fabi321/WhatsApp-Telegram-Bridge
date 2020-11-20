from typing import List

from DBModels.GroupStorage import GroupStorage
from DBModels.TgBotStorage import TgBotStorage
from Utilities.typings import GroupDescription, GroupName, TgGroupId


class TgGroupStorage(GroupStorage):
    def __init__(self, id: TgGroupId, name: GroupName, description: GroupDescription,
                 users: List[TgBotStorage] = None):
        super().__init__(name=name, description=description, users=users)
        assert isinstance(id, TgGroupId)
        self.id: TgGroupId = id

    def __repr__(self):
        return f'TgGroupStorage({self.id!r}, {self.name!r}, {self.description!r}, {self.users!r})'

    def get_pipe_id(self) -> str:
        return str(self.id)
