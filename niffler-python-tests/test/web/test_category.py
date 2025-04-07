from model.web_spend import Category
from page.marks import Pages, TestData
from allure import feature, story, tag


@tag("UI")
@feature("Профиль")
@story("Управление категорями расходов")
@Pages.profile_page
class TestCategory:

    @TestData.category(Category.random())
    def test_category_should_be_present(self, category, profile_page):
        """Проверка, что категория присутствует на странице, если она есть в бд и не архивна."""
        profile_page \
            .check_category_item_is_visible(category.name)

    def test_category_should_be_added(self, profile_page, new_category):
        """Проверка, что категория добавляется через UI-интерфейс."""
        profile_page \
            .input_category(new_category.name) \
            .check_category_item_is_visible(new_category.name)

    @TestData.category(Category.random())
    def test_category_should_be_archived(self, category, profile_page):
        """Проверка, что категория перемещается в архив и отображается в архиве."""
        profile_page \
            .archive_category(category.name) \
            .check_category_item_is_not_visible(category.name)
        profile_page \
            .show_archived_click() \
            .check_category_item_is_visible(category.name)
