import os
from json import dumps
from typing import Any, Optional, Sequence, Tuple
from tests.util import BTC, execute_sql_file
import pytest
import pymysql

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
        ("""Array.join("adfuhjklhag123470987,.a]", null) -> ??""",
            """adfuhjklhag123470987,.a]""", None, pymysql.OperationalError),
    ))
    def test_illegal_json_input(self, title: str, arr: Sequence[Any], separator_chars: str, expected: Exception)-> None:
        cur = self.get_cursor()
        stmt: str = cur.mogrify("SELECT ARRAY_JOIN(%(arr)s, %(separator_chars)s) AS `expected`;", locals())
        exc: Optional[Exception] = None
        try:
            cur.execute(stmt)
        except Exception as e:
            exc = e
            print(e)
        finally:
            assert isinstance(exc, expected)
    
    @pytest.mark.parametrize(("title", "arr", "separator_chars", "expected"), (
        ("""Array.join(null, null) -> null""", dumps(None), None, None),
        ("""Array.join([], null) -> """"", dumps([]), None, ""),
        ("""Array.join(null, "") -> """"", dumps(None), "", None),
        ("""Array.join([], "") -> """"", dumps([]), "", ""),
    ))
    def test_null_boundary(self, title: str, arr: Sequence[Any], separator_chars: str, expected: Sequence[Any])-> None:
        cur = self.get_cursor()
        stmt: str = cur.mogrify("SELECT ARRAY_JOIN(%(arr)s, %(separator_chars)s) AS `expected`;", locals())
        cur.execute(stmt)
        raw: str = cur.fetchone()['expected']
        assert expected == raw, stmt

    @pytest.mark.parametrize(("title", "arr", "separator_chars", "expected"), (
        ("""Array.join(["a", "b", "c", "d"], null) -> "a,b,c,d""""",
            dumps(["a", "b", "c", "d"]), None, "a,b,c,d"),
        ("""Array.join(["a", "b", "c", "d"], ", ") -> "a, b, c, d""""",
            dumps(["a", "b", "c", "d"]), ", ", "a, b, c, d"),
        ("""Array.join(["a", "b", "c", "d"], "") -> "abcd""""",
            dumps(["a", "b", "c", "d"]), "", "abcd"),
        ("""Array.join(["a", "b", "c", "d"], "●") -> "a●b●c●d""""",
            dumps(["a", "b", "c", "d"]), "●", "a●b●c●d"),
        ("""Array.join(["a", "b", null, "c", "d"], null) -> "a,b,null,c,d""""",
            dumps(["a", "b", None, "c", "d"]), None, "a,b,null,c,d"),
        ("""Array.join(["a", "b", true, "c", "d"], null) -> "a,b,true,c,d""""",
            dumps(["a", "b", True, "c", "d"]), None, "a,b,true,c,d"),
        ("""Array.join(["a", "b", false, "c", "d"], null) -> "a,b,false,c,d""""",
            dumps(["a", "b", False, "c", "d"]), None, "a,b,false,c,d"),
    ))
    def test_string(self, title: str, arr: Sequence[Any], separator_chars: str, expected: Sequence[Any])-> None:
        cur = self.get_cursor()
        stmt: str = cur.mogrify("SELECT ARRAY_JOIN(%(arr)s, %(separator_chars)s) AS `expected`;", locals())
        cur.execute(stmt)
        raw: str = cur.fetchone()['expected']
        assert expected == raw, stmt

    @pytest.mark.parametrize(("title", "arr", "separator_chars", "expected"), (
        ("""Array.join([1, 2, 3, 4], null) -> "1,2,3,4""""",
            dumps([1, 2, 3, 4]), None, "1,2,3,4"),
        ("""Array.join([1, 2, 3, 4], ", ") -> "1, 2, 3, 4""""",
            dumps([1, 2, 3, 4]), ", ", "1, 2, 3, 4"),
        ("""Array.join([1, 2, 3, 4], "●") -> "1●2●3●4""""",
            dumps([1, 2, 3, 4]), "●", "1●2●3●4"),
        ("""Array.join([1, 2, 3, 4], "") -> "1234""""",
            dumps([1, 2, 3, 4]), "", "1234"),
        ("""Array.join([1, 2, 3, 4], true) -> "1121314""""",
            dumps([1, 2, 3, 4]), True, "1121314"),
        ("""Array.join([1, 2, 3, 4], false) -> "1020304""""",
            dumps([1, 2, 3, 4]), False, "1020304"),
        ("""Array.join([1, 2, null, 3, 4], null) -> "1,2,null,3,4""""",
            dumps([1, 2, None, 3, 4]), None, "1,2,null,3,4"),
        ("""Array.join([1, 2, true, 3, 4], null) -> "1,2,true,3,4""""",
            dumps([1, 2, True, 3, 4]), None, "1,2,true,3,4"),
        ("""Array.join([1, 2, false, 3, 4], null) -> "1,2,false,3,4""""",
            dumps([1, 2, False, 3, 4]), None, "1,2,false,3,4"),
        ("""Array.join(["a", "b", "c", "d"], 0) -> "a0b0c0d""""",
            dumps(["a", "b", "c", "d"]), dumps(0), "a0b0c0d"),
    ))
    def test_number(self, title: str, arr: Sequence[Any], separator_chars: str, expected: Sequence[Any])-> None:
        cur = self.get_cursor()
        stmt: str = cur.mogrify("SELECT ARRAY_JOIN(%(arr)s, %(separator_chars)s) AS `expected`;", locals())
        cur.execute(stmt)
        raw: str = cur.fetchone()['expected']
        assert expected == raw, stmt
