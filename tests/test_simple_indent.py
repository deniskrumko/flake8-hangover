import pytest

from flake8_hangover.plugin import Messages

CLASSES_REGISTRY = {}


def register_case(_class):
    """Decorator to register case class."""
    name = _class.__name__
    if name in CLASSES_REGISTRY:
        raise ValueError(f'Case "{name}" already exists')
    CLASSES_REGISTRY[name] = _class
    return _class


@register_case
class Case1:
    errors = [Messages.FHG007]
    code = """
    predicted: list = ([predicted_columns] if isinstance(predicted_columns, str)
                    else predicted_columns)
    """


@register_case
class Case2:
    errors = [Messages.FHG007]
    code = """
    predicted = ([predicted_columns] if isinstance(predicted_columns, str)
                    else predicted_columns
        )
    """


@register_case
class Case3:
    errors = None
    code = """
    predicted: list = ([predicted_columns] if isinstance(predicted_columns, str)
                    else predicted_columns
    )
    """


@register_case
class Case4:
    errors = None
    code = """
    predicted = (
        [predicted_columns] if isinstance(predicted_columns, str)
        else predicted_columns
    )
    """


@register_case
class Case5:
    errors = None
    code = """
    value = func(
        param=1,
    ).arg()
    """


@register_case
class Case6:
    errors = None
    code = """
    value = model.score(
        param=1,
    ) * 2 - 1
    """


@pytest.mark.parametrize('case', CLASSES_REGISTRY.values())
def test_plugin_simple_indent(run_plugin, case):
    """Test plugin on simple indentation."""
    code, expected_errors = case.code, sorted(case.errors or [])
    found_errors = sorted(list(run_plugin(code, strip_tabs=1)))

    if expected_errors:
        assert len(found_errors) == len(expected_errors), f'Case "{case.__name__}" failed'
        for i, msg in enumerate(expected_errors):
            assert found_errors[i].endswith(msg), (
                f'Case "{case.__name__}" failed.\n'
                f'Error: {found_errors[i]}\n'
                f'Expected: {msg}'
            )
    else:
        assert not found_errors, (
            f'Case "{case.__name__}" failed.\n'
            f'Found: {found_errors}\n'
            f'Expected no errors'
        )
