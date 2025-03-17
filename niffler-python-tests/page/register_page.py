from typing import Self

from selene import browser, have
from allure import step


class RegisterPage:
    title = browser.element('h1')
    form_error = browser.element(".form__error")
    username = browser.element('#username')
    password = browser.element('#password')
    password_submit = browser.element('#passwordSubmit')
    signup_button = browser.element('button[type=submit]')
    signin_button = browser.element('a.form_sign-in')

    @step("ввести данные для регистрации")
    def input_data(self, username, password, password_submit=None) -> Self:
        self.set_username(username)
        self.set_password(password)
        self.set_password_submit(password_submit if password_submit else password)
        return self

    @step("нажать кнопку регистрации")
    def signup_click(self) -> Self:
        self.signup_button.click()
        return self

    @step("нажать кнопку входа")
    def signin_click(self):
        self.signin_button.click()

    @step("ввести имя пользователя")
    def set_username(self, value: str) -> Self:
        self.username.set_value(value)
        return self

    @step("ввести пароль")
    def set_password(self, value: str) -> Self:
        self.password.set_value(value)
        return self

    @step("ввести подтверждение пароля")
    def set_password_submit(self, value: str) -> Self:
        self.password_submit.set_value(value)
        return self

    @step("проверка, что на странице есть ошибка '{0}'")
    def check_form_error(self, text: str) -> Self:
        self.form_error.should(have.text(text))
        return self
