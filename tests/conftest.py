import ast
from typing import Optional

import pytest

from flake8_hangover import Plugin


@pytest.fixture
def run_plugin():
    """Fixture to parse ast from string and run plagin on it."""
    def wrapper(code_str, strip_tabs: Optional[int] = None):
        if strip_tabs:
            tabs = strip_tabs * 4
            code_str = '\n'.join([line[tabs:] for line in code_str.strip('\n').split('\n')])
        return {'{}:{}: {}'.format(*r) for r in Plugin(ast.parse(code_str)).run()}
    return wrapper
