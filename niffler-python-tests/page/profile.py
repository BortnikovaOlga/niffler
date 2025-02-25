from selene import browser, Element

from page.pages import Dialog
from page.spendings_page import SpendingPage


class ProfilePage:
    username = browser.element('#username')
    category = browser.element('#category')
    save_changes = browser.element("//button[contains(., 'Save changes')]")
    show_archived = browser.element("//span[contains(text(),'Show archived')]")

    dialog = Dialog()

    def __init__(self):
        self.toolbar = Toolbar(self)

    def input_category(self, name):
        self.category.set_value(name).press_enter()
        return self

    def show_archived_click(self):
        self.show_archived.click()
        return self

    def category_item_str(self, name) -> str:
        return f"//span[contains(text(),'{name}')]"

    def category_item(self, name) -> Element:
        return browser.element(self.category_item_str(name))

    def edit_category_click(self, name):
        browser.element(
            f"{self.category_item_str(name)}../following-sibling::div//button[@aria-label='Edit category']").click()
        return self

    def archive_button_click(self, name):
        browser.element(
            f"{self.category_item_str(name)}/../following-sibling::div//button[@aria-label='Archive category']").click()
        return self

    def archive_category(self, name):
        self.archive_button_click(name)
        self.dialog.confirm_click()
        return self

class Toolbar:
    new_spending = browser.element("a[href='/spending']")
    menu_button = browser.element("button[aria-label=Menu]")

    profile = browser.element("a[href='/profile']")
    sign_out = browser.element("//li[contains(text(), 'Sign out')]")

    def __init__(self, page):
        self.page = page

    def menu_click(self):
        self.menu_button.click()
        return self

    def profile_click(self) -> ProfilePage:
        self.profile.click()
        return self.page if isinstance(self.page, ProfilePage) else ProfilePage()

    def new_spending_click(self):
        self.new_spending.click()
        return SpendingPage()