"""
Bulk Validation Model.
"""
from __future__ import annotations

from sqlalchemy.sql import text

from strr_api.common.enum import BaseEnum, auto
from strr_api.models.base_model import BaseModel

from .db import db


class BulkValidation(BaseModel):
    """Bulk Validation Model."""

    class Status(BaseEnum):
        """Enum of the registration types."""

        NOT_PROCESSED = auto()  # pylint: disable=invalid-name
        PROCESSING = auto()  # pylint: disable=invalid-name
        ERROR = auto()  # pylint: disable=invalid-name
        COMPLETED = auto()  # pylint: disable=invalid-name

    __tablename__ = "bulk_validation"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    request_file_id = db.Column(db.String(250), index=True)
    response_file_id = db.Column(db.String(250))
    request_timestamp = db.Column(db.DateTime, nullable=False, server_default=text("(NOW())"))
    response_timestamp = db.Column(db.DateTime)
    status = db.Column(db.Enum(Status), nullable=False, index=True, default=Status.NOT_PROCESSED)
