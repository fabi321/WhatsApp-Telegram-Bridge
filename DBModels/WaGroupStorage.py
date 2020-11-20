from typing import List

from DBModels.GroupStorage import GroupStorage
from DBModels.WaUserStorage import WaUserStorage
from Utilities.typings import WaGroupId, GroupDescription, GroupName


class WaGroupStorage(GroupStorage):
    def __init__(self, id: WaGroupId, name: GroupName, description: GroupDescription,
                 users: List[WaUserStorage] = None):
        super().__init__(name=name, description=description, users=users)
        assert isinstance(id, WaGroupId)
        self.id: WaGroupId = id

    def __repr__(self):
        return f'WaGroupStorage({self.id!r}, {self.name!r}, {self.description!r}, users={self.users!r})'

    def get_pipe_id(self) -> str:
        return str(self.id)
