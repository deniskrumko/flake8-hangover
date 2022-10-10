"""
Tests for following rules:
    - FHG001 Function argument has hanging indentation
"""
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
    errors = None
    code = """
    def _calc_pdp(
        df: pd.DataFrame, estimator: sklearn.base.BaseEstimator, feature_columns: List[str],
        pdp_kwarg: Optional[Dict] = None,
    ) -> List[pdp.PDPIsolate]:
        pdp_isolates = []
    """


@register_case
class Case2:
    errors = None
    code = """
    def _calc_pdp(
        df: pd.DataFrame,
        estimator: sklearn.base.BaseEstimator,
        feature_columns: List[str],
        pdp_kwarg: Optional[Dict] = None,
    ) -> List[pdp.PDPIsolate]:
        pdp_isolates = []
    """


@register_case
class Case3:
    errors = None
    code = """
    def _calc_pdp(df: pd.DataFrame, estimator: sklearn.base.BaseEstimator) -> List[pdp.PDPIsolate]:
        pdp_isolates = []
    """


@register_case
class Case4:
    errors = None
    code = """
    def _calc_pdp(
        df: pd.DataFrame,
        estimator: sklearn.base.BaseEstimator,
        feature_columns: List[str], pdp_kwarg: Optional[Dict] = None,
    ) -> List[pdp.PDPIsolate]:
        pdp_isolates = []
    """


@register_case
class Case5:
    errors = None
    code = """
    def _hello_world(
        param: pd.DataFrame,
        other_param: sklearn.base.BaseEstimator,
        extra_param: Optional[Dict] = None,
    ) -> str:
        ...
    """


@register_case
class Case6:
    errors = [Messages.FHG004]
    code = """
    def _hello_world(param: pd.DataFrame, other_param: sklearn.base.BaseEstimator,
        extra_param: Optional[Dict] = None) -> str:
        ...
    """


@register_case
class Case7:
    errors = [Messages.FHG004, Messages.FHG001]
    code = """
    def _calc_pdp(df: pd.DataFrame, estimator: sklearn.base.BaseEstimator,
                pdp_kwarg: Optional[Dict]) -> List[pdp.PDPIsolate]:
        pdp_isolates = []
    """


@register_case
class Case8:
    errors = [Messages.FHG004, Messages.FHG001]
    code = """
    def _hello_world(param: pd.DataFrame, other_param: sklearn.base.BaseEstimator,
                    extra_param: Optional[Dict] = None) -> str:
        ...
    """


@register_case
class Case9:
    errors = [Messages.FHG001] * 3
    code = """
    def _calc_pdp(
            df: pd.DataFrame,
            estimator: sklearn.base.BaseEstimator,
            feature_columns: List[str], pdp_kwarg: Optional[Dict] = None,
    ) -> List[pdp.PDPIsolate]:
        pdp_isolates = []
    """


@register_case
class Case10:
    errors = [Messages.FHG004]
    code = """
    def test_something(foo, bar,
        buzz):
        return None
    """


@register_case
class Case11:
    errors = [Messages.FHG004]
    code = """
    def test_something(key=foo,
        value=buzz,
    ):
        return key + value
    """


@register_case
class Case12:
    errors = None
    code = """
    def test_something(
        foo, bar, buzz,
    ):
        return None
    """


@pytest.mark.parametrize('case', CLASSES_REGISTRY.values())
def test_plugin_on_func_definition(run_plugin, case):
    """Test plugin on function definitions."""
    code, expected_errors = case.code, case.errors
    found_errors = sorted(run_plugin(code, strip_tabs=1))

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


@pytest.mark.parametrize('case', CLASSES_REGISTRY.values())
def test_plugin_on_async_func_definition(run_plugin, case):
    """Test plugin on async function definitions."""
    code, expected_errors = case.code, case.errors
    code = code.replace('def ', 'async def ')
    found_errors = sorted(run_plugin(code, strip_tabs=1))

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
