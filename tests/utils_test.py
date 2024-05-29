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

import pytest

from ib_fundamental import FundamentalData
from ib_fundamental.utils import to_json

fund_data_methods = (
    _m
    for _m in dir(FundamentalData)
    if (_m[:1] != "_" and _m not in ("client", "parser"))
)


@pytest.fixture(params=fund_data_methods)
def fund_method(fundamental_data, request):
    """JSON fixture, send all FundamentalData methods as json"""
    _m = request.param
    yield fundamental_data, _m


class TestUtils:
    """Tests for utils module"""

    def test_json_inc_annual(self, fund_method):
        """test json"""
        _fund_data, _method = fund_method
        _json = to_json(getattr(_fund_data, _method))
        # assert
        assert isinstance(_json, str)
