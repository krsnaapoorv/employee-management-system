from datetime import date
from types import SimpleNamespace

import pytest

from application import create_app


def make_employee(**overrides):
    data = {
        "id": 1,
        "name": "Apoorva Krishna",
        "email": "apporva.k@example.com",
        "department": "Engineering",
        "date_joined": date(2022, 1, 15),
    }
    data.update(overrides)
    return SimpleNamespace(**data)


@pytest.fixture
def app():
    application = create_app()
    application.config.update({"TESTING": True})
    return application


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def sample_employee_data():
    return {
        "name": "Apoorva Krishna",
        "email": "apporva.k@example.com",
        "department": "Engineering",
        "date_joined": date(2022, 1, 15),
    }
