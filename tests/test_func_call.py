import pytest

from flake8_hangover.plugin import Messages

correct_1 = """
def foo():
    if use_shap:
        shap_values, shap_interaction_values = _calc_shap(
            df, estimator, feature_columns, shap_interactions,
        )
"""

correct_2 = """
def foo():
    if use_shap:
        shap_values, shap_interaction_values = _calc_shap(
            df,
            estimator,
            feature_columns,
            shap_interactions,
        )
"""

correct_3 = """
def foo():
    my_func(value='name',
        other_value='hello')
"""

correct_4 = """
print(  # noqa
    'one line'
    f'{report_dir_path / report_name}', end=' ',
)
"""

correct_5 = """
try:
    current_controller = CacheController(
        check_version_level=check_version_level,
        check_func_code_hash=check_func_code_hash,
        **controller_kwargs,
    )
except ValidationError as e:
    raise ValueError()
"""

correct_6 = """
current_controller = CacheController(
    *controller_kwargs,
)
"""

correct_7 = """
t_group, bins_data = get_groups(
    df=df[feature_columns + [target_column]],
    continuous=continuous,
    categorical=categorical,
    target_column=target_column,
    **(grouping_params or {}),
)
"""

correct_8 = """
return cls(
    func_code_hash=fixed_hash or joblib.hash(
        func.__code__.co_consts
        + (func.__code__.co_code,),
    ),
    func_args_kwargs={
        'args': yaml_repr(func_args or []),
        'kwargs': yaml_repr(func_kwargs or {}),
    },
    **base_meta.dict(),
)
"""

correct_9 = """
subplot = Plot(
    linewidth=(
        wide_line
        if best_score and score.params == best_score.params
        else default_line
    ),
)
"""

correct_10 = """
subprocess.run(
    f'python{python_version} -m venv venv',
    shell=True, check=True, cwd=directory,
)
"""

correct_11 = """
x(
    shell=True,
    check=True,
    cwd=directory,
)
"""

correct_12 = """
x(
    1,
    2,
    y=10,
)
"""

correct_13 = """
for key in predictor_instance.dict().keys():
    value = getattr(predictor_instance, key)
"""

correct_14 = """
kafka_config = {'bootstrap.servers': settings["kafka"].get("url")}
"""

correct_15 = """
def _format_error(self, value, message) -> str:
    return (self.error or message).format(
        input=value,
        min=self.format_min(),
        max=self.format_max(),
    )
"""

incorrect_1 = """
def foo():
    if use_shap:
        shap_values, shap_interaction_values = _calc_shap(df, estimator, feature_columns,
                                                            shap_interactions)
"""

incorrect_2 = """
def foo():
    my_func(value='name',
       other_value='hello')
"""


@pytest.mark.parametrize('value, error_messages', (
    (correct_1, None),
    (correct_2, None),
    (correct_3, None),
    (correct_4, None),
    (correct_5, None),
    (correct_6, None),
    (correct_7, None),
    (correct_8, None),
    (correct_9, None),
    (correct_10, None),
    (correct_11, None),
    (correct_12, None),
    (correct_13, None),
    (correct_14, None),
    (correct_15, None),
    (incorrect_1, [Messages.FHG002]),
    (incorrect_2, [Messages.FHG003]),
))
def test_plugin_on_func_call(run_plugin, value, error_messages):
    """Test plugin on function calls."""
    error_lines = list(run_plugin(value))
    if error_messages:
        assert len(error_lines) == len(error_messages)
        for i, msg in enumerate(error_messages):
            assert error_lines[i].endswith(msg)
    else:
        assert not error_lines
