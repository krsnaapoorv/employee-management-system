"""
Register all SQLAlchemy models for Flask-Migrate.

Import every model here so `import app.repositories.models` in application.py
registers metadata without listing models in the entry file.
"""

from app.repositories.models.employee_dao.employee import Employee

__all__ = ["Employee"]
