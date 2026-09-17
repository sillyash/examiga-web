from apiflask import Schema
from apiflask.fields import Boolean, Date, DateTime, Integer, String
from apiflask.validators import Length


class TourDateOut(Schema):
    id = Integer()
    date = Date()
    city = String()
    venue = String()
    ticket_url = String(allow_none=True)
    is_sold_out = Boolean()
    notes = String(allow_none=True)


class ShoutoutIn(Schema):
    name = String(required=True, validate=Length(min=1, max=80))
    message = String(required=True, validate=Length(min=1))


class ShoutoutOut(Schema):
    id = Integer()
    name = String()
    message = String()
    created_at = DateTime()
