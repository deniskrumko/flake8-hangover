import pytest

from flake8_hangover.plugin import Messages

from .conftest import (
    CLASSES_REGISTRY,
    check_registered_case,
    register_case,
)


@register_case
class Case1:
    errors = [Messages.FHG005]
    code = """
    predicted: list = ([predicted_columns] if isinstance(predicted_columns, str)
                    else predicted_columns)
    """


@register_case
class Case2:
    errors = [Messages.FHG005]
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


@register_case
class Case7:
    errors = None
    code = """
    final_score['index'] = [
        i for i in range(0, len(sorted_columns), self.step)
    ][:final_score.shape[0]]
    """


@register_case
class Case8:
    errors = None
    code = """
    data_to_plot = create_distplot(
        bin_size=bin_size,
    ).data
    """


@register_case
class Case9:
    errors = None
    code = """
    class MyClass:
        some_results: Union[
            int,
            HyperparametersOptimizationResult,
            ModelInterpretationResult,
        ] = 100
    """


@register_case
class Case10:
    errors = None
    code = """
    n_best_scores = sorted(
        deserialized_scores,
    )[-max_scores_on_plot:]
    """


@pytest.mark.parametrize('case', CLASSES_REGISTRY[__name__].values())
def test_plugin_simple_indent(run_plugin, case):
    """Test plugin on simple indentation."""
    check_registered_case(run_plugin, case)
