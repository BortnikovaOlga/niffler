from enum import StrEnum
from typing import Self

from selene import browser, Element, have
from allure import step

from model.web_spend import str_total
from page.pages import Dialog
from page.profile import Toolbar
from page.spendings_page import SpendingPage


class Period(StrEnum):
    LAST_MONTH = "MONTH"
    LAST_WEEK = "WEEK"
    TODAY = "TODAY"


class MainPage:
    delete_button = browser.element('#delete')
    spendings = browser.element('#spendings')
    spendings_title = browser.element('#spendings h2')

    spending_table = browser.element('#spendings tbody')
    table_first = spending_table.element("tr")
    first_checkbox = spending_table.element('input[type=checkbox]')
    edit_first = browser.element("button[aria-label='Edit spending']")
    table_checkbox = browser.element("input[aria-label='select all rows']")
    table_rows = spending_table.all("tr")

    period = browser.element("#period")

    dialog = Dialog()

    def __init__(self):
        self.toolbar = Toolbar(self)

    @step("выбрать все расходы")
    def table_checkbox_click(self) -> Self:
        self.table_checkbox.click()
        return self

    @step("нажать кнопку Удалить")
    def delete_click(self) -> Self:
        self.delete_button.click()
        return self

    @step("Удалить все расходы")
    def delete_spendings(self) -> Self:
        self.table_checkbox_click()
        self.delete_click()
        self.dialog.confirm_click()
        return self

    @step("редактировать расход в первой строке")
    def edit_first_click(self) -> SpendingPage:
        self.edit_first.click()
        return SpendingPage()

    @step("нажать фильтр 'Период'")
    def period_click(self) -> Self:
        self.period.click()
        return self

    @step("выбрать период за {0}")
    def choose_period_by(self, period: Period) -> Self:
        period_by = browser.element(f"li[data-value={period.value}]")
        period_by.click()
        return self

    @staticmethod
    def stat_item(category: str) -> Element:
        """статистика по категории."""
        return browser.element(f"//div[@id='stat']//li[contains(text(),'{category}')]")

    @step("проверка, что плашка статистики по категории {0} отображает сумму {1}")
    def check_stat_item_have_total(self, category_name: str, total: float) -> Self:
        total = str_total(total)
        self.stat_item(category_name).should(have.text(total))
        return self

    @step("проверка присутствия строки '{0}' в таблице")
    def check_table_have_text(self, text) -> Self:
        self.table_first.should(have.text(text))
        return self

    @step("проверка, что нет расходов")
    def check_no_spends(self) -> Self:
        self.spendings.should(have.text("There are no spendings"))
        return self
