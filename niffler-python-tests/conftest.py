import os

import dotenv
import pytest

from selene import browser
from allure import step, attach, attachment_type
from allure_commons.reporter import AllureReporter
from allure_pytest.listener import AllureListener
from selenium.webdriver.chrome.options import Options

from client.oauth_client import OAuthClient
from client.spends_api import SpendsApi
from client.categories_api import CategoriesApi
from db.spend_service import SpendDbService
from model.envs import Envs
from model.web_spend import Category
from page.login_page import LoginPage
from page.main_page import MainPage
from page.profile import ProfilePage


@pytest.fixture(scope="session")
def envs() -> Envs:
    dotenv.load_dotenv()
    envs_instance = Envs(
        frontend_url=os.getenv("FRONTEND_URL"),
        gateway_url=os.getenv("GATEWAY_URL"),
        db_engine=os.getenv("SPEND_DB_URL"),
        test_username=os.getenv("TEST_USERNAME"),
        test_password=os.getenv("TEST_PASSWORD"),
        auth_url=os.getenv("AUTH_URL"),
        auth_secret=os.getenv("AUTH_SECRET"),
    )
    return envs_instance


@pytest.fixture(scope="session")
def spend_db(envs) -> SpendDbService:
    return SpendDbService(envs.db_engine)


# @pytest.fixture(scope="session")
# def auth(envs):
#     browser.open(envs.frontend_url)
#
#     browser.element('input[name=username]').set_value(envs.test_username)
#     browser.element('input[name=password]').set_value(envs.test_password)
#     browser.element('button[type=submit]').click()
#
#     return browser.driver.execute_script('return window.localStorage.getItem("id_token")')


@pytest.fixture(scope="session")
def auth_token(envs: Envs):
    return OAuthClient(envs).get_token(envs.test_username, envs.test_password)


@pytest.fixture(scope="session")
def auth_browser_config(auth_token):
    options = Options()
    # options.add_argument("--headless")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-site-isolation-trials")  # Отключает изоляцию сайтов
    options.add_argument("--allow-file-access-from-files")  # Разрешает доступ к файлам
    # options.add_argument("--disable-redirects")
    options.add_argument("--remote-debugging-port=9222")  # Включаем DevTools

    browser.config.driver_options = options
    browser.config.timeout = 10
    browser.driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {"source": f"localStorage.setItem('id_token', '{auth_token}');"}
    )
    browser.driver.refresh()


@pytest.fixture(scope="session")
def spends_api(envs, auth_token) -> SpendsApi:
    return SpendsApi(envs.gateway_url, auth_token)


@pytest.fixture(scope="session")
def categories_api(envs, auth_token) -> CategoriesApi:
    return CategoriesApi(envs.gateway_url, auth_token)


@pytest.fixture(params=[])
def category(request, categories_api, spend_db, envs) -> Category:
    """request.param : Category."""
    test_category = request.param
    with step("проверить наличие и добавить категорию"):
        db_categories = categories_api.get_categories()
        category_names = [category.name for category in db_categories]
        if test_category.name not in category_names:
            test_category = categories_api.add_category(test_category)
    yield test_category
    with step("удалить категорию"):
        result = spend_db.get_category_by_name(test_category.name, envs.test_username)
        if result:
            spend_db.delete_category(result.id)


@pytest.fixture(params=[])
def categories(request, categories_api, spend_db, envs) -> list[str]:
    """request.param: list[str]."""
    db_categories = categories_api.get_categories()
    category_names = [category.name for category in db_categories]
    categories = []
    for category_name in request.param:
        if category_name not in category_names:
            categories_api.add_category(Category(name=category_name))
            categories.append(category_name)
    yield categories
    with step("удалить категории"):
        for category in categories:
            result = spend_db.get_category_by_name(category, envs.test_username)
            if result:
                spend_db.delete_category(result.id)


@pytest.fixture(params=[])
def spends(request, spends_api):
    spends = []
    with step("добавить список расходов"):
        for spend in request.param:
            spends.append(spends_api.add_spend(spend))
    yield spends
    with step("удалить расходы"):
        try:
            # TODO вместо исключения проверить список текущих spends
            spends_api.remove_spends([s.id for s in spends])
        except Exception:
            pass


@pytest.fixture()
def main_page(auth_browser_config, envs):
    browser.driver.maximize_window()
    browser.open(envs.frontend_url)
    return MainPage()


@pytest.fixture()
def profile_page(auth_browser_config, envs):
    browser.open(f"{envs.frontend_url}/profile")
    return ProfilePage()


@pytest.fixture
def login_page(envs):
    browser.open(envs.frontend_url)
    return LoginPage()


def allure_reporter(config) -> AllureReporter:
    listener: AllureListener = next(
        filter(
            lambda plugin: (isinstance(plugin, AllureListener)),
            dict(config.pluginmanager.list_name_plugin()).values(),
        ),
        None,
    )
    return getattr(listener, "allure_logger", None)


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_teardown(item):
    yield
    reporter = allure_reporter(item.config)
    if reporter:
        test = reporter.get_test(None)
        test.labels = list(
            filter(lambda x: not (x.name == "tag" and "@pytest.mark.usefixtures" in x.value),
                   test.labels)
        )


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        try:
            attach(browser.driver.get_screenshot_as_png(), name="screenshot", attachment_type=attachment_type.PNG)
        except Exception as e:
            pass  # logger.error("Fail to take screen-shot: {}".format(e))
