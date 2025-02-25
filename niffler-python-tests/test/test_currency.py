from selene import have
from model.spendings import Spend, Currency, total_to_rub, str_total
from page.marks import TestData, TestListData


TEST_CATEGORY = "образование"
TEST_CATEGORIES = ["образование", "хобби", "проезд", "одежда"]
TEST_CURRENCIES = [currency for currency in Currency]


@TestData.category(TEST_CATEGORY)
@TestListData.spends_by(categories=[TEST_CATEGORY] * len(TEST_CURRENCIES), currencies=TEST_CURRENCIES)
def test_spends_stat_one_category_and_currency(category, spends, main_page):
    """Проверка статистики суммы расходов по одной категории и валюте, здесь 4 кейса для разных валют."""
    main_page \
        .stat_item(category) \
        .should(have.text(str_total(total_to_rub(spends))))


@TestData.category(TEST_CATEGORY)
@TestData.spends(Spend.list_by(currencies=TEST_CURRENCIES, categories=[TEST_CATEGORY] * len(TEST_CURRENCIES)))
def test_spends_stat_one_category_and_different_currencies(category, spends, main_page):
    """Проверка статистики суммы расходов по одной категории и все расходы в разной валюте, 1 кейс."""
    main_page \
        .stat_item(category) \
        .should(have.text(str_total(total_to_rub(spends))))


@TestData.categories(TEST_CATEGORIES)
@TestData.spends(Spend.list_by(currencies=TEST_CURRENCIES, categories=TEST_CATEGORIES))
def test_spends_eur_to_rub_total(categories, spends, main_page):
    """Проверка статистики сумм расходов по разным категориям и расходам в разной валюте, 1 кейс."""
    for spend in spends:
        total = str_total(spend.amount_to_rub())
        main_page \
            .stat_item(spend.category.name) \
            .should(have.text(total))
