from datetime import date
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from app.services.employee_service import EmployeeService
from app.utils.exceptions import ResourceNotFound, ValidationError

from tests.conftest import make_employee


@pytest.fixture
def mock_repository():
    return MagicMock()


@pytest.fixture
def service(mock_repository):
    return EmployeeService(repository=mock_repository)


def test_create_employee_success(service, mock_repository, sample_employee_data):
    mock_repository.get_by_email.return_value = None
    mock_employee = make_employee()
    mock_repository.create.return_value = mock_employee

    result = service.create_employee(sample_employee_data)

    mock_repository.get_by_email.assert_called_once_with("apporva.k@example.com")
    mock_repository.create.assert_called_once_with(
        name="Apoorva Krishna",
        email="apporva.k@example.com",
        department="Engineering",
        date_joined=date(2022, 1, 15),
    )
    assert result is mock_employee


def test_create_employee_duplicate_email(service, mock_repository, sample_employee_data):
    mock_repository.get_by_email.return_value = make_employee()

    with pytest.raises(ValidationError, match="Email already exists"):
        service.create_employee(sample_employee_data)

    mock_repository.create.assert_not_called()


def test_get_employee_not_found(service, mock_repository):
    mock_repository.get_by_id.return_value = None

    with pytest.raises(ResourceNotFound, match="Employee not found"):
        service.get_employee(1)


def test_get_all_employees_to_repository(service, mock_repository):
    expected = [make_employee(), make_employee(id=2, email="akrishna@example.com")]
    mock_repository.get_all.return_value = expected

    result = service.get_all_employees()

    mock_repository.get_all.assert_called_once()
    assert result == expected


def test_update_employee_raises_when_payload_empty(service, mock_repository):
    with pytest.raises(ValidationError, match="At least one field is required"):
        service.update_employee(1, {})

    mock_repository.get_by_id.assert_not_called()


def test_update_employee_applies_changes_and_commits(service, mock_repository):
    mock_employee = SimpleNamespace(
        id=1,
        name="Apoorva Krishna",
        email="apporva.k@example.com",
        department="Engineering",
        date_joined=date(2022, 1, 15),
    )
    mock_repository.get_by_id.return_value = mock_employee

    result = service.update_employee(1, {"name": "Rahul K", "department": "Product"})

    assert mock_employee.name == "Rahul K"
    assert mock_employee.department == "Product"
    mock_repository.update_emp.assert_called_once()
    assert result is mock_employee


def test_update_employee_raises_when_email_taken(service, mock_repository):
    mock_employee = SimpleNamespace(
        id=1,
        name="Apoorva Krishna",
        email="apporva.k@example.com",
        department="Engineering",
        date_joined=date(2022, 1, 15),
    )
    mock_repository.get_by_id.return_value = mock_employee
    mock_repository.get_by_email.return_value = SimpleNamespace(
        id=2,
        email="akrishna@example.com",
    )

    with pytest.raises(ValidationError, match="Email already exists"):
        service.update_employee(1, {"email": "akrishna@example.com"})

    mock_repository.update_emp.assert_not_called()


def test_delete_employee_delegates_to_repository(service, mock_repository):
    mock_employee = make_employee()
    mock_repository.get_by_id.return_value = mock_employee

    service.delete_employee(1)

    mock_repository.get_by_id.assert_called_once_with(1)
    mock_repository.delete_emp.assert_called_once_with(mock_employee)
