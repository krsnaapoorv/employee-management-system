"""Service layer for employee-related business logic"""
from app.repositories.employee_repository import EmployeeRepository
from app.utils.exceptions import ValidationError, ResourceNotFound


# Service layer for employee-related business logic
class EmployeeService:

    def __init__(self, repository=None):
        self.repository = repository or EmployeeRepository()

    def create_employee(self, data):
        existing_employee = self.repository.get_by_email(data["email"])

        if existing_employee:
            raise ValidationError("Email already exists")

        return self.repository.create(
            name=data["name"],
            email=data["email"],
            department=data["department"],
            date_joined=data["date_joined"],
        )

    def get_all_employees(self):
        return self.repository.get_all()

    def get_employee(self, employee_id):
        employee = self.repository.get_by_id(employee_id)

        if not employee:
            raise ResourceNotFound("Employee not found")

        return employee

    def update_employee(self, employee_id, data):
        if not data:
            raise ValidationError("At least one field is required to update")

        employee = self.get_employee(employee_id)

        if "email" in data:
            existing = self.repository.get_by_email(data["email"])
            if existing and existing.id != employee.id:
                raise ValidationError("Email already exists")

        for field in ("name", "email", "department", "date_joined"):
            if field in data:
                setattr(employee, field, data[field])

        self.repository.update_emp()

        return employee

    def delete_employee(self, employee_id):
        employee = self.get_employee(employee_id)
        self.repository.delete_emp(employee)
