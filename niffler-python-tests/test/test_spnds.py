from selene import have
from page.marks import TestData

TEST_CATEGORY = "образование"


class TestSpendings:
    test_spend = {
        "amount": "58000",
        "description": "QA.GURU Python Advanced 2",
        "category": {"name": TEST_CATEGORY},
        "spendDate": "2025-02-17T18:39:27.955Z",
        "currency": "RUB"
    }

    def test_spending_title_exists(self, main_page):
        """Проверка, на главной странице есть заголовок истории расходов."""
        main_page \
            .spendings_title.should(have.text('History of Spendings'))

    @TestData.category(TEST_CATEGORY)
    def test_spending_may_be_cancel(self, category, main_page):
        """Проверка, что при добавлении расхода есть отмена добавления, расход не добавляется."""
        main_page \
            .toolbar.new_spending_click() \
            .input_spending(self.test_spend) \
            .cancel.click()
        main_page.spendings.should(have.text("There are no spendings"))

    def test_spending_should_be_add(self, main_page):
        """Проверка, что при добавлении расход сохраняется и присутствует в истории расходов."""
        main_page \
            .toolbar.new_spending_click() \
            .input_spending(self.test_spend) \
            .save.click()
        main_page \
            .table_first.should(have.text(TEST_CATEGORY).and_(have.text(self.test_spend["amount"]).and_(have.text(
            self.test_spend["description"]))))

    @TestData.category(TEST_CATEGORY)
    @TestData.spends(test_spend)
    def test_spending_should_be_deleted(self, category, spends, main_page):
        """Проверка, что пункт расхода удаляется из истории."""
        main_page \
            .table_first.should(have.text("QA.GURU Python Advanced 2"))
        main_page \
            .delete_spendings() \
            .spendings.should(have.text("There are no spendings"))
