from page.main_page import MainPage
from faker import Faker
from allure import feature, story, tag

from page.profile import ProfilePage

fake = Faker()
main_page = MainPage()
# profile_page/ = ProfilePage()

@tag("UI")
@feature("Учетная запись пользователя")
@story("Регистрация")
class TestRegister:

    def test_register_new_user(self, login_page):
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
            .toolbar \
            .menu_click() \
            .profile_click() \
            .check_username_is(username)


    def test_not_register_if_user_exist(self, login_page, envs):
        """Проверка, что не выполняется повторная регистрация существующего пользователя."""
        username = envs.test_username
        login_page \
            .register_button_click() \
            .input_data(username, fake.password()) \
            .signup_click() \
            .check_form_error(f"Username `{username}` already exists")


    def test_not_register_if_password_not_eql_password_submit(self, login_page):
        """Проверка, что при регистрации возникает ошибка, если введены разные пароль и подтверждение пароля."""
        username = fake.user_name()
        password = fake.password()
        login_page \
            .register_button_click() \
            .input_data(username, password, password + "*") \
            .signup_click() \
            .check_form_error(f"Passwords should be equal")
