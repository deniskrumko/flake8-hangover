"""
NOTE: These cases are not implemented yet
"""
import pytest

incorrect_1 = """
predicted: list = ([predicted_columns] if isinstance(predicted_columns, str)
                   else predicted_columns)
"""


@pytest.mark.parametrize('value, error_messages', (
    (incorrect_1, None),
    # (incorrect_1, [Messages.FHG004]),
))
def test_plugin_on_simple_indentation(run_plugin, value, error_messages):
    """Test plugin on simple indentation.

    TODO: This check is not yet implemented.
    """
    error_lines = list(run_plugin(value))
    if error_messages:
        assert len(error_lines) == len(error_messages)
        for i, msg in enumerate(error_messages):
            assert error_lines[i].endswith(msg)
    else:
        assert not error_lines
