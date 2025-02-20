from selene import be
from page.marks import Pages, TestData


@Pages.profile_page
class TestCategory:
    TEST_CATEGORY = "hobby"

    @TestData.category(TEST_CATEGORY)
    def test_category_should_be_present(self, category, profile_page):
        """Категория присутствует на странице, если она есть в бд и не архивна."""
        profile_page \
            .category_item(category).should(be.present)

    def test_category_should_be_added(self, profile_page):
        """Категория должна добавляться через UI-интерфейс."""
        category = "путешествия"
        profile_page \
            .input_category(category) \
            .category_item(category).should(be.present)

    @TestData.category(TEST_CATEGORY)
    def test_category_should_be_archived(self, category, profile_page):
        """Категория должна премещаться в архив."""
        profile_page \
            .archive_category(category) \
            .category_item(category).should(be.not_.present)
