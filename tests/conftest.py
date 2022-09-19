import ast
from io import StringIO
from tokenize import generate_tokens
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
        tree = ast.parse(code_str)
        tokens = list(generate_tokens(StringIO(code_str).readline))
        return {'{}:{}: {}'.format(*r) for r in Plugin(tree=tree, file_tokens=tokens).run()}
    return wrapper
