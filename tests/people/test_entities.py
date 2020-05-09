from people.entities import Person


class TestPerson:
    def test_create_new_person(self, name, date_of_birth):
        # GIVEN some person attributes

        # WHEN creating a person
        person = Person(name, date_of_birth)

        # THEN the person's attributes are set
        assert person.name == name
        assert person.date_of_birth == date_of_birth
        assert person.id is None

    def test_set_id(self, person, faker):
        # GIVEN a Person
        # AND an id
        id_ = faker.random_digit()

        # WHEN setting the __id attribute
        person._Person__id = id_

        # THEN the id property has the id value
        assert person.id == id_

    def test_to_dict(self, person_with_id, name, date_of_birth):
        assert person_with_id.as_dict() == {
            "name": name,
            "date_of_birth": date_of_birth.isoformat(),
            "id": person_with_id.id,
        }

    def test_from_dict(self, person_with_id):
        assert Person.from_dict(person_with_id.as_dict()) == person_with_id
