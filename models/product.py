from datetime import datetime

from enum import Enum
from mongoengine import (
    QuerySet, queryset_manager,
    Document, StringField,
    EnumField, DateTimeField,
    FloatField, URLField,
    ListField, ReferenceField,
)


class Status(Enum):
    ACTIVE = 0
    INACTIVE = 1

class Product(Document):
    name = StringField(required=True)
    price = FloatField(required=True)
    quantity = FloatField(required=True)

    stock = FloatField()
    sold = FloatField()

    gallery = ListField(URLField(), default=[])

    shop = ReferenceField('Shop')
    category = ReferenceField('Category')
    reviews = ReferenceField('Reviews')

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
