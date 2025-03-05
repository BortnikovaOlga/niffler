import pytest

from model.spendings import Spend


class Pages:
    main_page = pytest.mark.usefixtures("main_page")
    profile_page = pytest.mark.usefixtures("profile_page")
    login_page = pytest.mark.usefixtures()


class TestData:
    category = lambda x: pytest.mark.parametrize("category", [x], indirect=True)
    categories = lambda x: pytest.mark.parametrize("categories", [x], indirect=True)
    spends = lambda x: pytest.mark.parametrize("spends", [x], indirect=True)  # , ids=lambda param: param.description)


class TestListData:
    """в параметры создается список из списков по сочетаниям (категория, валюта)."""
    spends_by = \
        lambda currencies, categories: \
            pytest.mark.parametrize("spends",
                                    [
                                        Spend.random_list(category=category, currency=currency) \
                                        for currency, category in zip(currencies, categories)
                                    ],
                                    indirect=True)

    # spends = lambda x: pytest.mark.parametrize("spends", x, indirect=True)
