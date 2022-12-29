from datetime import datetime

from enum import Enum
from mongoengine import (
    QuerySet, queryset_manager,
    Document, StringField,
    EnumField, DateTimeField,
    ReferenceField, GeoPointField,
)


class Status(Enum):
    ACTIVE = 0
    INACTIVE = 1

class Type(Enum):
    BILLING = 0
    SHIPPING = 1

class Address(Document):
    user = ReferenceField('User')

    address = StringField(required=True)
    geo_location = GeoPointField(required=True)

    type = EnumField(
        enum=Type,
        required=True,
        choices=[
            Type.BILLING,
            Type.SHIPPING,
        ],
    )

    status = EnumField(
        Status,
        default=Status.ACTIVE,
        choices=[
            Status.ACTIVE,
            Status.INACTIVE,
        ],
    )

    createdAt = DateTimeField(
        default=datetime.utcnow,
    )
    updatedAt = DateTimeField(
        default=datetime.utcnow,
    )

    @queryset_manager
    def objects(doc_cls, queryset: QuerySet):
        return queryset.order_by('-createdAt')

    def update(self, **kwargs):
        self.updatedAt = datetime.utcnow()
        kwargs['updatedAt'] = self.updatedAt
        return super().update(**kwargs)
