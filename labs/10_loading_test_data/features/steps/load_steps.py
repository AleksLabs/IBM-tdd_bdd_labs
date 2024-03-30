# pylint: disable=function-redefined, missing-function-docstring
# flake8: noqa
"""
Pet Steps
Steps file for Pet.feature
For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""
import requests
from behave import given

# Load data here

@given("the following pets")
def step_impl(context):
    """Refreshing initial table"""
    # List all of the pets and delete them one by one
    response = requests.get(f"{context.base_url}/pets")
    assert response.status_code == 200
    for pet in response.json():
        del_response = requests.delete(f"{context.base_url}/pets/{pet['id']}")
        assert del_response.status_code == 204