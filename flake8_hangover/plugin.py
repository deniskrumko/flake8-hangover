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


class Visitor(ast.NodeVisitor):
    """Class for visiting ast nodes."""

    def __init__(self) -> None:
        """Initialize class instance."""
        self.errors: List[Tuple[int, int, str]] = []

    def visit_Call(self, node: ast.Call) -> None:
        """Visit ``Call`` node."""
        cur_lineno = node.lineno
        func_name_offset = None

        # Iterate over positional arguments
        for arg in node.args:
            col_offset = arg.col_offset
            lineno = arg.lineno

            if lineno - cur_lineno == 1:
                if func_name_offset is None:
                    func_name_offset = self._get_func_name_offset(node)

                if col_offset > func_name_offset or col_offset % TAB_SIZE != 0:
                    self.errors.append((lineno, col_offset, Messages.FHG002))

            cur_lineno = getattr(arg, 'end_lineno', lineno)

        # Iterate over keyword arguments
        for kwarg in node.keywords:
            col_offset = kwarg.value.col_offset - len(str(kwarg.arg or '')) - 1  # 1 is for "="
            lineno = kwarg.value.lineno

            if lineno - cur_lineno == 1:
                if func_name_offset is None:
                    func_name_offset = self._get_func_name_offset(node)

                if (
                    col_offset > func_name_offset
                    or (kwarg.arg and col_offset % TAB_SIZE != 0)
                ):
                    self.errors.append((lineno, col_offset, Messages.FHG003))

            cur_lineno = getattr(kwarg, 'end_lineno', lineno)

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
        for arg in node.args.args:
            if arg.lineno != cur_lineno:
                if arg.col_offset != node.col_offset + 4:
                    self.errors.append((arg.lineno, arg.col_offset, Messages.FHG001))
                cur_lineno = arg.lineno

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
