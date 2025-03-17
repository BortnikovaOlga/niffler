from allure import step


def assert_with_allure(condition, message=""):
    """example : assert_with_allure(username == 'admin', 'Проверка логина')."""
    with step(message):
        assert condition, message
