# -------------< Imports >-------------
from marshmallow import (
    Schema,
    fields,
)
from decorators.schema_handler import validation_error_handler

# -------------< Schemas >-------------
class CategorySchema(Schema):
    name = fields.String(required=True)

# -------------< Validators >-------------
@validation_error_handler
def category_validator(body):
    return {}, CategorySchema().load(body)
