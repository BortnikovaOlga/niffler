from typing import Self

from selene import browser
from allure import step

from page.register_page import RegisterPage


class LoginPage:
    username = browser.element('input[name=username]')
    password = browser.element('input[name=password]')
    login_button = browser.element('button[type=submit]')
    register_button = browser.element("a[href='/register']")
    login_prompt = browser.element("form[action='/login'] p")

    @step("Выполнить вход")
    def login(self, username, password):
        self.set_username(username)
        self.set_password(password)
        self.login_click()
        return self

    @step("нажать регистрацию")
    def register_button_click(self) -> RegisterPage:
        self.register_button.click()
        return RegisterPage()

    @step("ввести имя пользователя {0}")
    def set_username(self, value: str) -> Self:
        self.username.set_value(value)
        return self

    @step("ввести пароль")
    def set_password(self, value: str) -> Self:
        self.password.set_value(value)
        return self

    @step("нажать кнопку Входа")
    def login_click(self) -> Self:
        self.login_button.click()
        return self
