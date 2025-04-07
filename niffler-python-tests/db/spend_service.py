from typing import Sequence
from uuid import UUID

from sqlalchemy import create_engine, Engine, event
from sqlalchemy.exc import NoResultFound

from sqlmodel import Session, select, delete
from allure import attach, step
from allure_commons.types import AttachmentType
from db.spend_models import Spend, Category
from model import web_spend


class SpendDbService:
    engine: Engine

    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        event.listen(self.engine, "do_execute", fn=self.attach_sql)

    @staticmethod
    def attach_sql(cursor, statement, parameters, context):
        statement_with_params = statement % parameters
        name = statement.split(" ")[0] + " " + context.engine.url.database
        attach(statement_with_params, name=name, attachment_type=AttachmentType.TEXT)

    @step("DB вернуть все категории для пользователя")
    def get_user_categories(self, username: str) -> Sequence[web_spend.Category]:
        """возвращает все категории для пользователя."""
        with Session(self.engine) as session:
            statement = select(Category).where(Category.username == username)
            result = session.exec(statement).all()
            if result:
                return [web_spend.Category.model_validate(category.model_dump()) for category in result]

    @step("DB получить информацию по названию категории ")
    def get_category_by_name(self, category_name: str, username: str) -> web_spend.Category | None:
        """возвращает информацию по категории для определенного пользователя."""
        with Session(self.engine) as session:
            statement = select(Category).where(Category.name == category_name).where(Category.username == username)
            try:
                result = session.exec(statement).one()
                return web_spend.Category.model_validate(result.model_dump())
            except NoResultFound:
                return None

    @step("DB получить информацию по ид категории")
    def get_category(self, category_id: str | UUID) -> web_spend.Category | None:
        """возвращает информацию по ид категории."""
        with Session(self.engine) as session:
            category = session.get(Category, str(category_id))
            if category:
                return web_spend.Category.model_validate(category.model_dump())

    @step("DB удалить категорию по ид")
    def delete_category(self, category_id: str | UUID):
        with Session(self.engine) as session:
            category = session.get(Category, str(category_id))
            session.delete(category)
            session.commit()

    @step("DB удалить все траты пользователя")
    def delete_spends_by_user(self, username: str):
        with Session(self.engine) as session:
            statement = delete(Spend).where(Spend.username == username)
            session.exec(statement)
            session.commit()

    @step("DB поставить признак архив для категории")
    def set_archive_category(self, category_id):
        with Session(self.engine) as session:
            category = session.get(Category, str(category_id))
            category.archived = True
            session.add(category)
            session.commit()

    @step("DB получить все траты пользователя")
    def get_user_spends(self, username: str) -> Sequence[web_spend.Spend]:
        with Session(self.engine) as session:
            statement = select(Spend, Category) \
                .join(Category, Spend.category_id == Category.id) \
                .where(Spend.username == username)
            results = session.exec(statement).all()
            if results:
                return [web_spend.Spend.model_validate({**spend.model_dump(), "category": category.model_dump()}) \
                        for spend, category in results]

    def get_spend_by_id(self, spend_id: str | UUID) -> web_spend.Spend:
        with Session(self.engine) as session:
            spend = session.get(Spend, str(spend_id))
            if spend:
                category = session.get(Category, str(spend.category_id))
                return web_spend.Spend.model_validate({**spend.model_dump(), "category": category.model_dump()})
