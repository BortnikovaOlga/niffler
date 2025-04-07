from model.web_spend import Spend, Currency, Category
from page.main_page import Period
from page.marks import TestData
from allure import feature, story, tag

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


@tag("UI")
@feature("Ведение расходов")
@story("Фильтрация расходов по периоду")
class TestPeriodFilter:

    @TestData.category(TEST_CATEGORY)
    @TestData.spends([spend_yesterday, spend_today])
    def test_spends_filtered_by_today(self, category, spends, main_page):
        """Проверка, что расходы фильтруются за текущий день + проверка статистики."""
        main_page \
            .period_click() \
            .choose_period_by(Period.TODAY)
        main_page \
            .check_table_have_text(spend_today.description) \
            .check_stat_item_have_total(category.name, spend_today.amount)

    @TestData.category(TEST_CATEGORY)
    @TestData.spends([old_spend, spend_past_week])
    def test_spends_filtered_by_last_week(self, category, spends, main_page):
        """Проверка, что расходы фильтруются за текущую неделю + проверка статистики."""
        main_page \
            .period_click() \
            .choose_period_by(Period.LAST_WEEK)
        main_page \
            .check_table_have_text(spend_past_week.description) \
            .check_stat_item_have_total(category.name, spend_past_week.amount)

    @TestData.category(TEST_CATEGORY)
    @TestData.spends([old_spend, spend_past_month])
    def test_spends_filtered_by_last_month(self, category, spends, main_page):
        """Проверка, что расходы фильтруются за последний месяц + проверка статистики."""
        main_page \
            .period_click() \
            .choose_period_by(Period.LAST_MONTH)
        main_page \
            .check_table_have_text(spend_past_month.description) \
            .check_stat_item_have_total(category.name, spend_past_month.amount)
