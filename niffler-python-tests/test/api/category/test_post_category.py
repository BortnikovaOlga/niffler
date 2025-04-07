import pytest
from http import HTTPStatus
from requests import HTTPError
from model.web_spend import Category
from test.helpers import assert_with_allure
from allure import feature, story, tag


@tag("API")
@feature("CRUD, categories-controller")
@story("POST")
class TestApiPostCategory:

    def test_post_category(self, new_category, categories_api):
        """Проверка ответа при создании категории."""
        category = categories_api \
            .add_category(new_category)
        assert_with_allure(
            category == new_category, f"Ожидается в ответе боди {new_category}, получено {category}")

    def test_post_category_db(self, new_category, categories_api, spend_db):
        """Проверка записи категории в бд."""
        category = categories_api \
            .add_category(new_category)
        category_db = spend_db \
            .get_category(category.id)
        assert_with_allure(
            category_db == new_category, "Ожидается, что запись в бд идентична боди в http-запросе.")

    def test_post_category_ignore_archived(self, new_category, categories_api):
        """Проверка , что при создании не учитывается признак архива."""
        new_category.archived = True
        response = categories_api \
            .add_category(new_category)
        assert_with_allure(
            not response.archived, "Ожидается, что категория при создании всегда не в архиве.")

    @pytest.mark.parametrize("category", [
        Category(name=""),
        Category(name="x"),
        Category(name="X" * 51)
    ])
    def test_post_invalid_data_category(self, categories_api, category):
        """Проверка, что при запросе на создание с невалидными данными возникает ошибка BAD_REQUEST."""
        with pytest.raises(HTTPError) as e:
            categories_api \
                .add_category(category)
        resp_status_code = e.value.response.status_code
        assert_with_allure(
            resp_status_code == HTTPStatus.BAD_REQUEST, f"Ожидается 400 КО, получен {resp_status_code}")

    # todo 8 categories
