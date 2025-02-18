from selene import browser, have
from page.marks import Pages, TestData
from page.pages import SpendingTable, MainPage, Dialog, Toolbar, SpendingPage


TEST_CATEGORY = "образование"


@Pages.main_page
class TestSpendings:

    def test_spending_title_exists(self):
        """Проверка, на главной странице есть заголовок истории расходов."""
        browser.element(MainPage.spendings_title).should(have.text('History of Spendings'))

    @TestData.category(TEST_CATEGORY)
    @TestData.spends({
        "amount": "58000.0",
        "description": "QA.GURU Python Advanced 2",
        "category": {"name": TEST_CATEGORY},
        "spendDate": "2025-02-17T18:39:27.955Z",
        "currency": "RUB"
    })
    def test_spending_should_be_deleted(self, category, spends):
        """Проверка, что пункт расхода удаляется из истории."""
        browser.element(SpendingTable.first_row).should(have.text("QA.GURU Python Advanced 2"))
        browser.element(SpendingTable.title_checkbox).click()
        browser.element(MainPage.delete_button).click()
        browser.element(Dialog.confirm).click()

        browser.all(SpendingTable.rows).should(have.size(0))
        browser.element(MainPage.spendings).should(have.text("There are no spendings"))

    @TestData.category(TEST_CATEGORY)
    def test_spending_may_be_cancel(self, category):
        """Проверка, что при добавлении расхода есть отмена добавления, расход не добавляется."""
        browser.element(Toolbar.new_spending).click()
        browser.element(SpendingPage.amount).set_value("1001")
        browser.element(SpendingPage.description).set_value("1001")
        browser.element(SpendingPage.category(TEST_CATEGORY)).click()
        browser.element(SpendingPage.cancel).click()

        browser.all(SpendingTable.rows).should(have.size(0))

    def test_spending_should_be_add(self):
        """Проверка, что при добавлении расход сохраняется и присутствует в истории расходов."""
        browser.element(Toolbar.new_spending).click()
        browser.element(SpendingPage.amount).set_value("58000")
        browser.element(SpendingPage.description).set_value("QA.GURU Python Advanced 2")
        browser.element(SpendingPage.category(TEST_CATEGORY)).click()
        browser.element(SpendingPage.save).click()

        browser.element(SpendingTable.first_row).should(have.text(TEST_CATEGORY))
        browser.element(SpendingTable.first_row).should(have.text('58000'))
        browser.element(SpendingTable.first_row).should(have.text("QA.GURU Python Advanced 2"))
