import os
from json import dumps
from typing import Any, Optional, Sequence, Tuple
from tests.util import BTC, execute_sql_file
import pytest
import pymysql

DDL_PATHS: Tuple[str] = ("ddl", "array_reverse.sql",)

@pytest.fixture(scope = "module", autouse = True)
def install()-> None:
    """Install stored function into test target DB instance."""
    args: str = execute_sql_file(os.path.join(*DDL_PATHS))
    print(f"Executed below:\n{args}")
    yield
    pass

class TestArrayReverse(BTC):
    @pytest.mark.parametrize(("title", "arr", "expected"), (
        ("""Array.reversed("adfuhjklhag123470987,.a]") -> ??""",
            """adfuhjklhag123470987,.a]""", pymysql.OperationalError),
    ))
    def test_illegal_json_input(self, title: str, arr: Sequence[Any], expected: Exception)-> None:
        cur = self.get_cursor()
        stmt: str = cur.mogrify("SELECT ARRAY_REVERSE(%(arr)s) AS `expected`;", locals())
        exc: Optional[Exception] = None
        try:
            cur.execute(stmt)
        except Exception as e:
            exc = e
            print(e)
        finally:
            assert isinstance(exc, expected)
    
    @pytest.mark.parametrize(("title", "arr", "expected"), (
        ("""Array.reversed(null) -> null""", dumps(None), None),
        ("""Array.reversed([null]) -> [null]""", dumps([None]), dumps([None])),
    ))
    def test_null_boundary(self, title: str, arr: Sequence[Any], expected: Sequence[Any])-> None:
        cur = self.get_cursor()
        stmt: str = cur.mogrify("SELECT ARRAY_REVERSE(%(arr)s) AS `expected`;", locals())
        cur.execute(stmt)
        raw: str = cur.fetchone()['expected']
        assert expected == raw, stmt

    @pytest.mark.parametrize(("title", "arr", "expected"), (
        ("""Array.reversed([5, 3, 2, 1]) -> [1, 2, 3, 5]""",
            dumps([5, 3, 2, 1]), dumps([1, 2, 3, 5])),
        ("""Array.reversed(["a", 2, true, false, 3]) -> [3, false, true, 2, "a"]""",
            dumps(["a", 2, True, False, 3]), dumps([3, False, True, 2, "a"])),
    ))
    def test_simple_element(self, title: str, arr: Sequence[Any], expected: Sequence[Any])-> None:
        cur = self.get_cursor()
        stmt: str = cur.mogrify("SELECT ARRAY_REVERSE(%(arr)s) AS `expected`;", locals())
        cur.execute(stmt)
        raw: str = cur.fetchone()['expected']
        assert expected == raw, stmt
