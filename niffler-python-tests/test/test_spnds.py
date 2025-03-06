import datetime
from selene import have
from model.web_spend import Spend, Currency, Category, str_total
from page.marks import TestData

TEST_CATEGORY_NAME = "образование"
TEST_CATEGORY = Category(name=TEST_CATEGORY_NAME)


class TestSpendings:

    test_spend = Spend(amount=58000,
                       description="QA.GURU Python Advanced 22",
                       category=TEST_CATEGORY,
                       spendDate=datetime.date(month=2, day=27, year=2025),
                       currency=Currency.EUR.value)

    def test_spending_title_exists(self, main_page):
        """Проверка, на главной странице есть заголовок истории расходов."""
        main_page \
            .spendings_title.should(have.text('History of Spendings'))

    @TestData.category(TEST_CATEGORY)
    def test_cancel_add_spend(self, category, main_page):
        """Проверка, что при добавлении расхода есть отмена добавления, расход не добавляется."""
        main_page \
            .toolbar.new_spending_click() \
            .input_spending(self.test_spend) \
            .cancel.click()
        main_page.spendings.should(have.text("There are no spendings"))

    def test_add_spend(self, main_page):
        """Проверка, что при добавлении расход сохраняется и присутствует в истории расходов."""
        main_page \
            .toolbar.new_spending_click() \
            .input_spending(self.test_spend) \
            .save_click()
        main_page \
            .table_first.should(have.text(TEST_CATEGORY_NAME).and_(have.text(self.test_spend.description)))

    @TestData.category(TEST_CATEGORY)
    @TestData.spends([test_spend])
    def test_delete_spend(self, category, spends, main_page):
        """Проверка, что пункт расхода удаляется из истории."""
        main_page \
            .table_first.should(have.text(self.test_spend.description))
        main_page \
            .delete_spendings() \
            .spendings.should(have.text("There are no spendings"))

    @TestData.category(TEST_CATEGORY)
    @TestData.spends([test_spend])
    def test_edit_spend(self, category, spends, main_page):
        """Проверка, что расход редактируется."""
        update = Spend.random(category=TEST_CATEGORY_NAME)

        main_page \
            .table_first.should(have.text(self.test_spend.description))
        main_page \
            .edit_first_click() \
            .input_spending(update) \
            .save_click()
        main_page \
            .table_first.should(have.text(str_total(update.amount)).and_(have.text(update.description)))
        # todo check stat
