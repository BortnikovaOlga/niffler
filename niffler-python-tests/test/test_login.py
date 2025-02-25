import pytest
from selene import have
from page.main_page import MainPage

main_page = MainPage()


def test_auth(login_page, app_user):
    """Вход с тестовым паролем и логином, проверка - профиль соответствует username."""
    username, password = app_user
    login_page \
        .login(username, password)
    main_page \
        .toolbar.menu_click().profile_click() \
        .username.should(have.value(username))


def test_auth_with_invalid_login(login_page):
    """Вход с невалидным пользователем и паролем, проверка - сообщение о неверных учетных данных."""
    login_page \
        .login("username", "password") \
        .login_prompt.should(have.text("Неверные учетные данные пользователя"))


def test_open_register_page(login_page):
    """Проверка, что со страницы логина есть переход на страницу регистрации."""
    login_page \
        .register_button_click() \
        .title.should(have.text("Sign up"))
