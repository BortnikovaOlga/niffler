import pytest
import allure
from http import HTTPStatus
from requests import HTTPError
from model.web_spend import Category
from page.marks import TestData
from test.helpers import assert_with_allure
from allure import feature, story, tag


@tag("API")
@feature("CRUD, categories-controller")
@story("PATCH")
class TestApiPatchCategory:

    @TestData.category(Category.random())
    def test_update_category_name(self, category, categories_api):
        """Проверка редактирования имени категории, проверка ответа на запрос."""
        update = Category.random()
        update.id = category.id
        result = categories_api \
            .update_category(update)
        assert_with_allure(
            result == update, f"Ожидается ответ {update}, получен {result}")

    @TestData.category(Category.random())
    def test_update_category_name_and_check_db(self, category, categories_api, spend_db):
        """Проверка редактирования категории, проверка результата в бд."""
        update = Category.random()
        update.id = category.id
        categories_api \
            .update_category(update)
        category_db = spend_db \
            .get_category(category.id)
        assert_with_allure(
            category_db == update, f"Ожидается ответ {update}, получен из бд {category_db}")

    @TestData.category(Category.random())
    def test_update_category_archived(self, category, categories_api, spend_db):
        """Проверка перемещения категории в архив."""
        category.archived = True
        result = categories_api \
            .update_category(category)
        category_db = spend_db \
            .get_category(category.id)
        assert_with_allure(
            result.archived and category_db.archived, "Ожидается признак архива в ответе апи и в бд")

    @allure.issue("при обновлении название категории не валидируется")
    @pytest.mark.xfail(reason="баг в апи, все запросы выполняются с 200 КО")
    @TestData.category(Category.random())
    @pytest.mark.parametrize("update", [
        Category(name=""),
        Category(name="   "),
        Category(name="x"),
        Category(name="X" * 51)
    ])
    def test_update_category_with_invalid_data(self, category, categories_api, update):
        """Проверка, что при обновлении с невалидными данными возникает ошибка BAD_REQUEST."""
        category.name = update.name
        with pytest.raises(HTTPError) as e:
            categories_api \
                .update_category(category)
        resp_status_code = e.value.response.status_code
        assert_with_allure(
            resp_status_code == HTTPStatus.BAD_REQUEST, f"Ожидается 400 КО, получен {resp_status_code}")
