# -------------< Imports >-------------
from marshmallow import (
    Schema,
    fields,
)
from decorators.schema_handler import validation_error_handler

# -------------< Schemas >-------------
class ReviewsSchema(Schema):
    stars = fields.Integer(
        required=True,
        min=0,
        max=5,
    )
    comment = fields.String()
    gallery = fields.List(
        fields.Url()
    )

# -------------< Validators >-------------
@validation_error_handler
def reviews_validator(body):
    return {}, ReviewsSchema().load(body)
