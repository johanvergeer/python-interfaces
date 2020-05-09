from typing import Optional

from people.entities import Person
from people.repositories import PersonRepositoryProtocol


class AddPersonUseCase:
    def __init__(self, repo: PersonRepositoryProtocol):
        self.__repo = repo

    def execute(self, person: Person) -> None:
        self.__repo.add_person(person)


class FindPersonByIdUseCase:
    def __init__(self, repo: PersonRepositoryProtocol):
        self.__repo = repo

    def execute(self, person_id: int) -> Optional[Person]:
        return self.__repo.find_person_by_id(person_id)
