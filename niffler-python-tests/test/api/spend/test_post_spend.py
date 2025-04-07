from http import HTTPStatus

import pytest
from requests import HTTPError

from model.web_spend import Category, Spend
from page.marks import TestData
from test.helpers import assert_with_allure
from allure import feature, story, tag

TEST_CATEGORY = Category.random()
TEST_SPEND_ZERO_AMOUNT = Spend.random(category=TEST_CATEGORY.name)
TEST_SPEND_ZERO_AMOUNT.amount = 0
TEST_SPEND_NULL_CATEGORY = Spend.random(category=TEST_CATEGORY.name)
TEST_SPEND_NULL_CATEGORY.category = None
TEST_SPEND_NULL_DATE = Spend.random(category=TEST_CATEGORY.name)
TEST_SPEND_NULL_DATE.spendDate = None


@tag("API")
@feature("CRUD, spend-controller")
@story("POST")
class TestApiPostSpend:

    @pytest.fixture
    def delete_spends(self, spend_db, envs):
        yield
        spend_db.delete_spends_by_user(envs.test_username)

    @TestData.category(TEST_CATEGORY)
    def test_post_spend(self, category, spends_api, delete_spends):
        """Проверка записи расхода с валидными данными, проверка ответа апи."""
        spend = Spend.random(category=TEST_CATEGORY.name)
        response = spends_api \
            .add_spend(spend)
        assert_with_allure(
            response == spend, f"В ответе ожидается {spend}, получено {response}")

    @TestData.category(TEST_CATEGORY)
    def test_post_spend_check_db(self, category, spends_api, spend_db, delete_spends):
        """Проверка записи расхода с валидными данными, проверка записи в бд."""
        spend = Spend.random(category=TEST_CATEGORY.name)
        response = spends_api \
            .add_spend(spend)
        assert response
        spend_db = spend_db \
            .get_spend_by_id(response.id)
        assert_with_allure(
            spend_db == spend, f"В БД ожидается {spend}, получено {spend_db}")

    @TestData.category(TEST_CATEGORY)
    @pytest.mark.parametrize("spend", [
        Spend.random(category=TEST_CATEGORY.name, currency="  "),  # USD, если ""
        Spend.random(category=TEST_CATEGORY.name, currency="RRR"),
        TEST_SPEND_ZERO_AMOUNT,
        TEST_SPEND_NULL_DATE,
        TEST_SPEND_NULL_CATEGORY
    ])
    def test_post_invalid_spend_data(self, category, spend, spends_api, delete_spends):
        with pytest.raises(HTTPError) as e:
            spends_api \
                .add_spend(spend)
        resp_status_code = e.value.response.status_code
        assert_with_allure(
            resp_status_code == HTTPStatus.BAD_REQUEST, f"Ожидается 400 КО, получен {resp_status_code}")
