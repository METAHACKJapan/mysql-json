import os
from json import dumps, loads
from typing import Any, Optional, Sequence, Tuple
from tests.util import BTC, execute_sql_file
import pytest

DDL_PATHS: Tuple[str] = ("ddl", "str_split_to_json_array.sql",)

@pytest.fixture(scope = "module", autouse = True)
def install()-> None:
    """Install stored function into test target DB instance."""
    args: str = execute_sql_file(os.path.join(*DDL_PATHS))
    print(f"Executed below:\n{args}")
    yield
    pass

class TestStrSplitToJsonArray(BTC):
    @pytest.mark.parametrize(("title", "source_chars", "separator_chars", "expected"), (
        ("""String.split(null, null) -> null""",
            None, None, dumps(None),),
        ("""String.split([], null) -> []""",
            dumps([]), None, """["[]"]""",),
        ("""String.split("a,b,c,d", null) -> ["a", "b", "c", "d"]""",
            "a,b,c,d", None, dumps(["a", "b", "c", "d"]),),
        ("""String.split("a|b|c|d", null) -> ["a|b|c|d"]""",
            "a|b|c|d", None, dumps(["a|b|c|d"]),),
        ("""String.split("a|b|c|d", "|") -> ["a", "b", "c", "d"]""",
            "a|b|c|d", "|", dumps(["a", "b", "c", "d"]),),
        ("""String.split("a, b, c, d", ", ") -> ["a", "b", "c", "d"]""",
            "a, b, c, d", ", ", dumps(["a", "b", "c", "d"]),),
    ))
    def test_simple(self, title: str, source_chars: str, separator_chars: str, expected: Sequence[Any])-> None:
        cur = self.get_cursor()
        stmt: str = cur.mogrify("SELECT STR_SPLIT_TO_JSON_ARRAY(%(source_chars)s, %(separator_chars)s) AS `expected`;", locals())
        cur.execute(stmt)
        raw: str = cur.fetchone()['expected']
        assert expected == raw, stmt
