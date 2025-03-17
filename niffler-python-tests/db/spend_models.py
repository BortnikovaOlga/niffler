from datetime import datetime
from sqlmodel import SQLModel, Field


class Category(SQLModel, table=True):
    __tablename__ = 'category'
    id: str | None = Field(default=None, primary_key=True)
    name: str
    username: str
    archived: bool


class Spend(SQLModel, table=True):
    __tablename__ = 'spend'
    id: str | None = Field(default=None, primary_key=True)
    username: str
    amount: float
    description: str
    category_id: str = Field(foreign_key="category.id")
    spend_date: datetime
    currency: str
