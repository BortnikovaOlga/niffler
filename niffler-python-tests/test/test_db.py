import time

import pytest
from selene import have
from model.web_spend import Spend, Category
from page.marks import TestData

TEST_CATEGORY_NAME = "образование"
TEST_CATEGORY = Category(name=TEST_CATEGORY_NAME)


class TestSpendDB:

    def test_spend_when_add_in_ui_then_added_in_db(self, main_page, spend_db, app_user):
        """Проверка, что расход сохраняется в БД, когда добавляется через UI."""
        test_spend = Spend.random(category=TEST_CATEGORY_NAME)
        user_name, _ = app_user

        main_page \
            .toolbar.new_spending_click() \
            .input_spending(test_spend) \
            .save_click()

        time.sleep(2)  # нужна задержка, следющий запрос в бд отработает раньше, чем отработет запрос с фронта
        result = spend_db.get_user_spends(user_name)

        assert result and test_spend in result

    @TestData.category(TEST_CATEGORY)
    @TestData.spends([Spend.random(category=TEST_CATEGORY_NAME)])
    def test_spend_when_delete_in_ui_then_deleted_from_db(self, category, spends, main_page, spend_db, app_user):
        """Проверка, что расходов нет в БД, когда расходы удаляются через UI."""
        user_name, _ = app_user

        main_page \
            .table_first.should(have.text(spends[0].description))
        main_page \
            .delete_spendings()

        time.sleep(2)
        result = spend_db.get_user_spends(user_name)

        assert not result

    @TestData.category(TEST_CATEGORY)
    @TestData.spends([Spend.random(category=TEST_CATEGORY_NAME, days_delta=2)])
    def test_spend_when_edit_in_ui_then_updated_in_db(self, category, spends, main_page, spend_db, app_user):
        """Проверка, что расход обновляется в БД, когда обновляется через UI."""
        user_name, _ = app_user
        update = Spend.random(category="hobby")

        main_page \
            .table_first.should(have.text(spends[0].description))
        main_page \
            .edit_first_click() \
            .input_spending(update) \
            .save_click()

        time.sleep(5)
        result = spend_db.get_user_spends(user_name)

        assert result and update in result

    @pytest.fixture()
    def new_category(self, spend_db, app_user):
        """в setup проверяется, что такой категории нет в бд, в teardown - удаляется."""
        user_name, _ = app_user
        category = Category.random()
        result = spend_db.get_category_by_name(category.name, user_name)
        assert not result

        yield category

        result = spend_db.get_category_by_name(category.name, user_name)
        if result:
            spend_db.delete_category(result.id)

    def test_category_when_add_in_ui_then_added_in_db_and_not_archived(self, profile_page, new_category, spend_db,
                                                                       app_user):
        """Проверка, что категория добавляется в БД и не архивна, когда добавляется через UI."""
        user_name, _ = app_user

        profile_page \
            .input_category(new_category.name)

        time.sleep(3)
        result = spend_db \
            .get_category_by_name(new_category.name, user_name)
        assert result is not None
        assert not result.archived

    @pytest.fixture()
    def t_category(self, category, spend_db):
        """в teardown - удаляется категория."""
        yield category
        spend_db.delete_category(category.id)

    @TestData.category(Category.random())
    def test_category_when_archive_in_ui_then_archived_true_in_db(self, t_category, profile_page, spend_db):
        """Проверка, что категория становится архивной в БД, когда перемещается в архив через UI."""

        profile_page \
            .archive_category(t_category.name)

        time.sleep(3)
        result = spend_db \
            .get_category(t_category.id)

        assert result is not None
        assert result.archived

    @TestData.category(Category.random())
    def test_category_when_unarchive_in_ui_then_archived_false_in_db(self, t_category, profile_page, spend_db):
        """Проверка, что категория становится не архивной(archived=false) в БД, когда возвращается из архива через UI"""
        spend_db.set_archive_category(t_category.id)

        profile_page \
            .show_archived_click() \
            .unarchive_category(t_category.name)

        time.sleep(3)
        result = spend_db \
            .get_category(t_category.id)

        assert result is not None
        assert not result.archived
