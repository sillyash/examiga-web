from apiflask import Schema
from apiflask.fields import Boolean, Date, DateTime, Integer, List, Nested, String, Time
from apiflask.validators import Length, Range


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
    message = String(required=True, validate=Length(min=1, max=500))
    # Honeypot: hidden in the form, so only bots fill it in. Must stay empty.
    website = String(load_default="", validate=Length(max=0))


class ShoutoutOut(Schema):
    id = Integer()
    name = String()
    message = String()
    created_at = DateTime()


class ShoutoutQuery(Schema):
    limit = Integer(load_default=10, validate=Range(min=1, max=50))
    # Cursor: id of the last shoutout already shown; returns the ones posted before it.
    before = Integer(load_default=None)


class ShoutoutPage(Schema):
    shoutouts = List(Nested(ShoutoutOut))
    has_more = Boolean()
