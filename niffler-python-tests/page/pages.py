from selene import browser, be, command
from allure import step


class Dialog:
    confirm = browser.element("(//div[@role='dialog']//button)[2]")

    @step("подтвердить действие")
    def confirm_click(self):
        self.confirm.wait_until(be.clickable)
        self.confirm.perform(command.js.click)
        self.confirm.wait_until(be.not_.visible)
