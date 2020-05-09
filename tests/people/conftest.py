import sqlite3
from datetime import date
from typing import Iterator

import pytest
from faker import Faker
from people.entities import Person
from people.repositories import (
    PersonRepositoryProtocol,
    create_tables_if_they_do_not_exist,
)


@pytest.fixture(scope="session")
def faker() -> Faker:
    """Return a :class:Faker instance for the test session"""
    return Faker()


@pytest.fixture
def sqlite_conn(tmpdir) -> Iterator[sqlite3.Connection]:
    """Return a :class:sqlite3.Connection instance for the test function
    and will close the connection after the test
    """
    conn = sqlite3.connect(tmpdir / "people.db")

    create_tables_if_they_do_not_exist(conn)

    yield conn

    conn.close()


@pytest.fixture
def date_of_birth(faker) -> date:
    """Returns a date of birth for a person born between 5 and 60 years ago"""
    return faker.date_between(start_date="-60y", end_date="-5y")


@pytest.fixture
def name(faker) -> str:
    """Returns a name for a person for the test function"""
    return faker.name()


@pytest.fixture
def person(date_of_birth, name):
    """Return a :class:Person instance without an id for the test function"""
    return Person(name, date_of_birth)


@pytest.fixture
def person_with_id(person, faker):
    """Return a :class:Person instance with an id for the test function"""
    person._Person__id = faker.random_digit()
    return person


@pytest.fixture
def person_repository_protocol_mock(mocker):
    """Returns a Mock object for a :class:PersonRepositoryProtocol"""
    return mocker.patch(
        f"{PersonRepositoryProtocol.__module__}.{PersonRepositoryProtocol.__name__}"
    )
