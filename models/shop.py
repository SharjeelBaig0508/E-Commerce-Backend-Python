from datetime import datetime

from enum import Enum
from mongoengine import (
    QuerySet, queryset_manager,
    Document, StringField,
    EnumField, DateTimeField,
    ReferenceField, GeoPointField,
    FloatField, IntField,
)


class Status(Enum):
    ACTIVE = 0
    INACTIVE = 1

class Shop(Document):
    name = StringField(required=True)

    address = StringField(required=True)
    geo_location = GeoPointField(required=True)

    ratings = FloatField(default=0.0)
    total_reviews = IntField(default=0)

    user = ReferenceField('User')

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
    def objects(self, queryset: QuerySet) -> QuerySet:
        return queryset.order_by('-createdAt')

    def update(self, **kwargs):
        self.updatedAt = datetime.utcnow()
        kwargs['updatedAt'] = self.updatedAt
        return super().update(**kwargs)
