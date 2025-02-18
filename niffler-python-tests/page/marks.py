import pytest


class Pages:
    main_page = pytest.mark.usefixtures("main_page")
    login_page = pytest.mark.usefixtures()
    profile_page = pytest.mark.usefixtures("profile_page")


class TestData:
    category = lambda x: pytest.mark.parametrize("category", [x], indirect=True)
    spends = lambda x: pytest.mark.parametrize("spends", [x], indirect=True, ids=lambda param: param["description"])