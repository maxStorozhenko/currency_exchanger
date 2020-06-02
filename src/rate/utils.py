from datetime import datetime
from decimal import Decimal


def to_decimal(num) -> Decimal:
    return round(Decimal(num), 2)


def display(model_object, attr):
    if hasattr(model_object, f'get_{attr}_display'):
        return getattr(model_object, f'get_{attr}_display')()

    if type(getattr(model_object, attr)) is datetime:
        return model_object.get_date()
    return getattr(model_object, attr)
