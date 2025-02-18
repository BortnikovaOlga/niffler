import os

import pytest
from dotenv import load_dotenv
from selene import browser
from client.spends_api import SpendsApi
from client.categories_api import CategoriesApi


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
def auth(frontend_url, app_user):
    username, password = app_user
    browser.open(frontend_url)

    browser.element('input[name=username]').set_value(username)
    browser.element('input[name=password]').set_value(password)
    browser.element('button[type=submit]').click()

    return browser.driver.execute_script('return window.localStorage.getItem("id_token")')


# class Pages:
#     main_page = pytest.mark.usefixtures("main_page")
#
#
# class TestData:
#     category = lambda x: pytest.mark.parametrize("category", [x], indirect=True)
#     spends = lambda x: pytest.mark.parametrize("spends", [x], indirect=True, ids=lambda param: param["description"])


@pytest.fixture(scope="session")
def spends_api(gateway_url, auth) -> SpendsApi:
    return SpendsApi(gateway_url, auth)


@pytest.fixture(scope="session")
def categories_api(gateway_url, auth) -> CategoriesApi:
    return CategoriesApi(gateway_url, auth)


@pytest.fixture(params=[])
def category(request, categories_api):
    category_name = request.param
    current_categories = categories_api.get_categories()
    category_names = [category["name"] for category in current_categories]
    if category_name not in category_names:
        categories_api.add_category(category_name)
    return category_name


@pytest.fixture(params=[])
def spends(request, spends_api):
    spend = spends_api.add_spends(request.param)
    yield spend
    try:
        # TODO вместо исключения проверить список текущих spends
        spends_api.remove_spends([spend["id"]])
    except Exception:
        pass


@pytest.fixture()
def main_page(auth, frontend_url):
    browser.open(frontend_url)


@pytest.fixture()
def profile_page(auth, frontend_url):
    browser.open(f"{frontend_url}/profile")
