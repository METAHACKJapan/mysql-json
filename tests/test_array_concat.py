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
    @pytest.mark.parametrize(("title", "arr1", "arr2", "expected"), (
        ("Array.concat(null, null) -> null", None, None, None),
        ("Array.concat([1, 2, 3], null)", dumps([1, 2, 3]), None, None),
        ("Array.concat(null, [1, 2, 3])", None, dumps([1, 2, 3]), None),
        ("Array.concat([], []) -> []", dumps([]), dumps([]), dumps([])),
        ("Array.concat(null, []) -> null", None, dumps([]), None),
        ("Array.concat([], null) -> null", dumps([]), None, None),
    ))
    def test_null_boundary(self, title: str, arr1: Sequence[Any], arr2: Sequence[Any], expected: Sequence[Any])-> None:
        cur = self.get_cursor()
        stmt: str = cur.mogrify("SELECT ARRAY_CONCAT(%(arr1)s, %(arr2)s) AS `expected`;", locals())
        cur.execute(stmt)
        raw: str = cur.fetchone()['expected']
        assert expected == raw, stmt

    @pytest.mark.parametrize(("title", "arr1", "arr2", "expected"), (
        ("Array.concat([], [1, 2, 3]) -> [1, 2, 3]", dumps([]), dumps([1, 2, 3]), dumps([1, 2, 3])),
        ("Array.concat([1, 2, 3], []) -> [1, 2, 3]", dumps([]), dumps([1, 2, 3]), dumps([1, 2, 3])),
        ("Array.concat([1, 2, 3], [4, 5, 6]) -> [1, 2, 3, 4, 5, 6]", dumps([1, 2, 3]), dumps([4, 5, 6]), dumps([1, 2, 3, 4, 5, 6])),
        ("Array.concat([4, 5, 6], [1, 2, 3]) -> [4, 5, 6, 1, 2, 3]", dumps([4, 5, 6]), dumps([1, 2, 3]), dumps([4, 5, 6, 1, 2, 3])),
    ))
    def test_simple_number_element(self, title: str, arr1: Sequence[Any], arr2: Sequence[Any], expected: Sequence[Any])-> None:
        cur = self.get_cursor()
        stmt: str = cur.mogrify("SELECT ARRAY_CONCAT(%(arr1)s, %(arr2)s) AS `expected`;", locals())
        cur.execute(stmt)
        raw: str = cur.fetchone()['expected']
        assert expected == raw, stmt

