from selene import browser, Element


class Dialog:
    confirm = browser.element("(//div[@role='dialog']//button)[2]")

    def confirm_click(self):
        self.confirm.click()


class ProfilePage:
    username = browser.element('#username')
    category = browser.element('#category')
    dialog = Dialog()

    def __init__(self):
        self.toolbar = Toolbar(self)

    def input_category(self, name):
        self.category.set_value(name).press_enter()
        return self

    def category_item_str(self, name) -> str:
        return f"//span[contains(text(),'{name}')]"

    def category_item(self, name) -> Element:
        return browser.element(self.category_item_str(name))

    def edit_category_click(self, name):
        browser.element(
            f"{self.category_item_str(name)}../following-sibling::div//button[@aria-label='Edit category']").click()
        return self

    def archive_button_click(self, name):
        browser.element(
            f"{self.category_item_str(name)}/../following-sibling::div//button[@aria-label='Archive category']").click()
        return self

    def archive_category(self, name):
        self.archive_button_click(name)
        self.dialog.confirm_click()
        return self



class Toolbar:
    new_spending = browser.element("a[href='/spending']")
    menu_button = browser.element("button[aria-label=Menu]")

    profile = browser.element("a[href='/profile']")
    sign_out = browser.element("//li[contains(text(), 'Sign out')]")

    def __init__(self, page):
        self.page = page

    def menu_click(self):
        self.menu_button.click()
        return self

    def profile_click(self) -> ProfilePage:
        self.profile.click()
        return self.page if isinstance(self.page, ProfilePage) else ProfilePage()

    def new_spending_click(self):
        self.new_spending.click()
        return SpendingPage()


class MainPage:
    delete_button = browser.element('#delete')
    spendings = browser.element('#spendings')
    spendings_title = browser.element('#spendings h2')

    spending_table = browser.element('#spendings tbody')
    table_first = spending_table.element("tr")
    first_checkbox = spending_table.element('input[type=checkbox]')
    table_checkbox = browser.element("input[aria-label='select all rows']")
    dialog = Dialog()

    def __init__(self):
        self.toolbar = Toolbar(self)
        self.table_rows = self.spending_table.all("tr")

    def table_checkbox_click(self):
        self.table_checkbox.click()
        return self

    def delete_click(self):
        self.delete_button.click()
        return self

    def delete_spendings(self):
        self.table_checkbox_click()
        self.delete_click()
        self.dialog.confirm_click()
        return self


class SpendingPage:
    amount = browser.element('#amount')
    description = browser.element('#description')
    save = browser.element('#save')
    cancel = browser.element("#cancel")

    @staticmethod
    def category(name) -> Element:
        return browser.element(f"//div[@role='button']//span[contains(text(),'{name}')]")

    def input_spending(self, data):
        self.amount.set_value(data["amount"])
        self.description.set_value(data["description"])
        self.category(data["category"]["name"]).click()
        # todo currency
        return self


class LoginPage:
    username = browser.element('input[name=username]')
    password = browser.element('input[name=password]')
    login_button = browser.element('button[type=submit]')
    register_button = browser.element("a[href='/register']")
    login_prompt = browser.element("form[action='/login'] p")

    def login(self, username, password):
        self.username.set_value(username)
        self.password.set_value(password)
        self.login_button.click()
        return self

    def register_button_click(self):
        self.register_button.click()
        return RegisterPage()


class RegisterPage:
    title = browser.element('h1')

# //div[@role='dialog']//button[contains(text(),'Archive')]
