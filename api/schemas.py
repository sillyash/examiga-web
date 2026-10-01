from apiflask import Schema
from apiflask.fields import Boolean, Date, DateTime, Integer, String, Time
from apiflask.validators import Length


class TourDateOut(Schema):
    id = Integer()
    date = Date()
    time = Time(allow_none=True)
    city = String()
    venue = String()
    address = String(allow_none=True)
    ticket_url = String(allow_none=True)
    info_url = String(allow_none=True)
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
