from random import randint, choice
from datetime import date, timedelta, datetime

from enum import StrEnum
from uuid import UUID
from zoneinfo import ZoneInfo

from pydantic import BaseModel, Field, AliasChoices, field_validator

from faker import Faker

fake = Faker()


class Category(BaseModel):
    id: str | UUID | None = Field(default=None)
    name: str
    archived: bool = Field(default=False)

    @staticmethod
    def random(archived=False):
        return Category(name=fake.word(), archived=archived)

    def __eq__(self, other):
        if isinstance(other, Category):
            return self.name == other.name
        return NotImplemented


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
    id: str | UUID | None = Field(default=None)
    amount: float
    description: str
    category: Category
    spendDate: date | None = Field(default=None, validation_alias=AliasChoices('spend_date', 'spendDate'))
    currency: str | None = Field(default=None)


    @field_validator("spendDate", mode='before')
    @classmethod
    def check_spendDate(cls, value):
        if isinstance(value, date):
            return value
        if isinstance(value, datetime):
            return date(value.year, value.month, value.day)
        if isinstance(value, str):
            # from dateutil import tz tz.tzlocal())
            dt = datetime.fromisoformat(value).astimezone(ZoneInfo("Europe/Moscow"))
            return dt.date()
        raise ValueError(f"spendDate validation error, for type value :{type(value)}")

    def __eq__(self, other):
        if isinstance(other, Spend):
            return (
                    self.amount == other.amount and
                    self.description == other.description and
                    self.category == other.category and
                    self.spendDate == other.spendDate and
                    self.currency == other.currency
            )
        return NotImplemented

    def amount_to_rub(self) -> float:
        return round(self.amount, 2) if self.amount == Currency.RUB else \
            round(
                self.amount * currency_rate[self.currency] / currency_rate[Currency.RUB.value], 2
            )

    @staticmethod
    def random(category: str = None, currency: str = None, days_delta=0, min_days_delta=1):
        """days_delta >= min_days_delta или равна 0."""
        d = datetime.now()
        if days_delta:
            d -= timedelta(days=randint(min_days_delta, int(days_delta)))
        if not category:
            category = Category(name=fake.word())
        if not currency:
            currency = choice([c for c in Currency])
        return Spend(amount=randint(1, 10_000),
                     description=fake.text(30),
                     category=Category(name=category),
                     spendDate=date(month=d.month, day=d.day, year=d.year),
                     currency=currency)

    @staticmethod
    def random_list(category=None, currency=None):
        return [Spend.random(category=category, currency=currency) for _ in range(randint(1, 4))]

    @staticmethod
    def list_by(categories, currencies):
        return [Spend.random(category=cat, currency=cur) for cat, cur in zip(categories, currencies)]


def total_to_rub(spends: list[Spend]) -> float:
    total = 0
    for spend in spends:
        total += spend.amount_to_rub()
    return round(total, 2)


def str_total(float_total) -> str:
    int_total = int(float_total)
    return str(float_total) if float_total >= int_total + 0.01 else str(int_total)
