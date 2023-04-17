import os
from json import dumps
from typing import Any, Optional, Sequence, Tuple
from tests.util import BTC, execute_sql_file
import pytest
import pymysql

DDL_PATHS: Tuple[str] = ("ddl", "array_unique.sql",)

@pytest.fixture(scope = "module", autouse = True)
def install()-> None:
    """Install stored function into test target DB instance."""
    args: str = execute_sql_file(os.path.join(*DDL_PATHS))
    print(f"Executed below:\n{args}")
    yield
    pass

class TestArrayUnique(BTC):
    @pytest.mark.parametrize(("title", "arr", "expected"), (
        ("""Array.unique("adfuhjklhag123470987,.a]") -> ??""",
            """adfuhjklhag123470987,.a]""", pymysql.OperationalError),
    ))
    def test_illegal_json_input(self, title: str, arr: Sequence[Any], expected: Exception)-> None:
        cur = self.get_cursor()
        stmt: str = cur.mogrify("SELECT ARRAY_UNIQUE(%(arr)s) AS `expected`;", locals())
        exc: Optional[Exception] = None
        try:
            cur.execute(stmt)
        except Exception as e:
            exc = e
            print(e)
        finally:
            assert isinstance(exc, expected)
    
    @pytest.mark.parametrize(("title", "arr", "expected"), (
        ("""Array.unique(null) -> null""", dumps(None), None),
        ("""Array.unique([]) -> []""", dumps([]), dumps([])),
    ))
    def test_null_boundary(self, title: str, arr: Sequence[Any], expected: Sequence[Any])-> None:
        cur = self.get_cursor()
        stmt: str = cur.mogrify("SELECT ARRAY_UNIQUE(%(arr)s) AS `expected`;", locals())
        cur.execute(stmt)
        raw: str = cur.fetchone()['expected']
        assert expected == raw, stmt

    @pytest.mark.parametrize(("title", "arr", "expected"), (
        ("""Array.unique(["f", "D", "D", "d", "b", "a", "0"]) -> ["0", "a", "b", "d", "D", "f"]""",
            dumps(["f", "D", "D", "d", "b", "a", "0"]), dumps(["0", "D", "a", "b", "d", "f"])),
        ("""Array.unique(["f", "D", "D", "d", "b", "a", "D"]) -> ["D", "a", "b", "d", "f"]""",
            dumps(["f", "D", "D", "d", "b", "a", "D"]), dumps(["D", "a", "b", "d", "f"])),
    ))
    def test_string(self, title: str, arr: Sequence[Any], expected: Sequence[Any])-> None:
        cur = self.get_cursor()
        stmt: str = cur.mogrify("SELECT ARRAY_UNIQUE(%(arr)s) AS `expected`;", locals())
        cur.execute(stmt)
        raw: str = cur.fetchone()['expected']
        assert expected == raw, stmt

    @pytest.mark.parametrize(("title", "arr", "expected"), (
        ("""Array.unique([0, 1, 2, 2, 3, 3, 3, 4, 4, 4, 4]) -> [0, 1, 2, 3, 4]""",
            dumps([0, 1, 2, 2, 3, 3, 3, 4, 4, 4, 4]), dumps([0, 1, 2, 3, 4])),
        ("""Array.unique([3, 5, 2, 4, 0.1, 0.3, 5, 2]) -> [0.1, 0.3, 2, 3, 4, 5]""",
            dumps([3, 5, 2, 4, 0.1, 0.3, 5, 2]), dumps([0.1, 0.3, 2, 3, 4, 5])),
    ))
    def test_number(self, title: str, arr: Sequence[Any], expected: Sequence[Any])-> None:
        cur = self.get_cursor()
        stmt: str = cur.mogrify("SELECT ARRAY_UNIQUE(%(arr)s) AS `expected`;", locals())
        cur.execute(stmt)
        raw: str = cur.fetchone()['expected']
        assert expected == raw, stmt

    @pytest.mark.parametrize(("title", "arr", "expected"), (
        ("""Array.unique([0, true, false, null, false, 3, "5", null, false, true]) -> [null, 0, 3, "5", false, true]""",
            dumps([0, True, False, None, False, 3, "5", None, False, True]), dumps([None, 0, 3, "5", False, True])),
    ))
    def test_mixtured_types(self, title: str, arr: Sequence[Any], expected: Sequence[Any])-> None:
        cur = self.get_cursor()
        stmt: str = cur.mogrify("SELECT ARRAY_UNIQUE(%(arr)s) AS `expected`;", locals())
        cur.execute(stmt)
        raw: str = cur.fetchone()['expected']
        assert expected == raw, stmt
