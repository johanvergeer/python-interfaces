from attr import dataclass
from core.entities import BaseEntity

import pytest


@dataclass
class BaseEntityImpl(BaseEntity):
    pass


class TestBaseEntity:
    def test_init(self):
        # GIVEN a base entity
        entity = BaseEntityImpl()

        # WHEN the id is not set

        # THEN the id is None
        assert entity.id is None

    def test_set_and_get_id(self, faker):
        # GIVEN a base entity
        entity = BaseEntityImpl()
        # AND an id
        entity_id = faker.random_number()

        # WHEN the entity id is set
        entity.id = entity_id

        # THEN the id is set
        assert entity.id == entity_id

    def test_set_id__already_set(self, faker):
        # GIVEN a base entity
        entity = BaseEntityImpl()
        # AND the id is already set
        entity.id = faker.random_number()

        # WHEN the id is set the second time
        with pytest.raises(ValueError) as err:
            entity.id = faker.random_number()

        # THEN an error is raised because the id cannot be set twice
        assert "id of an Entity cannot be changed once it is set" in str(err.value)
