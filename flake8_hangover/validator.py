from queue import LifoQueue
from token import (
    DEDENT,
    INDENT,
    OP,
)
from tokenize import TokenInfo
from typing import (
    Dict,
    List,
    Optional,
    Tuple,
)

from .messages import Messages


class Parenthese:
    """Store full info for single parentheses."""

    def __init__(
        self,
        line: int,
        column: int,
        type: int,
        open: bool,
        indent: int = 0,
        pair: Optional['Parenthese'] = None,
    ) -> None:
        self.line = line
        self.column = column
        self.type = type
        self.open = open
        self.indent = indent
        self.pair = pair

    @classmethod
    def parse_token(
        cls, token: TokenInfo, indents: Dict[int, int],
    ) -> Optional['Parenthese']:
        """Create class instance from token."""
        if token.type != OP or token.string not in '()[]{}':
            return None
        return cls(
            line=token.start[0],
            column=token.start[1],
            type=cls.get_type(token.string),
            open=token.string in '([{',
            indent=indents[token.start[0]],
        )

    @classmethod
    def get_type(cls, s: str) -> int:
        """Split tokens by type."""
        types = {'(': 1, ')': 1, '[': 2, ']': 2, '{': 3, '}': 3}
        return types.get(s, 0)

    def __repr__(self) -> str:
        """Object representation."""
        s = f"{self.line}:{self.column} ({self.indent}) type:{self.type} open:{self.open}"
        if self.pair:
            s += f" | pair: <{self.pair.line}:{self.pair.column} ({self.pair.indent})>"
        return s


class IndentValidator:
    """Validate close parentheses have the same line indent as open ones."""

    def __init__(self, tokens: List[TokenInfo]) -> None:
        self.tokens = tokens
        self.errors: Dict[Tuple[int, int], str] = {}

    def validate(self) -> None:
        """Check all parentheses"""
        indents = self.calculate_indents(self.tokens)
        parentheses = self.parse_parentheses(self.tokens, indents)
        for p in parentheses:
            if not p.open:
                continue
            if not p.pair or p.line == p.pair.line:
                continue
            if p.indent != p.pair.indent:
                self.errors[(p.pair.line, p.pair.column)] = Messages.FHG005

    def calculate_indents(self, tokens: List[TokenInfo]) -> Dict[int, int]:
        """Calculate the indent for each line in the code."""
        indents = {}
        for t in tokens:
            if t.type in (INDENT, DEDENT):
                continue
            line = t.start[0]
            if line not in indents:
                indents[line] = t.start[1]
        return indents

    def parse_parentheses(
        self,
        tokens: List[TokenInfo],
        indents: Dict[int, int],
    ) -> List[Parenthese]:
        """Parse all parentheses with their positions."""
        parentheses: List[Parenthese] = []
        # find all parentheses
        for t in tokens:
            p = Parenthese.parse_token(t, indents)
            if not p:
                continue
            parentheses.append(p)
        # find pairs for each parentheses
        queues: Dict[int, LifoQueue] = {1: LifoQueue(), 2: LifoQueue(), 3: LifoQueue()}
        for p in parentheses:
            if p.open:
                queues[p.type].put(p)
            else:
                if queues[p.type].empty():
                    raise ValueError(f"Unexpected close parentheses {p}")
                p_open = queues[p.type].get()
                p.pair = p_open
                p_open.pair = p
                assert p.open != p_open.open
                assert p.type == p_open.type
        return parentheses
