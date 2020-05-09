from dataclasses import dataclass
from datetime import date
from typing import Dict

from core.entities import BaseEntity


@dataclass
class Person(BaseEntity):
    name: str
    date_of_birth: date

    def as_dict(self):
        return {
            "name": self.name,
            "date_of_birth": self.date_of_birth.isoformat(),
            "id": self.id,
        }

    @classmethod
    def from_dict(cls, person_dict: Dict) -> "Person":
        person = Person(
            name=person_dict["name"],
            date_of_birth=date.fromisoformat(person_dict["date_of_birth"]),
        )

        setattr(person, "_Person__id", person_dict["id"])

        return person
