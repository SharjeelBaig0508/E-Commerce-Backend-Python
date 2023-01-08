# -------------< Imports >-------------
from marshmallow import (
    Schema,
    fields,
)
from decorators.schema_handler import validation_error_handler

# -------------< Schemas >-------------
class ProductSchema(Schema):
    name = fields.String(required=True)
    price = fields.Float(required=True)
    quantity = fields.Float(required=True)

    stock = fields.Float()

    gallery = fields.List(
        fields.Url()
    )

# -------------< Validators >-------------
@validation_error_handler
def reviews_validator(body):
    return {}, ProductSchema().load(body)
