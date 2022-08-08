from typing import Tuple


class ValidationError(Exception):
    details = {}

    def __init__(self, details):
        self.details = details


def is_positive_float(num):
    try:
        if float(num) > 0.0:
            return True
        else:
            return False
    except ValueError:
        return False


def get_order_key_and_direction(order: str) -> Tuple[str, bool]:
    is_ascending = False if order[0] == "-" else True
    order_by = order if is_ascending else order[1:]

    return (order_by.lower(), not is_ascending)


def is_valid_ordering(order: str) -> bool:
    if len(order) < 1:
        return False

    order_by, _ = get_order_key_and_direction(order)

    from models import Spending

    return order_by in Spending.orderby_fields


def is_valid_filtering(filter: str) -> bool:
    if len(filter) < 1:
        return False

    from models import Spending
    return filter.lower() in Spending.filterby_fields
