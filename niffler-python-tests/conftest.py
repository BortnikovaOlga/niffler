import os

import pytest
from dotenv import load_dotenv
from selene import browser
from client.spends_api import SpendsApi
from client.categories_api import CategoriesApi
from db.spend_service import SpendDbService
from model.web_spend import Category
from page.login_page import LoginPage
from page.main_page import MainPage
from page.profile import ProfilePage


@pytest.fixture(scope="session")
def envs():
    load_dotenv()


@pytest.fixture(scope="session")
def frontend_url(envs):
    return os.getenv("FRONTEND_URL")


@pytest.fixture(scope="session")
def gateway_url(envs):
    return os.getenv("GATEWAY_URL")


@pytest.fixture(scope="session")
def app_user(envs):
    return os.getenv("TEST_USERNAME"), os.getenv("TEST_PASSWORD")


@pytest.fixture(scope="session")
def spend_db_url(envs):
    return os.getenv("SPEND_DB_URL")


@pytest.fixture(scope="session")
def spend_db(spend_db_url) -> SpendDbService:
    return SpendDbService(spend_db_url)


@pytest.fixture(scope="session")
def auth(frontend_url, app_user):
    username, password = app_user
    browser.open(frontend_url)

    browser.element('input[name=username]').set_value(username)
    browser.element('input[name=password]').set_value(password)
    browser.element('button[type=submit]').click()

    return browser.driver.execute_script('return window.localStorage.getItem("id_token")')


@pytest.fixture(scope="session")
def spends_api(gateway_url, auth) -> SpendsApi:
    return SpendsApi(gateway_url, auth)


@pytest.fixture(scope="session")
def categories_api(gateway_url, auth) -> CategoriesApi:
    return CategoriesApi(gateway_url, auth)


@pytest.fixture(params=[])
def category(request, categories_api) -> Category:
    """request.param : Category."""
    test_category = request.param
    db_categories = categories_api.get_categories()
    category_names = [category.name for category in db_categories]
    if test_category.name not in category_names:
        return categories_api.add_category(test_category)
    return test_category


@pytest.fixture(params=[])
def categories(request, categories_api) -> list[str]:
    """request.param: list[str]."""
    db_categories = categories_api.get_categories()
    category_names = [category.name for category in db_categories]
    categories = []
    for category_name in request.param:
        if category_name not in category_names:
            categories_api.add_category(Category(name=category_name))
            categories.append(category_name)
    return categories


@pytest.fixture(params=[])
def spends(request, spends_api):
    spends = []
    for spend in request.param:
        spends.append(spends_api.add_spends(spend))
    yield spends
    try:
        # TODO вместо исключения проверить список текущих spends
        spends_api.remove_spends([s.id for s in spends])
        pass
    except Exception:
        pass


@pytest.fixture()
def main_page(auth, frontend_url):
    browser.driver.maximize_window()
    browser.open(frontend_url)
    return MainPage()


@pytest.fixture()
def profile_page(auth, frontend_url):
    browser.driver.maximize_window()
    browser.open(f"{frontend_url}/profile")
    return ProfilePage()


@pytest.fixture
def login_page(frontend_url):
    browser.open(frontend_url)
    return LoginPage()
