"""Employee schema for serialization and deserialization using Marshmallow."""
from marshmallow import Schema, fields, validate


class EmployeeSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    email = fields.Email(required=True)
    department = fields.Str(required=True)
    date_joined = fields.Date(required=True)


class EmployeeUpdateSchema(Schema):
    name = fields.Str(validate=validate.Length(min=2, max=100))
    email = fields.Email()
    department = fields.Str()
    date_joined = fields.Date()
