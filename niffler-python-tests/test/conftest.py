import pytest

from model.web_spend import Category


@pytest.fixture()
def new_category(spend_db, envs):
    """в setup проверяется, что такой категории нет в бд, в teardown - удаляется."""
    user_name = envs.test_username
    category = Category.random()
    result = spend_db.get_category_by_name(category.name, user_name)
    assert not result

    yield category

    result = spend_db.get_category_by_name(category.name, user_name)
    if result:
        spend_db.delete_category(result.id)

