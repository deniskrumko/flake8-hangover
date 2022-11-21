"""
Tests for following rules:
    - FHG002 Function call positional argument has hanging indentation
    - FHG003 Function call keyword argument has hanging indentation
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
    def foo():
        if use_shap:
            shap_values, shap_interaction_values = _calc_shap(
                df, estimator, feature_columns, shap_interactions,
            )
    """


@register_case
class Case2:
    errors = None
    code = """
    def foo():
        if use_shap:
            shap_values, shap_interaction_values = _calc_shap(
                df,
                estimator,
                feature_columns,
                shap_interactions,
            )
    """


@register_case
class Case3:
    errors = [Messages.FHG005]
    code = """
    def foo():
        my_func(value='name',
            other_value='hello')
    """


@register_case
class Case4:
    errors = None
    code = """
    print(  # noqa
        'one line'
        f'{report_dir_path / report_name}', end=' ',
    )
    """


@register_case
class Case5:
    errors = None
    code = """
    try:
        current_controller = CacheController(
            check_version_level=check_version_level,
            check_func_code_hash=check_func_code_hash,
            **controller_kwargs,
        )
    except ValidationError as e:
        raise ValueError()
    """


@register_case
class Case6:
    errors = None
    code = """
    current_controller = CacheController(
        *controller_kwargs,
    )
    """


@register_case
class Case7:
    errors = None
    code = """
    t_group, bins_data = get_groups(
        df=df[feature_columns + [target_column]],
        continuous=continuous,
        categorical=categorical,
        target_column=target_column,
        **(grouping_params or {}),
    )
    """


@register_case
class Case8:
    errors = None
    code = """
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


@register_case
class Case9:
    errors = None
    code = """
    subplot = Plot(
        linewidth=(
            wide_line
            if best_score and score.params == best_score.params
            else default_line
        ),
    )
    """


@register_case
class Case10:
    errors = None
    code = """
    subprocess.run(
        f'python{python_version} -m venv venv',
        shell=True, check=True, cwd=directory,
    )
    """


@register_case
class Case11:
    errors = None
    code = """
    x(
        shell=True,
        check=True,
        cwd=directory,
    )
    """


@register_case
class Case12:
    errors = None
    code = """
    x(
        1,
        2,
        y=10,
    )
    """


@register_case
class Case13:
    errors = None
    code = """
    for key in predictor_instance.dict().keys():
        value = getattr(predictor_instance, key)
    """


@register_case
class Case14:
    errors = None
    code = """
    kafka_config = {'bootstrap.servers': settings["kafka"].get("url")}
    """


@register_case
class Case15:
    errors = None
    code = """
    def _format_error(self, value, message) -> str:
        return (self.error or message).format(
            input=value,
            min=self.format_min(),
            max=self.format_max(),
        )
    """


@register_case
class Case16:
    errors = None
    code = """
    if a != b:
        error_message = get_error_message(param,
            other_param,
        )
    """


@register_case
class Case17:
    errors = None
    code = """
    if a != b:
        error_message = get_error_message(
            param,
            other_param,
        )
    """


@register_case
class Case18:
    errors = [Messages.FHG002, Messages.FHG005]
    code = """
    def foo():
        if use_shap:
            shap_values, shap_interaction_values = _calc_shap(df, estimator, feature_columns,
                                                                shap_interactions)
    """


@register_case
class Case19:
    errors = [Messages.FHG002, Messages.FHG005]
    code = """
    if a != b:
        error_message = get_error_message(param,
                                          other_param)
    """


@register_case
class Case20:
    errors = [Messages.FHG003, Messages.FHG005]
    code = """
    def foo():
        my_func(value='name',
                other_value='hello')
    """


@register_case
class Case21:
    errors = [Messages.FHG005]
    code = """
    def foo():
        my_func(
            value='name',
            other_value='hello')
    """


@register_case
class Case22:
    errors = [Messages.FHG005]
    code = """
    def foo():
        my_func(
            'name',
            'hello')
    """


@register_case
class Case23:
    errors = [Messages.FHG005]
    code = """
    def foo():
        my_func(
            value='name',
            other_value='hello'
            )
    """


@register_case
class Case24:
    errors = [Messages.FHG005]
    code = """
    def foo():
        my_func(
            'name',
            'hello'
            )
    """


@register_case
class Case25:
    errors = [Messages.FHG005]
    code = """
    def foo():
        result = my_func(
            value='name',
            other_value='hello'
            )
    """


@register_case
class Case26:
    errors = None
    code = """
    def foo():
        my_func({(
            'name',
            'hello'
        )})
    """


@register_case
class Case27:
    errors = None
    code = """
    def foo():
        my_func({(
            'name'
        )})
    """


@register_case
class Case28:
    errors = None
    code = """
    def foo():
        my_func({(  # comment with brackets ((
            123
        )})
    """


@register_case
class Case29:
    errors = None
    code = '''
    my_str = """
    hey
    """
    '''


@register_case
class Case30:
    errors = None
    code = """
    hello = '''
    world
    '''
    """


@register_case
class Case31:
    errors = None
    code = """
    @parametrize('value, error_messages', (
        (incorrect_1, None),
    ))
    def my_func():
        pass
    """


@register_case
class Case32:
    errors = None
    code = """
    def shorten_key(value: Any) -> str:
        return divider.join(
            part[:max_part_length]
            for part in value
        )
    """


@register_case
class Case33:
    errors = [Messages.FHG005]
    code = """
    def shorten_key(value: Any) -> str:
        return divider.join(
            part[:max_part_length]
            for part in value)
    """


@register_case
class Case34:
    errors = None
    code = """
    subplot = Plot(
        x=list(range(1, len(score.cv_scores) + 1)),  # number of CV split on X axis
        y=score.cv_scores,  # CV score on Y axis
        label=score.tag or f'#{i}' if enable_labels else None,
        linewidth=(
            wide_line
            if best_score and score.params == best_score.params
            else default_line
        ),
        set_xticks=True,
        plot_type=plot_type,
    )
    """


@register_case
class Case35:
    errors = None
    code = """
    return str(plot_subplots(
        subplots=[plot],
    ))
    """


@register_case
class Case36:
    errors = None
    code = """
    shap_list = np.abs(
        param=10,
    ).mean(0)
    """


@register_case
class Case37:
    errors = None
    code = """
    self.X_val[sorted_columns].columns[
        sorted_importances_idx[::-1]
    ].to_list()
    """


@register_case
class Case38:
    errors = None
    code = """
    result = [Class(
        kw='',
    )]
    """


@pytest.mark.parametrize('case', CLASSES_REGISTRY[__name__].values())
def test_plugin_on_func_call(run_plugin, case):
    """Test plugin on function calls."""
    check_registered_case(run_plugin, case)
