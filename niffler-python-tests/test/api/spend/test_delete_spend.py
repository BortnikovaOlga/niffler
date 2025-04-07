import allure
import pytest
from requests import HTTPError
from http import HTTPStatus
from model.web_spend import Category, Spend
from page.marks import TestData
from test.helpers import assert_with_allure
from allure import feature, story, tag

TEST_CATEGORY = Category.random()


@tag("API")
@feature("CRUD, spend-controller")
@story("DELETE")
class TestApiDeleteSpends:

    @TestData.category(TEST_CATEGORY)
    def test_remove_spend_by_id(self, category, spends_api):
        """Проверка удаления по валидному ид."""
        spend = Spend.random(category=TEST_CATEGORY.name)
        response = spends_api \
            .add_spend(spend)
        spends_api \
            .remove_spends([response.id])
        with pytest.raises(HTTPError) as e:
            spends_api.get_by_id(response.id)
        assert_with_allure(
            e.value.response.status_code == HTTPStatus.NOT_FOUND,
            "Ожидается 404 КО, т.к расход должен быть удален")

    @allure.issue("500 КО при удалении расхода по невалидному ид")
    @pytest.mark.xfail(reason="баг в апи")
    def test_remove_spend_by_invalid_id(self, spends_api):
        """Проверка удаления по невалидному ид."""
        with pytest.raises(HTTPError) as e:
            spends_api.remove_spends(["not_valid_id"])
        resp_status_code = e.value.response.status_code
        assert_with_allure(
            resp_status_code == HTTPStatus.NOT_FOUND,
            f"Ожидается 404 КО, т.к ид расхода не существует в бд, получен {resp_status_code} КО")
