# flake8-hangover
Flake8 plugin to prevent specific hanging indentations (and more).

# Installation

```
pip install flake8-hangover
```

# Errors

| Code   | Description                                               |
|--------|-----------------------------------------------------------|
| FHG001 | Function argument has hanging indentation                 |
| FHG002 | Function call positional argument has hanging indentation |
| FHG003 | Function call keyword argument has hanging indentation    |

# Examples

## FHG001 Function argument has hanging indentation

```python
# Hanging indentation on `extra_param`
def _hello_world(param: pd.DataFrame, other_param: sklearn.base.BaseEstimator,
                 extra_param: Optional[Dict] = None) -> str:
    ...

# Correct indentation
def _hello_world(param: pd.DataFrame, other_param: sklearn.base.BaseEstimator,
    extra_param: Optional[Dict] = None) -> str:
    ...

# Best practice
def _hello_world(
    param: pd.DataFrame,
    other_param: sklearn.base.BaseEstimator,
    extra_param: Optional[Dict] = None,
) -> str:
    ...
```

## FHG002 Function call positional argument has hanging indentation

```python
# Hanging indentation on `other_param`
if a != b:
    error_message = get_error_message(param,
                                      other_param)

# Correct indentation
if a != b:
    error_message = get_error_message(param,
        other_param,
    )

# Best practice
if a != b:
    error_message = get_error_message(
        param,
        other_param,
    )
```


# Not yet implemented cases

Hanging indentation in cases with brackets like this is not yet checked by linter:
```python
# Hanging indentation on `World`
my_string = ('Hello '
             'World')
```
