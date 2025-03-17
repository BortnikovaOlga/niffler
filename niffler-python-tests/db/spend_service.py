from typing import Sequence
from uuid import UUID

from sqlalchemy import create_engine, Engine
from sqlalchemy.exc import NoResultFound

from sqlmodel import Session, select

from db.spend_models import Spend, Category
from model import web_spend


class SpendDbService:
    engine: Engine

    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)

    def get_user_categories(self, username: str) -> Sequence[web_spend.Category]:
        """возвращает все категории для пользователя."""
        with Session(self.engine) as session:
            statement = select(Category).where(Category.username == username)
            result = session.exec(statement).all()
            if result:
                return [web_spend.Category.model_validate(category.model_dump()) for category in result]

    def get_category_by_name(self, category_name: str, username: str) -> web_spend.Category | None:
        """возвращает информацию по категории для определенного пользователя."""
        with Session(self.engine) as session:
            statement = select(Category).where(Category.name == category_name).where(Category.username == username)
            try:
                result = session.exec(statement).one()
                return web_spend.Category.model_validate(result.model_dump())
            except NoResultFound:
                return None

    def get_category(self, category_id: str | UUID) -> web_spend.Category | None:
        """возвращает информацию по ид категории."""
        with Session(self.engine) as session:
            category = session.get(Category, str(category_id))
            if category:
                return web_spend.Category.model_validate(category.model_dump())

    def delete_category(self, category_id: str | UUID):
        with Session(self.engine) as session:
            category = session.get(Category, str(category_id))
            session.delete(category)
            session.commit()

    def set_archive_category(self, category_id):
        with Session(self.engine) as session:
            category = session.get(Category, str(category_id))
            category.archived = True
            session.add(category)
            session.commit()

    def get_user_spends(self, username: str) -> Sequence[web_spend.Spend]:
        with Session(self.engine) as session:
            statement = select(Spend, Category) \
                .join(Category, Spend.category_id == Category.id) \
                .where(Spend.username == username)
            results = session.exec(statement).all()
            if results:
                return [web_spend.Spend.model_validate({**spend.model_dump(), "category": category.model_dump()}) \
                        for spend, category in results]
