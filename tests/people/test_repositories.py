import json
import tempfile
from pathlib import Path

import pytest

from people.entities import Person
from people.repositories import PersonJsonRepository, PersonSqLiteRepository


class TestPersonSqLiteRepository:
    @pytest.fixture
    def repo(self, sqlite_conn):
        return PersonSqLiteRepository(sqlite_conn)

    def test_add_person(self, repo, person, sqlite_conn):
        # GIVEN a PersonSqLiteRepository
        # AND a Person where the __id attribute is not set
        assert person.id is None

        # WHEN adding the person to the PersonSqLiteRepository
        repo.add_person(person)

        # THEN the person.id property is set
        assert person.id is not None

        # AND the person is added to the database
        cursor = sqlite_conn.cursor()
        cursor.execute("select * from people")
        found_person_data = cursor.fetchone()

        assert found_person_data is not None

    def test_add_person__id_already_set(self, repo, person_with_id, faker):
        # GIVEN a PersonSqLiteRepository
        # AND a Person where the __id attribute is set

        # WHEN trying to add the person to the PersonSqLiteRepository
        with pytest.raises(ValueError) as err:
            repo.add_person(person_with_id)

        # THEN a ValueError is raised because the id should not be set
        assert "id should not be set when adding a person" in str(err.value)

    def test_find_person_by_id(self, repo, person):
        # GIVEN a PersonSqLiteRepository
        # AND a person is added to the database
        repo.add_person(person)

        # WHEN retrieving the person by it's id
        retrieved_person = repo.find_person_by_id(person.id)

        # THEN the correct person is found
        assert person == retrieved_person

    def test_find_person_by_id__not_found(self, repo, faker):
        # GIVEN a repository
        # AND no person is added to the repository

        # WHEN trying to find a person by an id that does not exist
        retrieved_person = repo.find_person_by_id(faker.random_number())

        # THEN no person is found
        assert retrieved_person is None


class TestPersonJsonRepository:
    @pytest.fixture
    def json_file(self, tmpdir):
        """
        Creates a temporary json file and returns the path
        """
        file = tempfile.mkstemp(suffix=".json")

        path = Path(file[1])
        yield path

        path.unlink()

    @pytest.fixture
    def repo(self, json_file):
        """Creates a PersonJsonRepository with a valid json file path"""
        return PersonJsonRepository(json_file)

    def test_init_repo__throws_if_file_does_not_exist(self):
        # GIVEN a Path to a non-existent json file
        non_existent_json_file = (Path() / "non_existent.json").absolute()

        # WHEN instantiating the repo
        with pytest.raises(FileNotFoundError) as err:
            PersonJsonRepository(non_existent_json_file)

        # THEN an error is raised
        assert f"{non_existent_json_file} not found" in str(err.value)

    def test_add_person(self, person, repo, json_file):
        # GIVEN a PersonJsonRepository
        # AND a person

        # WHEN adding the person to the repo
        repo.add_person(person)

        # THEN the person is added to the json file with the new id
        # AND the last_person_id is set
        with json_file.open() as people_file:
            people_json = json.load(people_file)

            assert people_json == {"last_person_id": 1, "people": [person.as_dict()]}

        # AND the id property is set on the Person
        assert person.id == 1

    def test_add_multiple_people(self, person, repo, json_file, faker):
        # GIVEN a PersonJsonRepository
        # AND a person is already added to the repo
        repo.add_person(person)

        # AND a second person
        second_person = Person(
            faker.name(), faker.date_between(start_date="-60y", end_date="-5y")
        )

        # WHEN adding the second the person to the repo
        repo.add_person(second_person)

        # THEN the person is added to the json file with the new id
        # AND the last_person_id is set
        with json_file.open() as people_file:
            people_json = json.load(people_file)

            assert people_json == {
                "last_person_id": 2,
                "people": [person.as_dict(), second_person.as_dict()],
            }

        # AND the id property is set both persons
        assert person.id == 1
        assert second_person.id == 2

    def test_add_person__id_already_set(self, repo, person_with_id, faker):
        # GIVEN a PersonJsonRepository
        # AND a Person where the __id attribute is set

        # WHEN trying to add the person to the PersonSqLiteRepository
        with pytest.raises(ValueError) as err:
            repo.add_person(person_with_id)

        # THEN a ValueError is raised because the id should not be set
        assert "id should not be set when adding a person" in str(err.value)

    def test_find_person_by_id(self, repo, person):
        # GIVEN a PersonSqLiteRepository
        # AND a person is added to the database
        repo.add_person(person)

        # WHEN retrieving the person by it's id
        retrieved_person = repo.find_person_by_id(person.id)

        # THEN the correct person is found
        assert retrieved_person == person

    def test_find_person_by_id__not_found(self, repo, faker):
        # GIVEN a repository
        # AND no person is added to the repository

        # WHEN trying to find a person by an id that does not exist
        retrieved_person = repo.find_person_by_id(faker.random_number())

        # THEN no person is found
        assert retrieved_person is None
