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

"""Tests for IBClient"""

import os

import pytest
from ib_async import IB, FundamentalRatios

from ib_fundamental.ib_client import IBClient, Stock, Ticker


class TestIBClient:

    def test_instantiation(self, ib_client: IBClient):
        """test IBClient instance"""
        # assert
        assert isinstance(ib_client, IBClient)
        assert isinstance(ib_client.ib, IB)
        assert ib_client.is_connected()

    def test_make_contract(self, ib_client: IBClient):
        """test IBClient.contract is correct"""
        # assert
        assert isinstance(ib_client.contract, Stock)
        assert ib_client.contract.symbol == ib_client.symbol

    def test_ratios(self, ib_client: IBClient):
        """Test FundamentalRatios"""
        # act
        _ratio = ib_client.get_ratios()
        # assert
        assert isinstance(_ratio, FundamentalRatios)

    def test_ticker(self, ib_client: IBClient):
        """Test IBClient.ticker"""
        # arrange
        _ticker = ib_client.get_ticker()
        if _ticker is None:
            while _ticker is None:
                ib_client.ib.sleep(0.0)
        # assert
        assert isinstance(_ticker, Ticker)
        assert _ticker.contract == ib_client.contract

    def test_req_fundamental(self, ib_client: IBClient):
        """Test IBClient.ib_req_fund"""
        # arrange
        _report_type = [
            "ReportsFinStatements",
            "ReportsFinSummary",
            "ReportSnapshot",
            "RESC",
            "ReportsOwnership",
        ]
        _reports = [ib_client.ib_req_fund(_r) for _r in _report_type]
        # assert
        assert len(_reports) == 5
        assert all([isinstance(_r, str) for _r in _reports])

    def test_req_fundamental_error(self, ib_client: IBClient):
        """Test IBClient.ib_req_fund raises ValueError"""
        # arrange
        _report_type = [
            "ReportsFinStatements",
            "ReportsFinSummary",
            "ReportSnapshot",
            "RESC",
            "ReportsOwnership",
            "CalendarReport",
        ]
        with pytest.raises(ValueError) as ex_info:
            _ = [ib_client.ib_req_fund(_r) for _r in _report_type]
        # assert
        assert ex_info.type is ValueError

    def test_is_connected(self, ib_client: IBClient):
        """Test IBClient.is_connected"""
        assert ib_client.is_connected()

    def test_disconnect(self, ib_client: IBClient):
        """Test IBClient.disconnect"""
        # act
        ib_client.disconnect()
        # assert
        assert not ib_client.is_connected()
        # re-connect
        ib_client.ib.connect(
            host=os.getenv("IBFUND_HOST", "localhost"),
            port=int(os.getenv("IBFUND_PORT", "7497")),
            clientId=int(os.getenv("IBFUND_CLI_ID", "120")),
        )
        # assert
        assert ib_client.is_connected()
