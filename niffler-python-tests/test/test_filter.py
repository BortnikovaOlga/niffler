from selene import have

from model.web_spend import Spend, Currency, str_total, Category
from page.main_page import Period
from page.marks import TestData

TEST_CATEGORY_NAME = "образование"
TEST_CATEGORY = Category(name=TEST_CATEGORY_NAME)

spend_today = Spend.random(category=TEST_CATEGORY_NAME,
                           currency=Currency.RUB
                           )
spend_yesterday = Spend.random(category=TEST_CATEGORY_NAME,
                               currency=Currency.RUB,
                               days_delta=1
                               )
spend_past_week = Spend.random(category=TEST_CATEGORY_NAME,
                               currency=Currency.RUB,
                               days_delta=6
                               )
spend_past_month = Spend.random(category=TEST_CATEGORY_NAME,
                                currency=Currency.RUB,
                                days_delta=25
                                )
old_spend = Spend.random(category=TEST_CATEGORY_NAME,
                         currency=Currency.RUB,
                         days_delta=60,
                         min_days_delta=32
                         )


@TestData.category(TEST_CATEGORY)
@TestData.spends([spend_yesterday, spend_today])
def test_spends_filtered_by_today(category, spends, main_page):
    """Проверка, что расходы фильтруются за текущий день + проверка статистики."""
    total = str_total(spend_today.amount)
    main_page \
        .period_click() \
        .choose_period_by(Period.TODAY)
    main_page \
        .table_first.should(have.text(total).and_(have.text(spend_today.description)))
    main_page \
        .stat_item(category.name).should(have.text(total))


@TestData.category(TEST_CATEGORY)
@TestData.spends([old_spend, spend_past_week])
def test_spends_filtered_by_last_week(category, spends, main_page):
    """Проверка, что расходы фильтруются за текущую неделю + проверка статистики."""
    total = str_total(spend_past_week.amount)
    main_page \
        .period_click() \
        .choose_period_by(Period.LAST_WEEK)
    main_page \
        .table_first.should(have.text(total).and_(have.text(spend_past_week.description)))
    main_page \
        .stat_item(category.name).should(have.text(total))


@TestData.category(TEST_CATEGORY)
@TestData.spends([old_spend, spend_past_month])
def test_spends_filtered_by_last_month(category, spends, main_page):
    """Проверка, что расходы фильтруются за последний месяц + проверка статистики."""
    total = str_total(spend_past_month.amount)
    main_page \
        .period_click() \
        .choose_period_by(Period.LAST_MONTH)
    main_page \
        .table_first.should(have.text(total).and_(have.text(spend_past_month.description)))
    main_page \
        .stat_item(category.name).should(have.text(total))
