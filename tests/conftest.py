import pytest
from faker import Faker


@pytest.fixture(scope="session")
def faker() -> Faker:
    """Return a :class:Faker instance for the test session"""
    return Faker()
