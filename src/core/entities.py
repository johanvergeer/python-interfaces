from abc import ABC
from typing import Optional


class BaseEntity(ABC):
    @property
    def id(self) -> Optional[int]:
        """Entity identifier, which is immutable once it is set."""
        return getattr(self, "_id", None)

    @id.setter
    def id(self, value: int) -> None:
        if self.id is not None:
            raise ValueError("id of an Entity cannot be changed once it is set")

        setattr(self, "_id", value)
