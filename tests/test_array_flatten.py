import os
from json import dumps
from typing import Any, Optional, Sequence, Tuple
from tests.util import BTC, execute_sql_file
import pytest
import pymysql

DDL_PATHS: Tuple[str] = ("ddl", "array_flatten.sql",)

@pytest.fixture(scope = "module", autouse = True)
def install()-> None:
    """Install stored function into test target DB instance."""
    args: str = execute_sql_file(os.path.join(*DDL_PATHS))
    print(f"Executed below:\n{args}")
    yield
    pass

class TestArrayFlatten(BTC):
    @pytest.mark.parametrize(("title", "arr", "expected"), (
        ("""Array.flatten("adfuhjklhag123470987,.a]") -> ??""",
            """adfuhjklhag123470987,.a]""", pymysql.OperationalError),
    ))
    def test_illegal_json_input(self, title: str, arr: Sequence[Any], expected: Exception)-> None:
        cur = self.get_cursor()
        stmt: str = cur.mogrify("SELECT ARRAY_FLATTEN(%(arr)s) AS `expected`;", locals())
        exc: Optional[Exception] = None
        try:
            cur.execute(stmt)
        except Exception as e:
            exc = e
            print(e)
        finally:
            assert isinstance(exc, expected)
    
    @pytest.mark.parametrize(("title", "arr", "expected"), (
        ("""Array.flatten(null) -> null""", dumps(None), None),
        ("""Array.flatten([]) -> []""", dumps([]), dumps([])),
    ))
    def test_null_boundary(self, title: str, arr: Sequence[Any], expected: Sequence[Any])-> None:
        cur = self.get_cursor()
        stmt: str = cur.mogrify("SELECT ARRAY_FLATTEN(%(arr)s) AS `expected`;", locals())
        cur.execute(stmt)
        raw: str = cur.fetchone()['expected']
        assert expected == raw, stmt

    @pytest.mark.parametrize(("title", "arr", "expected"), (
        ("""Array.flatten([[], [1, 2, 3]]) -> [1, 2, 3]""",
            dumps([[], [1, 2, 3]]), dumps([1, 2, 3])),
        ("""Array.flatten([[1, 2, 3], []]) -> [1, 2, 3]""",
            dumps([[1, 2, 3], []]), dumps([1, 2, 3])),
        ("""Array.flatten([[1, 2, 3], [4, 5, 6]]) -> [1, 2, 3, 4, 5, 6]""",
            dumps([[1, 2, 3], [4, 5, 6]]), dumps([1, 2, 3, 4, 5, 6])),
    ))
    def test_simple_element(self, title: str, arr: Sequence[Any], expected: Sequence[Any])-> None:
        cur = self.get_cursor()
        stmt: str = cur.mogrify("SELECT ARRAY_FLATTEN(%(arr)s) AS `expected`;", locals())
        cur.execute(stmt)
        raw: str = cur.fetchone()['expected']
        assert expected == raw, stmt

    @pytest.mark.parametrize(("title", "arr", "expected"), (
        ("""Array.flatten([["a", [1, 2, 3], "b"], [1, 2, 3]]) -> ["a", [1, 2, 3], "b", 1, 2, 3]""",
            dumps([["a", [1, 2, 3], "b"], [1, 2, 3]]), dumps(["a", [1, 2, 3], "b", 1, 2, 3])),
        ("""Array.flatten([["a", {"a":1, "b":2, "c":3}, "b"], [1, 2, 3]]) -> ["a", {"a":1, "b":2, "c":3}, "b", 1, 2, 3]""",
            dumps([["a", {"a":1, "b":2, "c":3}, "b"], [1, 2, 3]]), dumps(["a", {"a":1, "b":2, "c":3}, "b", 1, 2, 3])),
    ))
    def test_hierarchical_element(self, title: str, arr: Sequence[Any], expected: Sequence[Any])-> None:
        cur = self.get_cursor()
        stmt: str = cur.mogrify("SELECT ARRAY_FLATTEN(%(arr)s) AS `expected`;", locals())
        cur.execute(stmt)
        raw: str = cur.fetchone()['expected']
        assert expected == raw, stmt
