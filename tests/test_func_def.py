import pytest

from flake8_hangover.plugin import Messages

correct_1 = """
def _calc_pdp(
    df: pd.DataFrame, estimator: sklearn.base.BaseEstimator, feature_columns: List[str],
    pdp_kwarg: Optional[Dict] = None,
) -> List[pdp.PDPIsolate]:
    pdp_isolates = []
"""

correct_2 = """
def _calc_pdp(
    df: pd.DataFrame,
    estimator: sklearn.base.BaseEstimator,
    feature_columns: List[str],
    pdp_kwarg: Optional[Dict] = None,
) -> List[pdp.PDPIsolate]:
    pdp_isolates = []
"""

correct_3 = """
def _calc_pdp(df: pd.DataFrame, estimator: sklearn.base.BaseEstimator) -> List[pdp.PDPIsolate]:
    pdp_isolates = []
"""

correct_4 = """
def _calc_pdp(
    df: pd.DataFrame,
    estimator: sklearn.base.BaseEstimator,
    feature_columns: List[str], pdp_kwarg: Optional[Dict] = None,
) -> List[pdp.PDPIsolate]:
    pdp_isolates = []
"""

incorrect_1 = """
def _calc_pdp(df: pd.DataFrame, estimator: sklearn.base.BaseEstimator, feature_columns: List[str],
              pdp_kwarg: Optional[Dict]) -> List[pdp.PDPIsolate]:
    pdp_isolates = []
"""

incorrect_2 = """
def _calc_pdp(
        df: pd.DataFrame,
        estimator: sklearn.base.BaseEstimator,
        feature_columns: List[str], pdp_kwarg: Optional[Dict] = None,
) -> List[pdp.PDPIsolate]:
    pdp_isolates = []
"""


@pytest.mark.parametrize('value, error_messages', (
    (correct_1, None),
    (correct_2, None),
    (correct_3, None),
    (incorrect_1, [Messages.FHG001]),
    (incorrect_2, [Messages.FHG001] * 3),
))
def test_plugin_on_func_definition(run_plugin, value, error_messages):
    """Test plugin on function definitions."""
    error_lines = list(run_plugin(value))
    if error_messages:
        assert len(error_lines) == len(error_messages)
        for i, msg in enumerate(error_messages):
            assert error_lines[i].endswith(msg)
    else:
        assert not error_lines


@pytest.mark.parametrize('value, error_messages', (
    (correct_1, None),
    (correct_2, None),
    (correct_3, None),
    (incorrect_1, [Messages.FHG001]),
    (incorrect_2, [Messages.FHG001] * 3),
))
def test_plugin_on_async_func_definition(run_plugin, value, error_messages):
    """Test plugin on async function definitions."""
    value = value.replace('def ', 'async def ')
    error_lines = list(run_plugin(value))
    if error_messages:
        assert len(error_lines) == len(error_messages)
        for i, msg in enumerate(error_messages):
            assert error_lines[i].endswith(msg)
    else:
        assert not error_lines
