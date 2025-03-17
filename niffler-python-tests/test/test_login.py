from selene import have
from page.main_page import MainPage
from allure import Feature, Story, Tag

main_page = MainPage()


@Tag("UI")
@Feature("Профиль")
@Story("Управление категорями расходов")
class TestAuth:

    def test_auth(self, login_page, app_user):
        """Вход с тестовым паролем и логином, проверка - профиль соответствует username."""
        username, password = app_user
        login_page \
            .login(username, password)
        main_page.toolbar \
            .menu_click() \
            .profile_click() \
            .check_username_is(username)


    def test_auth_with_invalid_login(self, login_page):
        """Вход с невалидным пользователем и паролем, проверка - сообщение о неверных учетных данных."""
        login_page \
            .login("username", "password") \
            .login_prompt.should(have.text("Неверные учетные данные пользователя"))


    def test_open_register_page(self, login_page):
        """Проверка, что со страницы логина есть переход на страницу регистрации."""
        login_page \
            .register_button_click() \
            .title.should(have.text("Sign up"))
