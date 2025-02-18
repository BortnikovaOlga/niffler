from selene import browser, have
from page.pages import LoginPage, MainPage, Dialog, Toolbar, ToolbarMenu, ProfilePage, RegisterPage


def test_auth(frontend_url, app_user):
    """Вход с тестовым паролем и логином, проверка - профиль соответствует username."""
    username, password = app_user
    browser.open(frontend_url)

    browser.element(LoginPage.username).set_value(username)
    browser.element(LoginPage.password).set_value(password)
    browser.element(LoginPage.login_button).click()
    browser.element(Toolbar.menu_button).click()
    browser.element(ToolbarMenu.profile).click()

    browser.element(ProfilePage.username).should(have.value(username))


def test_auth_with_invalid_login(frontend_url):
    """Вход с невалидным пользователем и паролем, проверка - сообщение о неверных учетных данных."""
    browser.open(frontend_url)
    browser.element(LoginPage.username).set_value("username")
    browser.element(LoginPage.password).set_value("password")
    browser.element(LoginPage.login_button).click()
    browser.element(LoginPage.not_login_prompt).should(have.text("Неверные учетные данные пользователя"))


def test_open_register_page(frontend_url):
    """Проверка, что со страницы логина есть переход на страницу регистрации."""
    browser.open(frontend_url)
    browser.element(LoginPage.register_button).click()
    browser.element(RegisterPage.title).should(have.text("Sign up"))
