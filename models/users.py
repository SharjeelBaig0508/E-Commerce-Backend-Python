import re

from datetime import datetime
from bcrypt import hashpw, gensalt, checkpw

from enum import Enum
from mongoengine import (
    QuerySet, queryset_manager,
    Document, EmailField,
    StringField, EnumField,
    DateTimeField, GeoPointField,
)


class Status(Enum):
    ACTIVE = 0
    INACTIVE = 1

class Roles(Enum):
    ADMIN = 0
    SHOP_OWNER = 1
    CUSTOMER = 2

class Gender(Enum):
    MALE = 0
    FEMALE = 1
    OTHER = 2

class ContactField(StringField):
    def validate(self, value):
        super(StringField, self).validate(value)

        if re.match(r'^((\+92)?(0092)?(92)?(0)?)(3)([0-9]{9})$/gm', value):
            self.error('Contact Number must be a valid number like (+92) 3xxxxxxxxx')

class User(Document):
    name = StringField()

    email = EmailField(required=True)
    contact_num = ContactField(required=True)

    password = StringField(required=True)

    address = StringField()
    geo_location = GeoPointField()

    gender = EnumField(
        enum=Gender,
        required=True,
        choices=[
            Gender.MALE,
            Gender.FEMALE,
            Gender.OTHER,
        ],
    )

    status = EnumField(
        enum=Status,
        default=Status.ACTIVE,
        choices=[
            Status.ACTIVE,
            Status.INACTIVE,
        ],
    )

    role = EnumField(
        enum=Roles,
        required=True,
        choices=[
            Roles.ADMIN,
            Roles.SHOP_OWNER,
            Roles.CUSTOMER,
        ],
    )

    createdAt = DateTimeField(
        default=datetime.utcnow,
    )
    updatedAt = DateTimeField(
        default=datetime.utcnow,
    )

    def encrypt_password(self):
        if type(self.password) is not str:
            self.password = str(self.password)

        self.password = hashpw(self.password.encode(), gensalt(rounds=7)).decode()

    def check_password(self, password:str) -> bool:
        return checkpw(password.encode(), self.password.encode())

    def save(self, **kwargs):
        self.encrypt_password()
        return super().save(**kwargs)

    @queryset_manager
    def objects(self, queryset: QuerySet) -> QuerySet:
        return queryset.exclude('password').order_by('-createdAt')

    def update(self, **kwargs):
        if self.password:
            self.encrypt_password()
            kwargs['password'] = self.password

        kwargs['updatedAt'] = datetime.utcnow()
        return super().update(**kwargs)

# Default Admin
defaultAdminUser = {
    'name': 'Default Admin',
    'email': 'admin@admin.com',
    'contact_num': '+923123456789',
    'password': 'Admin@123',
    'gender': Gender.MALE,
    'status': Status.ACTIVE,
    'role': Roles.ADMIN,
}

if not User.objects(email=defaultAdminUser['email']):
    adminUser = User(**defaultAdminUser).save()
