from datetime import datetime

from enum import Enum
from mongoengine import (
    QuerySet, queryset_manager,
    Document, StringField,
    EnumField, DateTimeField,
    IntField, URLField,
    ListField, ReferenceField,
)


class Status(Enum):
    ACTIVE = 0
    INACTIVE = 1

class Reviews(Document):
    stars = IntField(
        required=True,
        min_value=0,
        max_value=5,
    )
    comment = StringField()

    gallery = ListField(URLField(), default=[])

    product = ReferenceField('Product')
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
    def objects(doc_cls, queryset: QuerySet):
        return queryset.order_by('-updatedAt')

    def update(self, **kwargs):
        self.updatedAt = datetime.utcnow()
        kwargs['updatedAt'] = self.updatedAt
        return super().update(**kwargs)
