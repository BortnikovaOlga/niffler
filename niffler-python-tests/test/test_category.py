from selene import be

from model.web_spend import Category
from page.marks import Pages, TestData
from faker import Faker

fake = Faker()

TEST_CATEGORY_NAME = "образование"
TEST_CATEGORY = Category(name=TEST_CATEGORY_NAME)


@Pages.profile_page
class TestCategory:

    @TestData.category(TEST_CATEGORY)
    def test_category_should_be_present(self, category, profile_page):
        """Проверка, что категория присутствует на странице, если она есть в бд и не архивна."""
        profile_page \
            .category_item(category.name).should(be.visible)

    def test_category_should_be_added(self, profile_page):
        """Проверка, что категория добавляется через UI-интерфейс."""
        category = Category.random()
        profile_page \
            .input_category(category.name) \
            .category_item(category.name).should(be.visible)

    @TestData.category(Category.random())
    def test_category_should_be_archived(self, category, profile_page):
        """Проверка, что категория перемещается в архив и отображается в архиве."""
        profile_page \
            .archive_category(category.name) \
            .category_item(category.name).should(be.not_.visible)
        profile_page \
            .show_archived_click() \
            .category_item(category.name).should(be.visible)
