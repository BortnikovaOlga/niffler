from selene import browser, be
from selenium.webdriver.common.keys import Keys
from page.marks import Pages, TestData
from page.pages import ProfilePage, Dialog


@Pages.profile_page
class TestCategory:
    TEST_CATEGORY = "хобби"

    @TestData.category(TEST_CATEGORY)
    def test_category_should_be_present(self, category, profile_page):
        """Категория присутствует на странице, если она есть в бд и не архивна."""
        browser.element(ProfilePage.category_item(category)).should(be.present)

    def test_category_should_be_added(self):
        """Категория должна добавляться через UI-интерфейс."""
        category = "путешествия"
        browser.element(ProfilePage.category).set_value(category).send_keys(Keys.ENTER)

        browser.element(ProfilePage.category_item(category)).should(be.present)

    @TestData.category(TEST_CATEGORY)
    def test_category_should_be_archived(self, category, profile_page):
        """Категория должна премещаться в архив."""
        browser.element(ProfilePage.archive_button(category)).click()
        browser.element(Dialog.confirm).click()

        browser.element(ProfilePage.category_item(category)).should(be.not_.present)
