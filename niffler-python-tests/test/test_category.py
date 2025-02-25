from selene import be
from page.marks import Pages, TestData
from faker import Faker

fake = Faker()


@Pages.profile_page
class TestCategory:

    @TestData.category("hobby")
    def test_category_should_be_present(self, category, profile_page):
        """Проверка, что категория присутствует на странице, если она есть в бд и не архивна."""
        profile_page \
            .category_item(category).should(be.visible)

    def test_category_should_be_added(self, profile_page):
        """Проверка, что категория добавляется через UI-интерфейс."""
        category = fake.word()
        profile_page \
            .input_category(category) \
            .category_item(category).should(be.visible)

    @TestData.category(fake.word())
    def test_category_should_be_archived(self, category, profile_page):
        """Проверка, что категория перемещается в архив и отображается в архиве."""
        profile_page \
            .archive_category(category) \
            .category_item(category).should(be.not_.visible)
        profile_page \
            .show_archived_click() \
            .category_item(category).should(be.visible)
