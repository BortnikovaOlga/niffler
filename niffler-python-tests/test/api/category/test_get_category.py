from page.marks import TestData
from test.helpers import assert_with_allure
from allure import feature, story, tag

TEST_CATEGORIES = ["образование", "хобби", "проезд", "одежда"]


@tag("API")
@feature("CRUD, categories-controller")
@story("GET")
class TestApiGetCategory:

    @TestData.categories(TEST_CATEGORIES)
    def test_get_all_categories(self, categories, categories_api, spend_db, envs):
        """Проверка получения всех категорий."""
        categories = categories_api \
            .get_categories()
        categories_db = spend_db \
            .get_user_categories(envs.test_username)
        assert_with_allure(
            set([c.name for c in categories]) == set([c.name for c in categories_db]),
            f"Получили из бд {categories_db}, \n получили из апи {categories}")

    def test_get_category_empty(self, categories_api):
        """Проверка получения пустого списка, когда у пользователя нет категорий."""
        categories = categories_api \
            .get_categories()
        assert_with_allure(
            categories == [], "Ожидается пустой список")
