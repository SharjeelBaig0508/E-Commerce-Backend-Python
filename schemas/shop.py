# -------------< Imports >-------------
from marshmallow import (
    Schema,
    fields,
)
from decorators.schema_handler import validation_error_handler

# -------------< Schemas >-------------
class ShopSchema(Schema):
    name = fields.String(required=True)

    address = fields.String(required=True)
    geo_location = fields.Tuple(
        required=True,
        tuple_fields=(
            fields.Float(
                required=True,
                min=-180,
                max=180,
                error="Longitude must be in between {min} and {max} inclusive",
            ),
            fields.Float(
                required=True,
                min=-90,
                max=90,
                error="Latitude must be in between {min} and {max} inclusive",
            ),
        ),
    )


# -------------< Validators >-------------
@validation_error_handler
def shop_validator(body):
    return {}, ShopSchema().load(body)
