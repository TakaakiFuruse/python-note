import pytest

from rent_o_matic.app import create_app
from rent_o_matic.flask_settings import TestConfig

@pytest.yield_fixture(scope="function")
def app():
    return create_app(TestConfig)
