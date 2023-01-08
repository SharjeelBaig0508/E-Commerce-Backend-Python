# -------------< Imports >-------------
from marshmallow import (
    Schema,
    fields,
    validate,
)
from decorators.schema_handler import validation_error_handler

# -------------< Schemas >-------------
class AddressSchema(Schema):
    TYPE_CHOICES = ['billing', 'shipping']

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

    type = fields.String(
        required=True,
        validate=validate.OneOf(
            TYPE_CHOICES
        ),
    )

# -------------< Validators >-------------
@validation_error_handler
def address_validator(body):
    return {}, AddressSchema().load(body)
