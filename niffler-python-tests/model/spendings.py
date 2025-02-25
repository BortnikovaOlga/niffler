from functools import reduce
from random import randint, choice
from datetime import date, timedelta, datetime
from enum import StrEnum
from pydantic import BaseModel, Field
from faker import Faker

fake = Faker()


class Category(BaseModel):
    name: str


class Currency(StrEnum):
    RUB = 'RUB'
    KZT = 'KZT'
    EUR = 'EUR'
    USD = 'USD'


currency_rate = {
    "RUB": 0.015,
    "KZT": 0.0021,
    "EUR": 1.08,
    "USD": 1.0
}


class Spend(BaseModel):
    id: str | None = Field(default=None)
    amount: float
    description: str
    category: Category
    spendDate: date | None = Field(default=None)
    currency: str | None = Field(default=None)

    def amount_to_rub(self):
        return round(self.amount, 2) if self.amount == Currency.RUB else \
            round(
                self.amount * currency_rate[self.currency] / currency_rate[Currency.RUB.value], 2
            )

    @staticmethod
    def random(category=None, currency=None, days_delta=0, min_days_delta=1):
        """days_delta >= min_days_delta или равна 0."""
        d = datetime.now()
        if days_delta:
            d -= timedelta(days=randint(min_days_delta, days_delta))
        if not category:
            category = Category(name=fake.word())
        if not currency:
            currency = choice([c.value for c in Currency])
        return Spend(
            amount=randint(1, 10_000),
            description=fake.text(30),
            category=Category(name=category),
            spendDate=date(month=d.month, day=d.day, year=d.year),  # date.strftime('%m-%d-%Y'),
            currency=currency
        )

    @staticmethod
    def random_list(category=None, currency=None):
        return [Spend.random(category=category, currency=currency) for _ in range(randint(1, 4))]

    @staticmethod
    def list_by(categories, currencies):
        return [Spend.random(category=cat, currency=cur) for cat, cur in zip(categories, currencies)]


def total_to_rub(spends: list[Spend]):
    total = 0
    for spend in spends:
        # spend = Spend.model_validate(spend)
        total += spend.amount_to_rub()
    return round(total, 2)

def str_total(float_total):
    int_total = int(float_total)
    return str(float_total) if float_total >= int_total + 0.01 else str(int_total)