import pytest
from selene import have
from model.web_spend import Spend, Category, str_total
from page.marks import TestData
from allure import feature, story, tag

TEST_DELETE_CATEGORY = Category.random()
TEST_EDIT_CATEGORY = Category.random()


@tag("UI")
@feature("Ведение расходов")
@story("Управление записями расходов")
class TestSpendings:

    def test_spending_title_exists(self, main_page):
        """Проверка, на главной странице есть заголовок истории расходов."""
        main_page \
            .spendings_title.should(have.text('History of Spendings'))

    @TestData.category(Category.random())
    def test_cancel_add_spend(self, category, main_page):
        """Проверка, что при добавлении расхода есть отмена добавления, расход не добавляется."""
        test_spend = Spend.random(category=category.name)
        main_page \
            .toolbar.new_spending_click() \
            .input_spending(test_spend) \
            .cancel_click()
        main_page \
            .check_no_spends()

    @pytest.fixture
    def delete_spends(self, spend_db, envs):
        yield
        spend_db.delete_spends_by_user(envs.test_username)

    @TestData.category(Category.random())
    def test_add_spend(self, category, main_page, delete_spends):
        """Проверка, что при добавлении расход сохраняется и присутствует на странице в истории расходов."""
        test_spend = Spend.random(category=category.name)
        main_page \
            .toolbar.new_spending_click() \
            .input_spending(test_spend) \
            .save_click()
        main_page \
            .check_table_have_text(test_spend.category.name) \
            .check_table_have_text(test_spend.description)

    @TestData.category(TEST_DELETE_CATEGORY)
    @TestData.spends([Spend.random(category=TEST_DELETE_CATEGORY.name)])
    def test_delete_spend(self, category, spends, main_page):
        """Проверка, что пункт расхода удаляется из истории."""
        test_spend = spends[0]
        main_page \
            .check_table_have_text(test_spend.description) \
            .delete_spendings() \
            .check_no_spends()

    @TestData.category(TEST_EDIT_CATEGORY)
    @TestData.spends([Spend.random(category=TEST_EDIT_CATEGORY.name)])
    def test_edit_spend(self, category, spends, main_page):
        """Проверка, что расход редактируется."""
        test_spend = spends[0]
        update = Spend.random(category=category.name)

        main_page \
            .check_table_have_text(test_spend.description) \
            .edit_first_click() \
            .input_spending(update) \
            .save_click()
        main_page \
            .check_table_have_text(str_total(update.amount)) \
            .check_table_have_text(update.description)
