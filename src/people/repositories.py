import json
from abc import abstractmethod
from datetime import date
from json import JSONDecodeError
from pathlib import Path
from sqlite3 import Connection
from typing import Dict, Optional

from typing_extensions import Protocol

from people.entities import Person


class PersonRepositoryProtocol(Protocol):
    @abstractmethod
    def add_person(self, person: Person) -> None:
        """Adds a Person to the repository and sets Person.id

        Args:
            person: A new person to be added

        Raises:
            ValueError: when the person.id property is not None
        """
        ...

    @abstractmethod
    def find_person_by_id(self, person_id: int) -> Optional[Person]:
        """Finds a person by it's id

        Args:
            person_id: id of the Person to be found

        Returns:
            Person with the given id if it is found, None otherwise.
        """
        ...


class PersonSqLiteRepository(PersonRepositoryProtocol):
    def __init__(self, conn: Connection):
        self.__conn = conn

    def add_person(self, person: Person) -> None:
        _validate_person_id_not_set(person)

        self.__conn.execute(
            "insert into people (name, date_of_birth) values (?, ?)",
            [person.name, person.date_of_birth],
        )

        self.__conn.commit()

        self._set_person_id(person)

    def _set_person_id(self, person):
        cursor = self.__conn.cursor()
        cursor.execute("select last_insert_rowid()")
        person._Person__id = cursor.fetchone()[0]

    def find_person_by_id(self, person_id: int) -> Optional[Person]:
        cursor = self.__conn.cursor()
        cursor.execute(
            "select name, date_of_birth from people where id = ?", [person_id]
        )

        person_data = cursor.fetchone()

        if person_data is None:
            return None

        person = Person(person_data[0], date.fromisoformat(person_data[1]))
        person._Person__id = person_id
        return person


def create_tables_if_they_do_not_exist(conn: Connection) -> None:
    # Create table
    conn.execute(
        """
        create table if not exists people
            (
                name text not null,
                date_of_birth text not null,
                id integer not null
                    constraint people_pk
                        primary key autoincrement
            );
    	"""
    )

    conn.execute(
        """
            create unique index if not exists people_id_uindex
                on people (id);
        """
    )


class PersonJsonRepository(PersonRepositoryProtocol):
    def __init__(self, json_file: Path):
        if not json_file.exists():
            raise FileNotFoundError(f"{json_file} not found")

        self.__json_file = json_file

    def add_person(self, person: Person) -> None:
        _validate_person_id_not_set(person)

        people_json = self._load_people_json()

        with self.__json_file.open("w") as people_file:
            next_person_id = people_json["last_person_id"] + 1
            person._Person__id = next_person_id
            people_json["last_person_id"] = next_person_id

            people_json["people"].append(person.as_dict())

            json.dump(people_json, people_file)

    def find_person_by_id(self, person_id: int) -> Optional[Person]:
        people_json = self._load_people_json()

        try:
            return next(
                Person.from_dict(person)
                for person in people_json["people"]
                if person["id"] == person_id
            )
        except StopIteration:
            return None

    def _load_people_json(self) -> Dict:
        with self.__json_file.open() as people_file:
            try:
                return json.load(people_file)
            except JSONDecodeError:
                return {"last_person_id": 0, "people": []}


def _validate_person_id_not_set(person: Person) -> None:
    if person.id is not None:
        raise ValueError("id should not be set when adding a person")
