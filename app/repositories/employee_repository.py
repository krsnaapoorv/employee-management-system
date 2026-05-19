""" This module defines the EmployeeRepository class,
    which provides methods for performing CRUD operations on Employee records in the database using SQLAlchemy.
"""
from app.repositories.models import Employee
from app.extensions import db


class EmployeeRepository:

    def __init__(self):
        self.emp = Employee

    @classmethod
    def create(cls, name, email, department, date_joined):
        employee = Employee(
            name=name,
            email=email,
            department=department,
            date_joined=date_joined,
        )
        db.session.add(employee)
        db.session.commit()
        return employee

    def get_all(self):
        return self.emp.query.all()

    def get_by_id(self, employee_id):
        return db.session.get(self.emp, employee_id)

    def get_by_email(self, email):
        return self.emp.query.filter_by(email=email).first()

    def update_emp(self):
        db.session.commit()

    def delete_emp(self, employee):
        db.session.delete(employee)
        db.session.commit()
