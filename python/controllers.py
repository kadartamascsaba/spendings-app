from models import Currency, Spending
from utils import get_order_key_and_direction, is_valid_ordering


USD_HUF_EXCHANGE_RATE = 387.14


def convert_to_huf(spending: Spending):
    amount = spending.amount
    if spending.currency == Currency.USD:
        amount *= USD_HUF_EXCHANGE_RATE
    return amount


def filter_spendings(spendings: list[Spending], args: dict) -> list[Spending]:
    """
    Filtering the spendings based on the query parameters.

    If the parameters not specified in the Model or equal with ALL, 
    then just return the original list
    """
    for field in Spending.filterby_fields:
        if args.get(field):
            if field == Spending.Keys.currency \
                    and args[field].upper() != Currency.ALL:
                spendings = filter(
                    lambda x: getattr(x, field) == args[field].upper(),
                    spendings
                )
    return spendings


def order_spendings(spendings: list[Spending], args: dict) -> list[Spending]:
    """
    Ordering the spendings based on the query parameters.

    If the parameters not valid, then return original list
    """
    if args.get("order"):
        if is_valid_ordering(args.get("order")):
            order_key, direction = get_order_key_and_direction(
                args.get("order")
            )
            if order_key == Spending.Keys.amount:
                spendings = sorted(
                    spendings,
                    key=convert_to_huf,
                    reverse=direction
                )
            else:
                spendings = sorted(
                    spendings,
                    key=lambda x: getattr(x, order_key),
                    reverse=direction
                )

    return spendings
