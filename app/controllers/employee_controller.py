""" This module defines the routes and handlers for employee-related operations in the Flask application."""
from flask import jsonify
from marshmallow import EXCLUDE
from webargs.flaskparser import use_args

from . import routes
from app.schemas.employee_schema.employee_schema import EmployeeSchema, EmployeeUpdateSchema
from app.services.employee_service.employee_service import EmployeeService
from app.utils.exceptions import ValidationError, ResourceNotFound

employee_service = EmployeeService()
employee_schema = EmployeeSchema()


@routes.route("/employees", methods=["POST"])
@use_args(EmployeeSchema(unknown=EXCLUDE), location="json")
def create_employee(args):
    try:
        employee = employee_service.create_employee(args)
        return jsonify(employee_schema.dump(employee)), 201
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@routes.route("/employees", methods=["GET"])
def get_employees():
    employees = employee_service.get_all_employees()
    return jsonify(employee_schema.dump(employees, many=True))


@routes.route("/employees/<int:employee_id>", methods=["GET"])
def get_employee(employee_id):
    try:
        employee = employee_service.get_employee(employee_id)
        return jsonify(employee_schema.dump(employee))
    except ResourceNotFound as e:
        return jsonify({"error": str(e)}), 404


@routes.route("/employees/<int:employee_id>", methods=["PUT"])
@use_args(EmployeeUpdateSchema(partial=True, unknown=EXCLUDE), location="json")
def update_employee(args, employee_id):
    try:
        employee = employee_service.update_employee(employee_id, args)
        return jsonify(employee_schema.dump(employee))
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except ResourceNotFound as e:
        return jsonify({"error": str(e)}), 404


@routes.route("/employees/<int:employee_id>", methods=["DELETE"])
def delete_employee(employee_id):
    try:
        employee_service.delete_employee(employee_id)
        return jsonify({"message": "Employee deleted successfully"})
    except ResourceNotFound as e:
        return jsonify({"error": str(e)}), 404
