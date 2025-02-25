import pytest
from selene import have

from page.main_page import MainPage
from faker import Faker

fake = Faker()
main_page = MainPage()


def test_register_new_user(login_page):
    """Проверка, что выполняется регистрация нового пользователя."""
    username = fake.user_name()
    password = fake.password()
    login_page \
        .register_button_click() \
        .input_data(username, password) \
        .signup_click() \
        .signin_click()
    login_page \
        .login(username, password)
    main_page \
        .toolbar.menu_click().profile_click() \
        .username.should(have.value(username))


def test_not_register_exist_user(login_page, app_user):
    """Проверка, что не выполняется повторная регистрация существующего пользователя."""
    username, _ = app_user
    login_page \
        .register_button_click() \
        .input_data(username, "password") \
        .signup_click() \
        .form.should(have.text(f"Username `{username}` already exists"))

