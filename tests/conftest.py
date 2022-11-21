import ast
from io import StringIO
from tokenize import generate_tokens
from typing import Optional

import pytest

from flake8_hangover import Plugin

CLASSES_REGISTRY = {}


@pytest.fixture
def run_plugin():
    """Fixture to parse ast from string and run plugin on it."""
    def wrapper(code_str, strip_tabs: Optional[int] = None):
        if strip_tabs:
            tabs = strip_tabs * 4
            code_str = '\n'.join([line[tabs:] for line in code_str.strip('\n').split('\n')])
        tree = ast.parse(code_str)
        tokens = list(generate_tokens(StringIO(code_str).readline))
        return {'{}:{}: {}'.format(*r) for r in Plugin(tree=tree, file_tokens=tokens).run()}
    return wrapper


def register_case(_class):
    """Decorator to register case class."""
    name = _class.__name__
    module = _class.__module__
    if module not in CLASSES_REGISTRY:
        CLASSES_REGISTRY[module] = {}
    if name in CLASSES_REGISTRY[module]:
        raise ValueError(f'Case "{name}" already exists')
    CLASSES_REGISTRY[module][name] = _class
    return _class


def check_registered_case(
    run_plugin,
    case,
    case_name: str = None,
    case_code: str = None,
):
    """Test plugin on function calls."""
    name = case_name or case.__name__
    code = case_code or case.code
    expected_errors = sorted(case.errors or [])
    found_errors = sorted(list(run_plugin(code, strip_tabs=1)), key=lambda s: s.split(': ', 1)[1])

    def show_error(found, expected):
        if isinstance(found, list):
            found = '\n'.join(found)
        if isinstance(expected, list):
            expected = '\n'.join(expected)
        return (
            f'Case "{name}" failed.\n'
            f'Code:\n{code}\n'
            f'Errors:\n{found}\n\n'
            f'Expected:\n{expected}\n'
        )

    if expected_errors:
        assert len(found_errors) == len(expected_errors), show_error(found_errors, expected_errors)
        for i, msg in enumerate(expected_errors):
            assert found_errors[i].endswith(msg), show_error(found_errors, expected_errors)
    else:
        assert not found_errors, show_error(found_errors, 'No errors')
