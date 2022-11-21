[![pypi](https://img.shields.io/pypi/v/flake8-hangover.svg)](https://pypi.org/project/flake8-hangover/)
[![pypi](https://img.shields.io/pypi/pyversions/flake8-hangover.svg)](https://pypi.org/project/flake8-hangover/)
[![pypi](https://img.shields.io/pypi/l/flake8-hangover.svg)](https://raw.githubusercontent.com/deniskrumko/flake8-hangover/master/LICENSE)

# flake8-hangover
Flake8 plugin to prevent specific hanging indentations (and more).

# Installation

```
pip install flake8-hangover
```

# Errors

| Code   | Description                                                |
|--------|------------------------------------------------------------|
| FHG001 | Function argument has hanging indentation                  |
| FHG002 | Function call positional argument has hanging indentation  |
| FHG003 | Function call keyword argument has hanging indentation     |
| FHG004 | First function argument must be on new line                |
| FHG005 | Close bracket have different indentation with open bracket |

# Examples

## FHG001 Function argument has hanging indentation

```python
# ERROR: Hanging indentation on `extra_param`
def _hello_world(param: pd.DataFrame, other_param: sklearn.base.BaseEstimator,
                 extra_param: Optional[Dict] = None) -> str:
    ...

# ERROR: Not hanging indentation, but params are "over indendented" by 2 tabs
# instead of just 1 tab
def _calc_pdp(
        df: pd.DataFrame,
        estimator: sklearn.base.BaseEstimator,
        feature_columns: List[str], pdp_kwarg: Optional[Dict] = None,
) -> List[pdp.PDPIsolate]:
    pdp_isolates = []

# OK: Correct indentation
# BUT! It will cause FHG004 error (it's more strict) for `param` argument
def _hello_world(param: pd.DataFrame, other_param: sklearn.base.BaseEstimator,
    extra_param: Optional[Dict] = None) -> str:
    ...

# OK: Best practice
def _hello_world(
    param: pd.DataFrame,
    other_param: sklearn.base.BaseEstimator,
    extra_param: Optional[Dict] = None,
) -> str:
    ...
```

## FHG002 Function call positional argument has hanging indentation

```python
# ERROR: Hanging indentation on `other_param`
if a != b:
    error_message = get_error_message(param,
                                      other_param)

# OK: Correct indentation
if a != b:
    error_message = get_error_message(param,
        other_param,
    )

# OK: Best practice
if a != b:
    error_message = get_error_message(
        param,
        other_param,
    )
```

## FHG003

```python
# ERROR: Keyword argument `other_value` has hanging indentation
def foo():
    result = my_func(value='name',
                     other_value='hello')

# Correct indentation, but looks terrible
# TODO: Rule like FHG004 for function calls is not yet implemented
def foo():
    result = my_func(value='name',
        other_value='hello')

# OK: Best practice
def foo():
    result = my_func(
        value='name',
        other_value='hello',
    )
```

## FHG004 First function argument must be on new line

This is more strict rule that requires any function definition with multiline arguments to
place first argument on new line.

```python
# ERROR: Positional argument `foo` must be on new line
def test_something(foo, bar,
    buzz):
    ...

# ERROR: Same thing but for keyword argument `foo`
def test_something(foo='Hello',
    value='World',
):
    return key + value

# OK: Argument `foo` is on new line
def test_something(
    foo, bar, buzz,
):
    ...

# OK: Best practice (but sometimes it's not good looking for over 5 params, for example)
def test_something(
    foo,
    bar,
    buzz,
):
    ...
```

## FHG005 Close bracket have different indentation with open bracket

```python
# ERROR: Close bracket on line with last parameter not allowed
func(
    123,
    456)
```

```python
# OK: Close bracket on new line
func(
    123,
    456,
)
```

Same thing with assigments:

```python
# ERROR: Close bracket not aligned with open bracket's line
result = [
    1,
    2]
```

```python
# OK: Close bracket aligned with first line
result = [
    1,
    2,
]
```
