from typing import Self

from allure import step
from selene import browser, Element, command, be, have

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

    @step("проверка, что имя пользователя соответствует ожидаемому {0}")
    def check_username_is(self, expected_name: str) -> Self:
        self.username.should(have.value(expected_name))
        return self

    @step("ввод новой категории : {0}")
    def input_category(self, name: str) -> Self:
        self.category.set_value(name).press_enter()
        return self

    @step("переключить свитчер 'Показать архивные'")
    def show_archived_click(self) -> Self:
        self.show_archived.click()
        return self

    def category_item_locator(self, name: str) -> str:
        return f"//span[contains(text(),'{name}')]"

    def category_item(self, name: str) -> Element:
        return browser.element(self.category_item_locator(name))

    @step("Проверка, что плашка категории есть(видима) на странице")
    def check_category_item_is_visible(self, name: str) -> Self:
        self.category_item(name).should(be.visible)
        return self

    @step("Проверка, что плашки категории нет(не видима) на странице")
    def check_category_item_is_not_visible(self, name: str) -> Self:
        self.category_item(name).should(be.not_.visible)
        return self

    @step("нажать кнопку 'Редактор категории' {0}")
    def edit_category_click(self, name: str) -> Self:
        browser.element(
            f"{self.category_item_locator(name)}../following-sibling::div//button[@aria-label='Edit category']") \
            .click()
        return self

    @step("нажать кнопку 'Архивировать категорию'")
    def archive_button_click(self, name: str) -> Self:
        browser.element(
            f"{self.category_item_locator(name)}/../following-sibling::div//button[@aria-label='Archive category']") \
            .click()
        return self

    @step("нажать кнопку 'Вернуть из архива'")
    def unarchive_button_click(self, name) -> Self:
        browser.element(
            f"{self.category_item_locator(name)}/../following-sibling::span[@aria-label='Unarchive category']") \
            .click()
        return self

    @step("Архивировать категорию")
    def archive_category(self, name: str) -> Self:
        self.archive_button_click(name)
        self.dialog.confirm_click()
        return self

    @step("Разархивировать категорию")
    def unarchive_category(self, name: str) -> Self:
        category = self.category_item(name)
        category.perform(command.js.scroll_into_view)  # execute_script(JScripts.SCROLL_TO_ELEMENT, category())
        self.unarchive_button_click(name)
        self.dialog.confirm_click()
        return self


class Toolbar:
    new_spending = browser.element("a[href='/spending']")
    menu_button = browser.element("button[aria-label=Menu]")

    profile = browser.element("a[href='/profile']")
    sign_out = browser.element("//li[contains(text(), 'Sign out')]")

    def __init__(self, page):
        self.page = page

    @step("нажать иконку на тулбаре")
    def menu_click(self) -> Self:
        self.menu_button.click()
        return self

    @step("пункт мею 'Профиль'")
    def profile_click(self) -> ProfilePage:
        self.profile.click()
        return self.page if isinstance(self.page, ProfilePage) else ProfilePage()

    @step("нажать кнопку 'Добавить расход (New spending)'")
    def new_spending_click(self) -> SpendingPage:
        self.new_spending.click()
        return SpendingPage()
