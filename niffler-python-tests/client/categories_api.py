from pydantic import TypeAdapter
from model.web_spend import Category
from .http_client import HttpClient
from allure import step


class CategoriesApi:

    def __init__(self, base_url: str, token: str):
        self.client = HttpClient(base_url=f"{base_url}/api/categories", token=token)

    @step("http получить все категории")
    def get_categories(self) -> list[Category]:
        response = self.client.get("/all")
        response.raise_for_status()
        return TypeAdapter(list[Category]).validate_python(response.json())

    @step("http добавить категорию")
    def add_category(self, category: Category) -> Category:
        response = self.client.post("/add", json=category.model_dump())
        response.raise_for_status()
        return Category.model_validate(response.json())

    def update_category(self, update: Category) -> Category:
        response = self.client.patch("/update", json=update.model_dump())
        response.raise_for_status()
        return Category.model_validate(response.json())
