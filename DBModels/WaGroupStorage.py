from DBModels.GroupStorage import GroupStorage
from DBModels.WaUserStorage import WaUserStorage
from Utilities.typings import WaGroupId, GroupDescription, GroupName
from typing import List


class WaGroupStorage(GroupStorage):
    def __init__(self, id: WaGroupId, name: GroupName, description: GroupDescription,
                 users: List[WaUserStorage] = None):
        super().__init__(name=name, description=description, users=users)
        self.id: WaGroupId = id
