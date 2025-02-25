from enum import StrEnum

from selene import browser, Element

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

    def table_checkbox_click(self):
        self.table_checkbox.click()
        return self

    def delete_click(self):
        self.delete_button.click()
        return self

    def delete_spendings(self):
        self.table_checkbox_click()
        self.delete_click()
        self.dialog.confirm_click()
        return self

    def edit_first_click(self) -> SpendingPage:
        self.edit_first.click()
        return SpendingPage()

    def period_click(self):
        self.period.click()
        return self

    def choose_period_by(self, period: Period):
        period_by = browser.element(f"li[data-value={period.value}]")
        period_by.click()
        return self

    @staticmethod
    def stat_item(category):
        return browser.element(f"//div[@id='stat']//li[contains(text(),'{category}')]")