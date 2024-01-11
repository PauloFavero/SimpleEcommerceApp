from enum import Enum


class PaymentMethod(str, Enum):
    credit_card = "credit_card"
    debit_card = "debit_card"
    cash = "cash"
