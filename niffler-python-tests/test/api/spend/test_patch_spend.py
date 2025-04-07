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
@story("PATCH")
class TestPatchSpend:

    @TestData.category(TEST_CATEGORY)
    @TestData.spends([Spend.random(category=TEST_CATEGORY.name)])
    def test_patch_spend(self, category, spends, spends_api):
        """Редактировать расход с валидными данными."""
        update = Spend.random(category=TEST_CATEGORY.name)
        update.id = spends[0].id
        result = spends_api.update(update)

        assert_with_allure(
            result == update, f"В ответе ожидается {update}, а получили {result}")

    @TestData.category(TEST_CATEGORY)
    @TestData.spends([Spend.random(category=TEST_CATEGORY.name)])
    @pytest.mark.parametrize("update", [
        Spend.random(category=TEST_CATEGORY.name, currency="  "),
        Spend.random(category=TEST_CATEGORY.name, currency="RRR"),
        TEST_SPEND_ZERO_AMOUNT,
        TEST_SPEND_NULL_DATE,
        TEST_SPEND_NULL_CATEGORY
    ])
    def test_patch_spend_with_invalid_update(self, category, spends, update, spends_api):
        """Редактировать расход с невалидными данными."""
        update.id = spends[0].id
        with pytest.raises(HTTPError) as e:
            spends_api \
                .update(update)
        assert_with_allure(
            e.value.response.status_code == HTTPStatus.BAD_REQUEST, "Ожидается 400 КО")
