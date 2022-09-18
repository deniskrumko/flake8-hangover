import ast
import tokenize
from typing import (
    Any,
    Generator,
    List,
    Tuple,
    Type,
    Union,
)

from flake8.processor import count_parentheses

TAB_SIZE = 4


class Messages:
    """Linter messages."""

    FHG001 = 'FHG001 Function argument has hanging indentation'
    FHG002 = 'FHG002 Function call positional argument has hanging indentation'
    FHG003 = 'FHG003 Function call keyword argument has hanging indentation'
    FHG004 = 'FHG004 First function argument must be on new line'
    FHG005 = 'FHG005 Function close bracket must be on new line'
    FHG006 = 'FHG006 Function close bracket got over indentation'
    FHG007 = 'FHG007 Assignment close bracket must be on new line'


class Visitor(ast.NodeVisitor):
    """Class for visiting ast nodes."""

    def __init__(self, tokens: List[tokenize.TokenInfo]) -> None:
        """Initialize class instance."""
        self.errors: List[Tuple[int, int, str]] = []
        self._tokens = tokens

    def visit_Call(self, node: ast.Call) -> None:
        """Visit ``Call`` node."""
        cur_lineno = node.lineno
        func_name_offset = None
        args_min_offset = node.col_offset + TAB_SIZE
        end_lineno = node.end_lineno or 0
        end_col_offset = node.end_col_offset or 0
        last_inner_lineno = cur_lineno  # not include args which started at the same line as node

        # Iterate over positional arguments
        for arg in node.args:
            col_offset = arg.col_offset
            lineno = arg.lineno
            args_min_offset = min(args_min_offset, arg.col_offset)

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
            # get expected brackets number for last line
            # 1 in case there is something other then bracket at the end of the line
            expected_brackets = self._count_brackets(node.lineno, node.col_offset, True) or 1
            if end_lineno == last_inner_lineno:  # close bracker on the same line as last param
                self.errors.append((end_lineno, end_col_offset, Messages.FHG005))
            elif end_col_offset - expected_brackets != args_min_offset - TAB_SIZE:
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

    def visit_Assign(self, node: ast.Assign) -> None:
        """Visit ``Assign`` node."""
        self._check_assign(node)
        self.generic_visit(node)

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        """Visit ``AnnAssign`` node."""
        self._check_assign(node)
        self.generic_visit(node)

    def visit_AugAssign(self, node: ast.AugAssign) -> None:
        """Visit ``AugAssign`` node."""
        self._check_assign(node)
        self.generic_visit(node)

    def _check_assign(self, node: Union[ast.Assign, ast.AnnAssign, ast.AugAssign]) -> None:
        """Check close bracket for assign is on new line and with corrent indent."""
        start_lineno = node.lineno
        end_lineno = node.end_lineno or start_lineno
        start_offset = node.col_offset
        end_offset = node.end_col_offset or start_offset
        if start_lineno == end_lineno:  # skip one-liners
            return
        start_line_tokens = self._get_tokens_for_line(start_lineno)
        start_indent = self._get_indent(start_line_tokens)
        open_brackets = sum((count_parentheses(0, token.string) for token in start_line_tokens))
        # all opened brackets on line with assign started should be closed on last assign` line
        if end_offset != start_indent + open_brackets:
            self.errors.append((end_lineno, end_offset, Messages.FHG007))

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

    def _get_tokens_for_line(self, line: int) -> List[tokenize.TokenInfo]:
        result = []
        for token in self._tokens:
            if token.start[0] == line:
                result.append(token)
        return result

    def _get_indent(self, tokens: List[tokenize.TokenInfo]) -> int:
        for token in tokens:
            if token.type == tokenize.INDENT:
                return token.end[1]
        return 0

    def _count_brackets(self, lineno: int, start_offset: int, find_open: bool) -> int:
        """Count open / close brackets at the end of specific line."""
        SKIP_TOKENS = {
            tokenize.NL, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT, tokenize.COMMENT,
        }
        OPEN_BRACKETS = {'(', '{', '['}
        CLOSE_BRACKETS = {')', '}', ']'}
        bracket_count = 0
        for token in reversed(self._get_tokens_for_line(lineno)):
            line, offset = token.start
            if offset < start_offset:
                # just in case nothing found
                break
            if token.type in SKIP_TOKENS:
                # skip empty ones and comments
                continue
            if token.type == tokenize.OP:
                # get all bracket from the end of the line
                if (
                    (find_open and token.string in OPEN_BRACKETS)
                    or (not find_open and token.string in CLOSE_BRACKETS)
                ):
                    bracket_count += 1
                    continue
            # non-bracket token found
            break
        return bracket_count


class Plugin:
    """Class to run flake8 plugin."""

    name = 'flake8-hangover'

    def __init__(self, tree: ast.AST, file_tokens: List[tokenize.TokenInfo]):
        """Initialize class instance."""
        self._tree = tree
        self._tokens = file_tokens

    @property
    def version(self) -> str:
        """Get package version."""
        from . import __version__
        return __version__

    def run(self) -> Generator[Tuple[int, int, str, Type[Any]], None, None]:
        """Run plugin."""
        visitor = Visitor(tokens=self._tokens)
        visitor.visit(self._tree)

        for lineno, col_offset, error_msg in visitor.errors:
            yield lineno, col_offset, error_msg, type(self)
