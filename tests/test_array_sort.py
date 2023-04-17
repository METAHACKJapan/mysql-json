import os
from json import dumps
from typing import Any, Optional, Sequence, Tuple
from tests.util import BTC, execute_sql_file
import pytest
import pymysql

DDL_PATHS: Tuple[str] = ("ddl", "array_sort.sql",)

@pytest.fixture(scope = "module", autouse = True)
def install()-> None:
    """Install stored function into test target DB instance."""
    args: str = execute_sql_file(os.path.join(*DDL_PATHS))
    print(f"Executed below:\n{args}")
    yield
    pass

class TestArraySort(BTC):
    @pytest.mark.parametrize(("title", "arr", "expected"), (
        ("""Array.sorted("adfuhjklhag123470987,.a]") -> ??""",
            """adfuhjklhag123470987,.a]""", pymysql.OperationalError),
    ))
    def test_illegal_json_input(self, title: str, arr: Sequence[Any], expected: Exception)-> None:
        cur = self.get_cursor()
        stmt: str = cur.mogrify("SELECT ARRAY_SORT(%(arr)s) AS `expected`;", locals())
        exc: Optional[Exception] = None
        try:
            cur.execute(stmt)
        except Exception as e:
            exc = e
            print(e)
        finally:
            assert isinstance(exc, expected)
    
    @pytest.mark.parametrize(("title", "arr", "expected"), (
        ("""Array.sorted(null) -> null""", dumps(None), None),
        ("""Array.sorted([]) -> []""", dumps([]), dumps([])),
    ))
    def test_null_boundary(self, title: str, arr: Sequence[Any], expected: Sequence[Any])-> None:
        cur = self.get_cursor()
        stmt: str = cur.mogrify("SELECT ARRAY_SORT(%(arr)s) AS `expected`;", locals())
        cur.execute(stmt)
        raw: str = cur.fetchone()['expected']
        assert expected == raw, stmt

    @pytest.mark.parametrize(("title", "arr", "expected"), (
        ("""Array.sorted([5, 3, 2, 1]) -> [1, 2, 3, 5]""",
            dumps([5, 3, 2, 1]), dumps([1, 2, 3, 5])),
        ("""Array.sorted(["F", "a", "d", "0", "f"]) -> ["0", "F", "a", "d", "e", "f"]""",
            dumps(["F", "a", "d", "0", "f"]), dumps(["0", "F", "a", "d", "f"])),
        ("""Array.sorted(["F", "f", "A", "a", 1, 0, null, true, false]) -> [null, 0, 1, "A", "F", "a", "f", false, true]""",
            dumps(["F", "f", "A", "a", 1, 0, None, True, False]), dumps([None, 0, 1, "A", "F", "a", "f", False, True])),
    ))
    def test_simple_element(self, title: str, arr: Sequence[Any], expected: Sequence[Any])-> None:
        cur = self.get_cursor()
        stmt: str = cur.mogrify("SELECT ARRAY_SORT(%(arr)s) AS `expected`;", locals())
        cur.execute(stmt)
        raw: str = cur.fetchone()['expected']
        assert expected == raw, stmt

    @pytest.mark.parametrize(("title", "arr", "expected"), (
        ("""Array.sorted({"a": 1, "b": 2, "c": 3}) -> null""",
            dumps({"a": 1, "b": 2, "c": 3}), None),
        ("""Array.flatten([{"a": 1, "b": 2, "c": 3}, 4, 2, 3]]) -> ??""",
            dumps([{"a": 1, "b": 2, "c": 3}, 4, 2, 3]), dumps([2, 3, 4, {"a": 1, "b": 2, "c": 3}])),
    ))
    def test_complexed_element(self, title: str, arr: Sequence[Any], expected: Sequence[Any])-> None:
        cur = self.get_cursor()
        stmt: str = cur.mogrify("SELECT ARRAY_SORT(%(arr)s) AS `expected`;", locals())
        cur.execute(stmt)
        raw: str = cur.fetchone()['expected']
        assert expected == raw, stmt
