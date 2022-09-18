import ast
from typing import (
    Any,
    Generator,
    List,
    Tuple,
    Type,
)

TAB_SIZE = 4


class Messages:
    """Linter messages."""

    FHG001 = 'FHG001 Function argument has hanging indentation'
    FHG002 = 'FHG002 Function call positional argument has hanging indentation'
    FHG003 = 'FHG003 Function call keyword argument has hanging indentation'
    FHG004 = 'FHG004 First function argument must be on new line'
    FHG005 = 'FHG005 Function close bracket must be on new line'
    FHG006 = 'FHG006 Function close bracket got over indentation'


class Visitor(ast.NodeVisitor):
    """Class for visiting ast nodes."""

    def __init__(self) -> None:
        """Initialize class instance."""
        self.errors: List[Tuple[int, int, str]] = []

    def visit_Call(self, node: ast.Call) -> None:
        """Visit ``Call`` node."""
        cur_lineno = node.lineno
        func_name_offset = None
        args_min_offset = node.col_offset + TAB_SIZE
        end_lineno = node.end_lineno or 0
        end_col_offset = node.end_col_offset or 0
        close_brackets_count = 1  # allow structure open/close brackets at the same lines as call
        last_inner_lineno = cur_lineno  # not include args which started with node

        # Iterate over positional arguments
        for arg in node.args:
            col_offset = arg.col_offset
            lineno = arg.lineno
            args_min_offset = min(args_min_offset, arg.col_offset)
            for subnode in ast.walk(arg):
                if (
                    getattr(subnode, 'lineno', None) == node.lineno
                    and getattr(subnode, 'end_lineno', None) == end_lineno
                ):
                    close_brackets_count += 1

            if lineno - cur_lineno == 1:
                if func_name_offset is None:
                    func_name_offset = self._get_func_name_offset(node)

                if col_offset > func_name_offset or col_offset % TAB_SIZE != 0:
                    self.errors.append((lineno, col_offset, Messages.FHG002))

            cur_lineno = getattr(arg, 'end_lineno', lineno)
            if lineno != node.lineno:
                last_inner_lineno = max(last_inner_lineno, cur_lineno)

        # Iterate over keyword arguments
        for kwarg in node.keywords:
            col_offset = kwarg.value.col_offset - len(str(kwarg.arg or '')) - 1  # 1 is for "="
            lineno = kwarg.value.lineno
            args_min_offset = min(args_min_offset, kwarg.col_offset)

            if lineno - cur_lineno == 1:
                if func_name_offset is None:
                    func_name_offset = self._get_func_name_offset(node)

                if (
                    col_offset > func_name_offset
                    or (kwarg.arg and col_offset % TAB_SIZE != 0)
                ):
                    self.errors.append((lineno, col_offset, Messages.FHG003))

            cur_lineno = getattr(kwarg, 'end_lineno', lineno)
            if kwarg.lineno != node.lineno:
                last_inner_lineno = max(last_inner_lineno, cur_lineno)

        if node.lineno != cur_lineno:  # skip one-liners
            if end_lineno == last_inner_lineno:  # close bracker on the same line as last param
                self.errors.append((end_lineno, end_col_offset, Messages.FHG005))
            elif end_col_offset - close_brackets_count != args_min_offset - TAB_SIZE:
                # last line should contain same brackets count as started on first nodes' line
                self.errors.append((end_lineno, end_col_offset, Messages.FHG006))

        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Visit ``FunctionDef`` node."""
        self._check_func_args_indentations(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        """Visit ``AsyncFunctionDef`` node."""
        self._check_func_args_indentations(node)
        self.generic_visit(node)

    def _check_func_args_indentations(self, node: Any) -> None:
        """Check indentations in function args/kwargs."""
        cur_lineno = node.lineno
        first_argument = None
        multiline_arguments = False

        for i, arg in enumerate(node.args.args):
            if i == 0:
                first_argument = (arg.lineno, arg.col_offset)

            if arg.lineno != cur_lineno:
                if arg.col_offset != node.col_offset + 4:
                    self.errors.append((arg.lineno, arg.col_offset, Messages.FHG001))
                cur_lineno = arg.lineno
                multiline_arguments = True

        if (
            multiline_arguments
            and first_argument
            and first_argument[0] == node.lineno
        ):
            self.errors.append(first_argument + (Messages.FHG004,))

    def _get_func_name_offset(self, node: Any) -> int:
        """Get function name offset."""
        func_name = self._get_func_name(node.func)
        return int(node.col_offset + max(len(func_name), TAB_SIZE))

    def _get_func_name(self, obj: Any) -> str:
        """Extract function full name from node.

        May not fully correctly work. For this cases function returns empty string.
        """
        try:
            if isinstance(obj, ast.Attribute):
                return f'{self._get_func_name(obj.value)}.{obj.attr}'
            if isinstance(obj, ast.Call):
                return self._get_func_name(obj.func)
            if isinstance(obj, ast.Subscript):
                return f'{self._get_func_name(obj.value)}[{self._get_func_name(obj.slice)}]'
            if isinstance(obj, ast.Index):
                return self._get_func_name(obj.value)
            if isinstance(obj, ast.Constant):
                return str(obj.value)

            return str(obj.id)
        except Exception:
            return ''


class Plugin:
    """Class to run flake8 plugin."""

    name = 'flake8-hangover'

    def __init__(self, tree: ast.AST):
        """Initialize class instance."""
        self._tree = tree

    @property
    def version(self) -> str:
        """Get package version."""
        from . import __version__
        return __version__

    def run(self) -> Generator[Tuple[int, int, str, Type[Any]], None, None]:
        """Run plugin."""
        visitor = Visitor()
        visitor.visit(self._tree)

        for lineno, col_offset, error_msg in visitor.errors:
            yield lineno, col_offset, error_msg, type(self)
