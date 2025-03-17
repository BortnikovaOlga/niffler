import time

import pytest
from selene import have
from model.web_spend import Spend, Category
from page.marks import TestData
from test.helpers import assert_with_allure

TEST_CATEGORY_NAME = "образование"
TEST_CATEGORY = Category(name=TEST_CATEGORY_NAME)


class TestSpendDB:

    @TestData.category(Category.random())
    def test_spend_when_add_in_ui_then_added_in_db(self, category, spend_db, app_user, main_page, delete_spends):
        """Проверка, что расход сохраняется в БД, когда добавляется через UI."""
        test_spend = Spend.random(category=category.name)
        user_name, _ = app_user

        main_page \
            .toolbar.new_spending_click() \
            .input_spending(test_spend) \
            .save_click()

        time.sleep(3)  # нужна задержка, следющий запрос в бд отработает раньше, чем отработет запрос с фронта
        result = spend_db.get_user_spends(user_name)

        assert_with_allure(
            result is not None, "Проверка, что результат запроса не пуст"
        )
        assert_with_allure(
            test_spend in result, "Проверка, что тестовая запись есть в БД"
        )

    @TestData.category(TEST_CATEGORY)
    @TestData.spends([Spend.random(category=TEST_CATEGORY_NAME)])
    def test_spend_when_delete_in_ui_then_deleted_from_db(self, category, spends, spend_db, app_user, main_page):
        """Проверка, что расходов нет в БД, когда расходы удаляются через UI."""
        user_name, _ = app_user

        main_page \
            .table_first.should(have.text(spends[0].description))
        main_page \
            .delete_spendings()

        time.sleep(2)
        result = spend_db.get_user_spends(user_name)

        assert_with_allure(
            not result, "Проверка, что результат запроса пуст"
        )

    @TestData.category(TEST_CATEGORY)
    @TestData.spends([Spend.random(category=TEST_CATEGORY_NAME, days_delta=2)])
    def test_spend_when_edit_in_ui_then_updated_in_db(self, category, spends, spend_db, app_user, main_page):
        """Проверка, что расход обновляется в БД, когда обновляется через UI."""
        user_name, _ = app_user
        update = Spend.random(category=category.name)

        main_page \
            .table_first.should(have.text(spends[0].description))
        main_page \
            .edit_first_click() \
            .input_spending(update) \
            .save_click()

        time.sleep(2)
        result = spend_db.get_user_spends(user_name)

        assert_with_allure(
            result is not None, "Проверка, что результат запроса не пуст"
        )
        assert_with_allure(
            update in result, "Проверка, что тестовая запись есть в БД"
        )

    def test_category_when_add_in_ui_then_added_in_db_and_not_archived(self,
                                                                       new_category,
                                                                       spend_db, app_user,
                                                                       profile_page):
        """Проверка, что категория добавляется в БД и не архивна, когда добавляется через UI."""
        user_name, _ = app_user

        profile_page \
            .input_category(new_category.name)

        time.sleep(4)
        result = spend_db \
            .get_category_by_name(new_category.name, user_name)

        assert_with_allure(
            result is not None, "Проверка, что результат запроса не пуст"
        )
        assert_with_allure(
            not result.archived, "Проверка, что запись без признака архива"
        )

    @pytest.fixture()
    def teardown_delete_category(self, category, spend_db):
        """teardown - удаляется категория."""
        yield category
        spend_db.delete_category(category.id)

    @TestData.category(Category.random())
    def test_category_when_archive_in_ui_then_archived_true_in_db(self, category, spend_db, profile_page):
        """Проверка, что категория становится архивной в БД, когда перемещается в архив через UI."""
        profile_page \
            .archive_category(category.name)

        time.sleep(2)
        result = spend_db \
            .get_category(category.id)

        assert_with_allure(
            result is not None, "Проверка, что результат запроса не пуст"
        )
        assert_with_allure(
            result.archived, "Проверка, что запись c признаком архива"
        )

    @TestData.category(Category.random())
    def test_category_when_unarchive_in_ui_then_archived_false_in_db(self, category, spend_db, profile_page):
        """Проверка, что категория становится не архивной(archived=false) в БД, когда возвращается из архива через UI"""
        spend_db.set_archive_category(category.id)

        profile_page \
            .show_archived_click() \
            .unarchive_category(category.name)

        time.sleep(2)
        result = spend_db \
            .get_category(category.id)

        assert_with_allure(
            result is not None, "Проверка, что результат запроса не пуст"
        )
        assert_with_allure(
            not result.archived, "Проверка, что запись без признака архива"
        )
