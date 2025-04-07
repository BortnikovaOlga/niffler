from http import HTTPStatus

import pytest
from requests import HTTPError

from model.web_spend import Category, Spend
from page.marks import TestData
from test.helpers import assert_with_allure
from allure import feature, story, tag

TEST_CATEGORY = Category.random()


@tag("API")
@feature("CRUD, spend-controller")
@story("GET")
class TestApiGetSpends:

    def test_get_empty_spends(self, spends_api):
        """Проверка при отсутствующих затратах."""
        result = spends_api.get_all_spends()
        assert_with_allure(
            result == [], "Ожидается пустой массив в ответе."
        )

    @TestData.category(TEST_CATEGORY)
    @TestData.spends([Spend.random(category=TEST_CATEGORY.name)])
    def test_get_all_spends(self, category, spends, spends_api):
        """Проверка получения всех затрат."""
        result = spends_api.get_all_spends()
        assert_with_allure(
            result == spends, f"В ответе ожидается массив \n {spends}, \n а получен\n {result}."
        )

    @TestData.category(TEST_CATEGORY)
    @TestData.spends([Spend.random(category=TEST_CATEGORY.name, currency='RUB', days_delta=6, min_days_delta=2)])
    def test_get_all_spends_with_filter(self, category, spends, spends_api):
        """Провкрка получения затрат с фильтрами."""
        filters = {"filterCurrency": spends[0].currency, "filterPeriod": "WEEK"}
        result = spends_api.get_all_spends(params=filters)
        assert_with_allure(
            result == spends, f"В ответе ожидается массив \n {spends}, \n а получен\n {result}."
        )

    @TestData.category(TEST_CATEGORY)
    @TestData.spends([Spend.random(category=TEST_CATEGORY.name)])
    def test_get_spend_by_id(self, category, spends, spends_api):
        """Проверка получения расхода по ид."""
        result = spends_api \
            .get_by_id(spends[0].id)
        assert_with_allure(
            result == spends[0], "В ответе ожидается запись из предусловий."
        )

    def test_get_spend_by_invalid_id(self, spends_api):
        """Проверка получения расхода по невалидному ид."""
        with pytest.raises(HTTPError) as e:
            spends_api.get_by_id("not_valid_uuid")
        assert_with_allure(
            e.value.response.status_code == HTTPStatus.NOT_FOUND, "Ожидается 404 КО")
