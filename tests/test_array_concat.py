import os
from json import dumps
from typing import Any, Optional, Sequence, Tuple
from tests.util import BTC, execute_sql_file
import pytest

DDL_PATHS: Tuple[str] = ("ddl", "array_concat.sql",)

@pytest.fixture(scope = "module", autouse = True)
def install()-> None:
    """Install stored function into test target DB instance."""
    args: str = execute_sql_file(os.path.join(*DDL_PATHS))
    print(f"Executed below:\n{args}")
    yield
    pass

class TestArrayConcat(BTC):
    @pytest.mark.parametrize(("title", "arr", "start", "stop", "step", "expected"), (
        ("Array.concat(NULL, NULL) -> null", None, None, None),
    ))
    def test_simple(self, title: str, arr1: Sequence[Any], arr2: Sequence[Any], expected: Sequence[Any])-> None:
        cur = self.get_cursor()
        stmt: str = cur.mogrify("SELECT ARRAY_CONCAT(%(arr1)s, %(arr2)s) AS `expected`;", locals())
        cur.execute(stmt)
        raw: str = cur.fetchone()['expected']
        assert expected == raw, stmt

