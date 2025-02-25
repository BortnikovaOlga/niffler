from selene import browser, Element


class Dialog:
    confirm = browser.element("(//div[@role='dialog']//button)[2]")

    def confirm_click(self):
        self.confirm.click()
