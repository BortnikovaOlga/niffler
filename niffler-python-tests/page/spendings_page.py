from datetime import date
from typing import Self

from selene import browser, Element
from allure import step

from model.web_spend import Spend


class SpendingPage:
    amount = browser.element('#amount')
    description = browser.element('#description')
    save = browser.element('#save')
    cancel = browser.element("#cancel")
    currency = browser.element('#currency')
    spend_date = browser.element("input[name=date]")  # format MM DD YYYY

    def currency_item(self, name: str):
        return browser.element(f"li[data-value={name}]")  # RUB KZT EUR USD

    @staticmethod
    def category(name: str) -> Element:
        return browser.element(f"//div[@role='button']//span[contains(text(),'{name}')]")

    @step("нажать Сохранить")
    def save_click(self):
        self.save.click()

    @step("нажать Отмену")
    def cancel_click(self):
        self.cancel.click()

    @step("ввод суммы")
    def set_amount(self, value: float) -> Self:
        self.amount.set_value(value)
        return self

    @step("ввод описания")
    def set_description(self, value: str) -> Self:
        self.description.set_value(value)
        return self

    @step("ввод даты")
    def set_spend_date(self, value: date) -> Self:
        self.spend_date.double_click().send_keys(value.strftime('%m/%d/%Y'))
        return self

    @step("ввод категории")
    def set_category(self, value: str) -> Self:
        self.category(value).click()
        return self

    @step("нажать выбор валюты")
    def currency_click(self) -> Self:
        self.currency.click()
        return self

    @step("выбрать {0} из списка")
    def set_currency_item(self, value) -> Self:
        self.currency_item(value).click()
        return self

    @step("ввод валюты")
    def set_currency(self, value) -> Self:
        self.currency_click()
        self.set_currency_item(value)
        return self

    @step("заполнить расход")
    def input_spending(self, data: Spend) -> Self:
        self.set_amount(data.amount)
        self.set_description(data.description)
        self.set_category(data.category.name)
        if data.currency:
            self.set_currency(data.currency)
        if data.spendDate:
            self.set_spend_date(data.spendDate)
        return self
