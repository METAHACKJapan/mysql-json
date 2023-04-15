from json import dumps
from typing import Any, Optional, Sequence
from tests.util import BTC
import pymysql
import pytest

class TestArraySlice(BTC):
    __con__: Optional[pymysql.Connection] = None
    DSN_PATH: str = "dsn.json"

    @pytest.mark.parametrize(("title", "arr", "start", "stop", "step", "expected"), (
        ("Array.slice(null) -> null", dumps(None), 0, 1, 1, None),
        ("", dumps([1, 2, 3, 4, 5, 6, 7, 8, 9,]), 0, 1, 1, '[1]'),
        ("", dumps(["1", "2", "3", "4", "5",]), 0, 1, 1, '["1"]'),
        ("", dumps([True, False, None, True, False, None,]), 0, 1, 1, '[true]'),
        ("", dumps([True, False, None, True, False, None,]), 1, 2, 1, '[false]'),
        ("", dumps([True, False, None, True, False, None,]), 2, 3, 1, '[null]'),
        ("", dumps([True, -1, 0.1, "HOGE", None,]), 0, 1, 1, '[true]'),
        ("", dumps([True, -1, 0.1, "HOGE", None,]), 1, 2, 1, '[-1]'),
        ("", dumps([True, -1, 0.1, "HOGE", None,]), 2, 3, 1, '[0.1]'),
        ("", dumps([True, -1, 0.1, "HOGE", None,]), 3, 4, 1, '["HOGE"]'),
        ("", dumps([True, -1, 0.1, "HOGE", None,]), 4, 5, 1, '[null]'),
    ))
    def test_arr(self, title: str, arr: Sequence[Any], start: int, stop: int, step: int, expected: Sequence[Any])-> None:
        if self.__con__ is None:
            self.__con__ = pymysql.connect(**self.dsn)
        cur = self.__con__.cursor(pymysql.cursors.DictCursor)
        stmt: str = cur.mogrify("SELECT ARRAY_SLICE(%(param)s, %(start)s, %(stop)s, %(step)s) AS `expected`;", {
            "param": arr,
            "start": start,
            "stop": stop,
            "step": step
        })
        cur.execute(stmt)
        raw: str = cur.fetchone()['expected']
        assert expected == raw, stmt

    @pytest.mark.parametrize(("title", "arr", "start", "stop", "step", "expected"), (
        ("", dumps([1, 2, 3, 4, 5, 6, 7, 8, 9,]), 0, 3, 1, '[1, 2, 3]'),
        ("", dumps([1, 2, 3, 4, 5, 6, 7, 8, 9,]), 1, 3, 1, '[2, 3]'),
        ("", dumps([1, 2, 3, 4, 5, 6, 7, 8, 9,]), 7, 9, 1, '[8, 9]'),
        ("", dumps([1, 2, 3, 4, 5, 6, 7, 8, 9,]), -1, 3, 1, None),
        ("", dumps([1, 2, 3, 4, 5, 6, 7, 8, 9,]), 0, -3, 1, None),
    ))
    def test_range(self, title: str, arr: Sequence[Any], start: int, stop: int, step: int, expected: Sequence[Any])-> None:
        if self.__con__ is None:
            self.__con__ = pymysql.connect(**self.dsn)
        cur = self.__con__.cursor(pymysql.cursors.DictCursor)
        stmt: str = cur.mogrify("SELECT ARRAY_SLICE(%(param)s, %(start)s, %(stop)s, %(step)s) AS `expected`;", {
            "param": arr,
            "start": start,
            "stop": stop,
            "step": step
        })
        cur.execute(stmt)
        raw: str = cur.fetchone()['expected']
        assert expected == raw, stmt
