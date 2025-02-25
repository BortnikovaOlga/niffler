from selene import browser, Element


class RegisterPage:
    title = browser.element('h1')
    form = browser.element("#register-form")
    username = browser.element('#username')
    password = browser.element('#password')
    password_submit = browser.element('#passwordSubmit')
    signup_button = browser.element('button[type=submit]')
    signin_button = browser.element('a.form_sign-in')

    def input_data(self, username, password):
        self.username.set_value(username)
        self.password.set_value(password)
        self.password_submit.set_value(password)
        return self

    def signup_click(self):
        self.signup_button.click()
        return self

    def signin_click(self):
        self.signin_button.click()
