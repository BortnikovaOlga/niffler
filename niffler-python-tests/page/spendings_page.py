from enum import StrEnum

from selene import browser, Element

from model.web_spend import Spend


class SpendingPage:
    amount = browser.element('#amount')
    description = browser.element('#description')
    save = browser.element('#save')
    cancel = browser.element("#cancel")
    currency = browser.element('#currency')
    spend_date = browser.element("input[name=date]")  # format MM DD YYYY

    def currency_item(self, name):
        return browser.element(f"li[data-value={name}]")  # RUB KZT EUR USD

    @staticmethod
    def category(name) -> Element:
        return browser.element(f"//div[@role='button']//span[contains(text(),'{name}')]")

    def input_spending(self, data: Spend):
        self.amount.set_value(data.amount)
        self.description.set_value(data.description)
        self.category(data.category.name).click()
        if data.currency:
            self.currency.click()
            self.currency_item(data.currency).click()
        if data.spendDate:
            self.spend_date.double_click().send_keys(data.spendDate.strftime('%m/%d/%Y'))
        return self

    def save_click(self):
        self.save.click()

    def cancel_click(self):
        self.cancel.click()
