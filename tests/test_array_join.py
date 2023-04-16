import os
from json import dumps
from typing import Any, Optional, Sequence, Tuple
from tests.util import BTC, execute_sql_file
import pytest

DDL_PATHS: Tuple[str] = ("ddl", "array_join.sql",)

@pytest.fixture(scope = "module", autouse = True)
def install()-> None:
    """Install stored function into test target DB instance."""
    args: str = execute_sql_file(os.path.join(*DDL_PATHS))
    print(f"Executed below:\n{args}")
    yield
    pass

class TestArrayJoin(BTC):
    @pytest.mark.parametrize(("title", "arr", "separator_chars", "expected"), (
        ("Array.join(null, null) -> null", dumps(None), None, None),
    ))
    def test_null_boundary(self, title: str, arr: Sequence[Any], separator_chars: str, expected: Sequence[Any])-> None:
        cur = self.get_cursor()
        stmt: str = cur.mogrify("SELECT ARRAY_JOIN(%(arr)s, %(separator_chars)s) AS `expected`;", locals())
        cur.execute(stmt)
        raw: str = cur.fetchone()['expected']
        assert expected == raw, stmt

