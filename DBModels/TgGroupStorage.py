from DBModels.GroupStorage import GroupStorage
from DBModels.TgBotStorage import TgBotStorage
from Utilities.typings import GroupDescription, GroupName, TgGroupId
from typing import List


class TgGroupStorage(GroupStorage):
    def __init__(self, id: TgGroupId, name: GroupName, description: GroupDescription,
                 users: List[TgBotStorage] = None):
        super().__init__(name=name, description=description, users=users)
        self.id: TgGroupId = id
