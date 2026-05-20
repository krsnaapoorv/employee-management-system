from datetime import date
from unittest.mock import MagicMock, patch

from app.repositories.employee_repository import EmployeeRepository

from tests.conftest import make_employee


@patch("app.repositories.employee_repository.db")
@patch("app.repositories.employee_repository.Employee")
def test_create_persists_employee(mock_employee_cls, mock_db, sample_employee_data):
    mock_employee = MagicMock()
    mock_employee_cls.return_value = mock_employee

    result = EmployeeRepository.create(**sample_employee_data)

    mock_employee_cls.assert_called_once_with(**sample_employee_data)
    mock_db.session.add.assert_called_once_with(mock_employee)
    mock_db.session.commit.assert_called_once()
    assert result is mock_employee


@patch("app.repositories.employee_repository.db")
def test_get_by_id_returns_employee(mock_db):
    mock_employee = make_employee()
    mock_db.session.get.return_value = mock_employee
    repository = EmployeeRepository()

    result = repository.get_by_id(1)

    mock_db.session.get.assert_called_once_with(repository.emp, 1)
    assert result is mock_employee


def test_get_all_returns_query_results():
    repository = EmployeeRepository()
    mock_query = MagicMock()
    expected = [make_employee(), make_employee(id=2, email="akrishna@example.com")]
    mock_query.all.return_value = expected
    repository.emp.query = mock_query

    result = repository.get_all()

    mock_query.all.assert_called_once()
    assert result == expected


def test_get_by_email_returns_first_match():
    repository = EmployeeRepository()
    mock_query = MagicMock()
    mock_employee = make_employee()
    mock_query.filter_by.return_value.first.return_value = mock_employee
    repository.emp.query = mock_query

    result = repository.get_by_email("apporva.k@example.com")

    mock_query.filter_by.assert_called_once_with(email="apporva.k@example.com")
    assert result is mock_employee


@patch("app.repositories.employee_repository.db")
def test_update_emp_commits_session(mock_db):
    EmployeeRepository().update_emp()

    mock_db.session.commit.assert_called_once()


@patch("app.repositories.employee_repository.db")
def test_delete_emp_removes_and_commits(mock_db):
    mock_employee = make_employee()

    EmployeeRepository().delete_emp(mock_employee)

    mock_db.session.delete.assert_called_once_with(mock_employee)
    mock_db.session.commit.assert_called_once()
