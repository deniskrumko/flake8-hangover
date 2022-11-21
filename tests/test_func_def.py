"""
Tests for following rules:
    - FHG001 Function argument has hanging indentation
"""
import pytest

from flake8_hangover.plugin import Messages

from .conftest import (
    CLASSES_REGISTRY,
    check_registered_case,
    register_case,
)


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
    errors = [Messages.FHG004, Messages.FHG005]
    code = """
    def _hello_world(param: pd.DataFrame, other_param: sklearn.base.BaseEstimator,
        extra_param: Optional[Dict] = None) -> str:
        ...
    """


@register_case
class Case7:
    errors = [Messages.FHG004, Messages.FHG001, Messages.FHG005]
    code = """
    def _calc_pdp(df: pd.DataFrame, estimator: sklearn.base.BaseEstimator,
                pdp_kwarg: Optional[Dict]) -> List[pdp.PDPIsolate]:
        pdp_isolates = []
    """


@register_case
class Case8:
    errors = [Messages.FHG004, Messages.FHG001, Messages.FHG005]
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
    errors = [Messages.FHG004, Messages.FHG005]
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


@pytest.mark.parametrize('case', CLASSES_REGISTRY[__name__].values())
def test_plugin_on_func_definition(run_plugin, case):
    """Test plugin on function definitions."""
    check_registered_case(run_plugin, case)


@pytest.mark.parametrize('case', CLASSES_REGISTRY[__name__].values())
def test_plugin_on_async_func_definition(run_plugin, case):
    """Test plugin on async function definitions."""
    check_registered_case(
        run_plugin,
        case,
        case_name=f'ASYNC {case.__name__}',
        case_code=case.code.replace('def ', 'async def '),
    )
