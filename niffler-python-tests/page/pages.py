class MainPage:
    delete_button = '#delete'
    spendings = '#spendings'
    spendings_title = '#spendings h2'


class SpendingTable:
    first_row = '#spendings tr'
    rows = "#spendings tbody tr"
    title_checkbox = '#spendings tbody input[type=checkbox]'


class SpendingPage:
    amount = '#amount'
    description = '#description'
    save = '#save'
    cancel = "#cancel"

    @staticmethod
    def category(name: str):
        return f"//div[@role='button']//span[contains(text(),'{name}')]"


class Dialog:
    confirm = "(//div[@role='dialog']//button)[2]"


class LoginPage:
    username = 'input[name=username]'
    password = 'input[name=password]'
    login_button = 'button[type=submit]'
    register_button = "a[href='/register']"
    not_login_prompt = "form[action='/login'] p"


class Toolbar:
    new_spending = "a[href='/spending']"
    menu_button = "button[aria-label=Menu]"


class ToolbarMenu:
    profile = "a[href='/profile']"
    sign_out = "//li[contains(text(), 'Sign out')]"


class ProfilePage:
    username = '#username'
    category = '#category'

    @staticmethod
    def category_item(name):
        return f"//span[contains(text(),'{name}')]"

    @staticmethod
    def edit_category_button(name):
        return f"{ProfilePage.category_item(name)}/../following-sibling::div//button[@aria-label='Edit category']"

    @staticmethod
    def archive_button(name):
        return f"{ProfilePage.category_item(name)}/../following-sibling::div//button[@aria-label='Archive category']"


class RegisterPage:
    title = 'h1'

# //div[@role='dialog']//button[contains(text(),'Archive')]