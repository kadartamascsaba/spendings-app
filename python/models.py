from datetime import datetime

from utils import ValidationError, is_positive_float


class Currency():
    ALL = "ALL"
    HUF = "HUF"
    USD = "USD"


class Spending():

    class Keys:
        description = "description"
        amount = "amount"
        currency = "currency"
        spent_at = "spent_at"

    description = ""
    amount = 0.0
    currency = Currency.HUF
    spent_at = datetime.now()

    # Helper fields for validating, ordering and filtering
    mandatory_fields = [Keys.description, Keys.amount]
    orderby_fields = [Keys.amount, Keys.spent_at]
    filterby_fields = [Keys.currency]

    def __init__(self, spending):
        self.description = spending[Spending.Keys.description]
        self.amount = float(spending[Spending.Keys.amount])
        self.currency = spending.get(Spending.Keys.currency, Currency.HUF)
        self.spent_at = datetime.now()

    def __str__(self):
        return f"{self.description}, {self.amount} {self.currency}, spent at {self.spent_at.isoformat()}"

    def to_dict(self):
        return {
            Spending.Keys.description: self.description,
            Spending.Keys.amount: self.amount,
            Spending.Keys.spent_at: self.spent_at.isoformat(),
            Spending.Keys.currency: self.currency
        }

    @staticmethod
    def is_valid(data: dict, raise_exception: bool = False) -> bool:
        """
        Validating the mandatory fields and checking the format
        """
        errors = {}

        for field in Spending.mandatory_fields:
            if data.get(field) is None or data.get(field) == "":
                errors[field] = ["This field is required."]

        amount = data.get(Spending.Keys.amount)
        if amount:
            if not is_positive_float(amount):
                errors[Spending.Keys.amount] = [
                    "Should be a positive number."
                ]

        currency = data.get(Spending.Keys.currency)
        if currency:
            if currency not in [Currency.HUF, Currency.USD]:
                errors[Spending.Keys.currency] = ["Not supported currency."]

        if raise_exception and any(errors):
            raise ValidationError(errors)

        return not any(errors)
