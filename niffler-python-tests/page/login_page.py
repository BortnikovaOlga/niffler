from selene import browser, Element

from page.register_page import RegisterPage


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


# //div[@role='dialog']//button[contains(text(),'Archive')]
