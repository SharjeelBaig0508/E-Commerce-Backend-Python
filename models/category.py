from datetime import datetime

from enum import Enum
from mongoengine import (
    QuerySet, queryset_manager,
    Document, StringField,
    EnumField, DateTimeField,
)


class Status(Enum):
    ACTIVE = 0
    INACTIVE = 1

class Category(Document):
    name = StringField(required=True)

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
        return queryset.order_by('+name')

    def update(self, **kwargs):
        self.updatedAt = datetime.utcnow()
        kwargs['updatedAt'] = self.updatedAt
        return super().update(**kwargs)
