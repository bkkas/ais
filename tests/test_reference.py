import pytest
# Due to relatives import being hard in python
# without adding to sys.path, tests should be run in
# the parent directory (ais/) with `python -m pytest` or with
# any of the ways listed here:
# https://docs.pytest.org/en/7.1.x/explanation/goodpractices.html#tests-outside-application-code
import src.ais_analyzer as ais


# Tests should have a descriptive name
# Tests have to start or end with *test*
# for pytest to register them
def test_addition():
    assert 4 == (2 + 2)


# Tests can be packaged into classes
class TestClass:
    # Pytest gives each function a unique instance of the class
    # This means that even if "val" where to be incremented
    # in a function, "val" would still be "0" for the next function
    val = 0

    # Function still needs to be prefixed by test_
    def test_something(self):
        assert True

    def test_another(self):
        assert True


def some_function(x: int) -> int:
    return x + 2

def divide_by_zero(x: float) -> float:
    return x / 0

class TestClass2:
    # One way to define fixtures
    # These fixtures can also request other fixtures in the same way the test function
    # below requests this fixture
    # These are also reusable, so each time a function requests a fixture, it will be re-executed
    @pytest.fixture
    def added_list(self):
        return [some_function(2), some_function(4)]

    # When added as an argument, pytest will then search for the
    # argument and pass the then executed fixture function to the test function
    def test_some_function(self, added_list):
        assert added_list[0] == 4
        assert added_list[1] == 6
        assert all([type(x) == int for x in added_list])

    # The scope keyword tells how often a fixture should be called.
    # Default is "function", which calls it each time a function requests it
    # Module will call it once for each module, meaning each testfile.py that requests
    # this fixture. This can be useful for things like connection to a port or a server,
    # and not having to re-connect each function call
    #
    # A list of scopes:
    # * function:   the default scope, the fixture is destroyed at the end of the test.
    # * class:      the fixture is destroyed during teardown of the last test in the class.
    # * module:     the fixture is destroyed during teardown of the last test in the module.
    # * package:    the fixture is destroyed during teardown of the last test in the package.
    # * session:    the fixture is destroyed at the end of the test session.
    @pytest.fixture(scope="module")
    def some_fixture(self):
        return "hunter2"

    # Generally, fixtures should yield and not return
    # The code after the yield statement is executed *after* all tests that requests this fixture are executed
    # This means that if you have code where you need a "cleanup" function afterwards, or you need to deconstruct some
    # variables, this can safely be done after the yield statement.
    @pytest.fixture
    def yield_example(self):
        yield some_function(4)
        # Teardown code

    # For ensuring that a function returns an error
    # The error in question is the one in pytest.raises
    # Useful to ensure that unwanted behaviour does not appear in edge cases
    # or when receiving unexpected input.
    def test_error_on_this(self):
        with pytest.raises(ZeroDivisionError):
            divide_by_zero(5)
