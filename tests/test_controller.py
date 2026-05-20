from unittest.mock import patch

from tests.conftest import make_employee

SERVICE_PATH = "app.controllers.employee_controller.employee_service"


def _employee_json(sample_employee_data):
    return {
        **sample_employee_data,
        "date_joined": sample_employee_data["date_joined"].isoformat(),
    }


@patch(SERVICE_PATH)
def test_create_employee_returns_201(mock_service, client, sample_employee_data):
    mock_service.create_employee.return_value = make_employee()

    response = client.post("/employees", json=_employee_json(sample_employee_data))

    assert response.status_code == 201
    assert response.get_json()["email"] == "apporva.k@example.com"
    mock_service.create_employee.assert_called_once()


@patch(SERVICE_PATH)
def test_create_employee_returns_400_on_validation_error(
    mock_service, client, sample_employee_data
):
    from app.utils.exceptions import ValidationError

    mock_service.create_employee.side_effect = ValidationError("Email already exists")

    response = client.post("/employees", json=_employee_json(sample_employee_data))

    assert response.status_code == 400
    assert response.get_json()["error"] == "Email already exists"


def test_create_employee_returns_422_on_invalid_payload(client, sample_employee_data):
    payload = _employee_json(sample_employee_data)
    payload["email"] = "not-an-email"

    response = client.post("/employees", json=payload)

    assert response.status_code == 422


@patch(SERVICE_PATH)
def test_get_employees_returns_list(mock_service, client):
    mock_service.get_all_employees.return_value = [
        make_employee(),
        make_employee(id=2, email="akrishna@example.com"),
    ]

    response = client.get("/employees")

    assert response.status_code == 200
    assert len(response.get_json()) == 2
    mock_service.get_all_employees.assert_called_once()


@patch(SERVICE_PATH)
def test_get_employee_returns_200(mock_service, client):
    mock_service.get_employee.return_value = make_employee()

    response = client.get("/employees/1")

    assert response.status_code == 200
    assert response.get_json()["id"] == 1
    assert response.get_json()["name"] == "Apoorva Krishna"
    mock_service.get_employee.assert_called_once_with(1)


@patch(SERVICE_PATH)
def test_get_employee_returns_404(mock_service, client):
    from app.utils.exceptions import ResourceNotFound

    mock_service.get_employee.side_effect = ResourceNotFound("Employee not found")

    response = client.get("/employees/99")

    assert response.status_code == 404
    assert response.get_json()["error"] == "Employee not found"


@patch(SERVICE_PATH)
def test_update_employee_returns_200(mock_service, client):
    mock_service.update_employee.return_value = make_employee(name="Rahul K")

    response = client.put("/employees/1", json={"name": "Rahul K"})

    assert response.status_code == 200
    assert response.get_json()["name"] == "Rahul K"
    mock_service.update_employee.assert_called_once()


@patch(SERVICE_PATH)
def test_update_employee_returns_404(mock_service, client):
    from app.utils.exceptions import ResourceNotFound

    mock_service.update_employee.side_effect = ResourceNotFound("Employee not found")

    response = client.put("/employees/99", json={"name": "Rahul K"})

    assert response.status_code == 404


@patch(SERVICE_PATH)
def test_delete_employee_returns_success_message(mock_service, client):
    response = client.delete("/employees/1")

    assert response.status_code == 200
    assert response.get_json()["message"] == "Employee deleted successfully"
    mock_service.delete_employee.assert_called_once_with(1)


@patch(SERVICE_PATH)
def test_delete_employee_returns_404(mock_service, client):
    from app.utils.exceptions import ResourceNotFound

    mock_service.delete_employee.side_effect = ResourceNotFound("Employee not found")

    response = client.delete("/employees/99")

    assert response.status_code == 404
