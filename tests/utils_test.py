# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""Tests for ib_fundamental utils"""

import json

import pytest

from ib_fundamental.utils import to_json


@pytest.fixture
def fund_method(fundamental_data):
    """JSON fixture, send all FundamentalData methods as json"""
    #
    _methods = [
        _m
        for _m in dir(fundamental_data)
        if (_m[:1] != "_" and _m not in ("client", "parser"))
    ]
    yield from _methods


class TestUtils:
    """Tests for utils module"""

    def test_json_inc_annual(self, fund_method):
        """test json"""
        _json = to_json(fund_method)
        _data = json.loads(_json)
        # assert
        assert isinstance(_json, str)
        assert isinstance(_data, (list, dict))
