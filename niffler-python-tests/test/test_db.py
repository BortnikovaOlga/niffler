import time

import pytest
from selene import have
from model.web_spend import Spend, Category
from page.marks import TestData

TEST_CATEGORY_NAME = "образование"
TEST_CATEGORY = Category(name=TEST_CATEGORY_NAME)


class TestSpendingsDB:

    def test_spending_should_be_add_db(self, main_page, spend_db, app_user):
        """Проверка, что при добавлении расход сохраняется в БД."""
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
    def test_spending_should_be_deleted_db(self, category, spends, main_page, spend_db, app_user):
        """Проверка, что пункт расхода удаляется из БД, когда удаляется через UI."""
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
    def test_spending_edit_db(self, category, spends, main_page, spend_db, app_user):
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

    def test_category_should_be_added_db(self, profile_page, spend_db, app_user):
        """Проверка, что категория добавляется в БД и не архивна, когда добавляется через UI."""
        user_name, _ = app_user
        category = Category.random()

        result = spend_db.get_user_categories(user_name)
        assert category not in result

        profile_page\
            .input_category(category.name)

        time.sleep(3)
        result = spend_db.get_user_categories(user_name)
        idx = result.index(category)

        assert idx is not None and not result[idx].archived

        spend_db.delete_category(result[idx].id)

    @TestData.category(Category.random())
    def test_category_should_be_archived_db(self, category, profile_page, spend_db, app_user):
        """Проверка, что категория изменяет статус в БД на архив, когда перемещается в архив через UI."""
        user_name, _ = app_user

        profile_page \
            .archive_category(category.name)

        time.sleep(4)
        result = spend_db.get_user_categories(user_name)
        idx = result.index(category)

        assert idx is not None and result[idx].archived

        spend_db.delete_category(result[idx].id)

    @pytest.fixture()
    def archive_category(self, category, spend_db):
        """(setup) добавляется архивная категория (из параметров теста), (teardown) удаляется."""
        spend_db.set_archive_category(category.id)
        yield category
        spend_db.delete_category(category.id)

    @TestData.category(Category.random())
    def test_category_should_be_re_archived_db(self, archive_category, profile_page, spend_db, app_user):
        """Проверка, что категория изменяет статус в БД , когда возврящается из архива через UI."""
        user_name, _ = app_user

        profile_page \
            .show_archived_click() \
            .unarchive_category(archive_category.name)

        time.sleep(2)
        result = spend_db.get_user_categories(user_name)
        idx = result.index(archive_category)

        assert idx is not None and not result[idx].archived
