import pytest

from people.usecases import AddPersonUseCase, FindPersonByIdUseCase


class TestAddPersonUseCase:
    @pytest.fixture()
    def add_person_use_case(self, person_repository_protocol_mock):
        return AddPersonUseCase(person_repository_protocol_mock)

    def test_add_person(
        self, person_repository_protocol_mock, person, add_person_use_case
    ):
        # GIVEN an AddPersonUseCase with a PersonRepository
        # AND a person without an id

        # WHEN the use case is executed
        add_person_use_case.execute(person)

        # THEN the add_person() method should be called on the repository
        person_repository_protocol_mock.add_person.assert_called_once_with(person)

    def test_add_person__person_with_id_throws(
        self, person_repository_protocol_mock, person_with_id, add_person_use_case
    ):
        # GIVEN an AddPersonUseCase with a PersonRepository
        # AND a person with an id

        person_repository_protocol_mock.add_person.side_effect = ValueError

        # WHEN the use case is executed
        with pytest.raises(ValueError):
            add_person_use_case.execute(person_with_id)

        # THEN the add_person() method should have thrown a ValueError
        person_repository_protocol_mock.add_person.assert_called_once_with(
            person_with_id
        )


class TestFindPersonByIdUseCase:
    @pytest.fixture
    def use_case(self, person_repository_protocol_mock):
        return FindPersonByIdUseCase(person_repository_protocol_mock)

    def test_find_person_by_id(
        self, person_repository_protocol_mock, person_with_id, use_case
    ):
        # GIVEN a FindPersonByIdUseCase
        # AND the Person to find exists
        person_repository_protocol_mock.find_person_by_id.return_value = person_with_id

        # WHEN executing the use case
        retrieved_person = use_case.execute(person_with_id.id)

        # THEN the person is returned
        assert retrieved_person == person_with_id
        person_repository_protocol_mock.find_person_by_id.assert_called_once_with(
            person_with_id.id
        )
