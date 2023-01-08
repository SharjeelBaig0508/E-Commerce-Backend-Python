# -------------< Imports >-------------
from marshmallow import (
    Schema,
    fields,
    validate,
    ValidationError,
    validates_schema,
)
from decorators.schema_handler import validation_error_handler

# -------------< Schemas >-------------
class UserLoginSchema(Schema):
    email = fields.Email()
    contact_num = fields.String()
    password = fields.String(required=True)

    @validates_schema
    def validate_fields(self, data: dict, **kwargs):
        if not (data.get('email') and data.get('contact_num')):
            raise ValidationError('must provide email or contact_num', 'email')


class UserSignUpSchema(Schema):
    GENDER_CHOICES = ['male', 'female', 'other']

    name = fields.String()

    email = fields.Email(required=True)
    contact_num = fields.String(
        required=True,
        validate=validate.Regexp(
            r'^((\+92)?(0092)?(92)?(0)?)(3)([0-9]{9})$/gm'
        ),
    )

    password = fields.String(required=True)

    address = fields.String()
    geo_location = fields.Tuple(
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

    gender = fields.String(
        required=True,
        validate=validate.OneOf(
            GENDER_CHOICES
        )
    )


class ChangePasswordSchema(Schema):
    email = fields.Email()
    contact_num = fields.String()

    old_password = fields.String()
    new_password = fields.String()
    confirm_password = fields.String()

    @validates_schema
    def validate_fields(self, data: dict, **kwargs):
        if not (data.get('email') and data.get('contact_num')):
            raise ValidationError('must provide email or contact_num', 'email')

        if data.get('old_password'):
            if not (data.get('new_password') and data.get('confirm_password')):
                raise ValidationError('if one is provided all will be provided', 'old_password')

        if data.get('new_password'):
            if not (data.get('old_password') and data.get('confirm_password')):
                raise ValidationError('if one is provided all will be provided', 'new_password')

        if data.get('confirm_password'):
            if not (data.get('old_password') and data.get('new_password')):
                raise ValidationError('if one is provided all will be provided', 'confirm_password')

        if data.get('new_password') != data.get('confirm_password'):
            raise ValidationError('new_password and confirm_password must be same', 'confirm_password')

        if data.get('old_password') and data.get('new_password'):
            if data['old_password'] == data['new_password']:
                raise ValidationError('new_password must not be same as old_password', 'new_password')

# -------------< Validators >-------------
@validation_error_handler
def user_login_validator(body):
    return {}, UserLoginSchema().load(body)

@validation_error_handler
def user_signup_validator(body):
    return {}, UserSignUpSchema().load(body)

@validation_error_handler
def change_password_validator(body):
    return {}, ChangePasswordSchema().load(body)
