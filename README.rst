##########################
Python Interfaces Tutorial
##########################

This project is all about showing how to create and use interfaces in Python
using Protocols_, which were added in Python 3.8.


I'm a big fan of `Clean Architecture`_, which was described in the book with the same name
and in `Clean Architectures for Python`_. I wanted to apply this architecture in this project.

I could have gone much further with some concepts, but I wanted to keep things as simple as I could.

Entities
########

I created a `BaseEntity` which only has an `id` property which is immutable once it has a value.
The `id` is supposed to be set on saving the entity.

The Person entity can be found in `people.entities.py`.
As you can see it is a very simple entity with a `name` and a `date_of_birth`.

Repositories
############

Repositories take care of persisting and retrieving data to some kind of storage.
Usually I would also include a Unit of Work mechanism but I left that out for the sake of simplicity.

`PersonRepositoryProtocol` is the interface. It only contains two abstract methods
that defines how a class that implements this interface should behave.

As an example I created two implementations, one for a SQLite database and one for json files.
Again, I would usually use a framework like Django or SQLAlchemy, but I wanted to keep this example simple.

Repository Tests
----------------

The repository tests check whether the classes have correctly implemented the interface.
They actually use the database and a json file, which makes them integration tests.

A proper application design makes sure that only the repositories have to use the actual storage.
All other tests can use a Mock of the `PersonRepositoryProtocol` which you can read next.

Use Cases
#########

Use cases handle the business logic of the application. The use cases in this application are very simple,
since the business logic is very simple. But you might imagine that they can be a lot more complicated.

Each use case uses dependency injection to get a `PersonRepositoryProtocol`, which it will use during execution.

Use Case Tests
--------------

The use case tests use a mock object created from the `PersonRepositoryProtocol`.
We don't need to talk to the actual storage.
All we need to know is whether the use case calls the correct methods on the repository.


How to use this?
################

Now you might ask yourself how to use this in practice. Let's take a simple example:

In this example we'll use the `PersonJsonRepository` and we'll save people.json in the home directory.

.. code-block:: python

    if __name__ == "__main__":
        people_file = Path() / "people.json"
        repo = PersonJsonRepository(people_file)

        person = Person("Johan Vergeer", date(1980, 1, 1))

        add_person_use_case = AddPersonUseCase(repo)

        add_person_use_case.execute(person)


And that's it. This is a very simple example, but you can also use this in a CLI app using Click_
or in a webapp using Flask_. When you want to use another storage, just implement the `PersonRepositoryProtocol`
and inject it into the use cases.

So what's next?
###############

As I stated in the example above, you can use the use cases in any framework.
Just be sure you keep the entities and use cases separated from the frameworks.

If you still want to take it up a notch you can take a look at a dependency injection framework.
I listed a few in my `article on dependency injection frameworks`_.


Contribute
##########

If you have any ideas feel free to create an issue or a pull request.

After cloning the repository you can install the dependencies with `poetry install`

Next you need to install `pre-commit`_ with `pre-commit install`.


.. _article on dependency injection frameworks: https://codingwithjohan.com/articles/python/python-dependency-injection-frameworks/
.. _Clean Architecture: https://www.amazon.com/Clean-Architecture-Craftsmans-Software-Structure/dp/0134494164
.. _Clean Architectures for Python: https://leanpub.com/clean-architectures-in-python
.. _Click: https://click.palletsprojects.com/en/7.x/
.. _Flask: https://flask.palletsprojects.com/en/1.1.x/
.. _pre-commit: https://pre-commit.com/
.. _Protocols: https://mypy.readthedocs.io/en/stable/protocols.html#simple-user-defined-protocols
