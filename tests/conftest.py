import ast

import pytest

from flake8_hangover import Plugin


@pytest.fixture
def run_plugin():
    """Fixture to parse ast from string and run plagin on it."""
    def wrapper(code_str):
        return {'{}:{}: {}'.format(*r) for r in Plugin(ast.parse(code_str)).run()}
    return wrapper
