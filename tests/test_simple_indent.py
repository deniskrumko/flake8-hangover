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


# @register_case
# class Case6:
#     errors = None
#     code = """
#     value = model.score(
#         param=1,
#     ) * 2 - 1
#     """


# @register_case
# class Case7:
#     errors = None
#     code = """
#     final_score['index'] = [
#         i for i in range(0, len(sorted_columns), self.step)
#     ][:final_score.shape[0]]
#     """


# @register_case
# class Case8:
#     errors = None
#     code = """
#     data_to_plot = create_distplot(
#         bin_size=bin_size,
#     ).data
#     """


# @register_case
# class Case9:
#     errors = None
#     code = """
#     class MyClass:
#         some_results: Union[
#             int,
#             HyperparametersOptimizationResult,
#             ModelInterpretationResult,
#         ] = 100
#     """


# @register_case
# class Case10:
#     errors = None
#     code = """
#     n_best_scores = sorted(
#         deserialized_scores,
#     )[-max_scores_on_plot:]
#     """


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
