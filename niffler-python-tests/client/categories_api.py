from urllib.parse import urljoin

from pydantic import TypeAdapter

from model.web_spend import Category
from .http_client import HttpClient
from allure import step


class CategoriesApi:
    url: str

    def __init__(self, base_url: str, token: str):
        # self.url = urljoin(base_url, "/api/categories")
        self.url = f"{base_url}/api/categories"
        self.client = HttpClient(token)

    @step("http получить все категории")
    def get_categories(self) -> list[Category]:
        response = self.client.get(f"{self.url}/all")
        response.raise_for_status()
        cat_l: list[Category]
        return TypeAdapter(list[Category]).validate_python(response.json())

    @step("http добавить категорию")
    def add_category(self, category: Category) -> Category:
        response = self.client.post(f"{self.url}/add", json=category.model_dump())
        response.raise_for_status()
        return Category.model_validate(response.json())
