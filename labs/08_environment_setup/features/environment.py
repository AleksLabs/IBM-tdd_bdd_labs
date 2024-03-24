"""
Environment for Behave Testing
"""
from os import getenv
from selenium import webdriver

BASE_URL = getenv("BASE_URL", "http://localhost:8080")
WAIT_SECONDS = int(getenv("WAIT_SECONDS", "60"))

def before_all(context):
    """ Executed once before all tests """
    context.base_url = BASE_URL
    context.wait_seconds = WAIT_SECONDS
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    context.driver = webdriver.Chrome(options=options)
    context.driver.implicitly_wait(context.wait_seconds)


def after_all(context):
    """ Executed after all tests """
    context.driver.quit()
