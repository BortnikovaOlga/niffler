from selene import browser


class JScripts:
    SCROLL_TO_ELEMENT = "arguments[0].scrollIntoView(true);"


def execute_script(script: str, *args):
    browser.driver.execute_script(script, *args)
