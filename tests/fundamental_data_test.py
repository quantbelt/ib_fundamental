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

"""Test fundamental FundamentalData module"""
import pytest
from ib_async import Dividends, FundamentalRatios, Ticker

from ib_fundamental.fundamental import FundamentalData
from ib_fundamental.objects import (
    AnalystForecast,
    CompanyInfo,
    Dividend,
    ForwardYear,
    OwnershipCompany,
    OwnershipDetails,
    OwnershipReport,
    RatioSnapshot,
)


class TestFundamentalData:
    """Test FundamentalData class"""

    def test_statments(self, fundamental_statement):
        """Test FundamentalData statements, income, cashflow, balance sheet
        by period, Annual and Interim
        """
        _statement, _class, _period = fundamental_statement
        # assert
        assert isinstance(_statement, list)
        assert len(_statement) > 1
        assert isinstance(_statement[0], _class)
        assert _statement[0].period == _period

    def test_ownership(self, fundamental_data: FundamentalData):
        """Test FundamentalData ownership report"""
        # act
        _fund_data = fundamental_data
        _own = _fund_data.ownership_report
        # assert
        assert isinstance(_own, OwnershipReport)
        assert isinstance(_own.company, OwnershipCompany)
        assert isinstance(_own.ownership_details, list)
        assert len(_own.ownership_details) > 1
        assert isinstance(_own.ownership_details[0], OwnershipDetails)

    @pytest.mark.xfail(reason="Non dividend paying companies will fail")
    def test_dividend(self, fundamental_data: FundamentalData):
        """Test FundamentalData dividends"""
        # act
        _fund_data = fundamental_data
        _div = _fund_data.dividend
        # assert
        assert isinstance(_div, list)
        assert len(_div) > 1
        assert isinstance(_div[0], Dividend)
        assert _div[0].currency == "USD"

    def test_dividend_summary(self, fundamental_data: FundamentalData):
        """Test FundamentalData dividend summary"""
        # act
        _fund_data = fundamental_data
        _div_summary = _fund_data.dividend_summary
        # assert
        assert isinstance(_div_summary, Dividends)

    @pytest.mark.xfail(reason="Non dividend paying companies will fail")
    def test_financials(self, fundamental_financials):
        """Test FundamentalData financials, dividends per share, revenue,eps"""
        _fin, _class, _report_type, _period_type = fundamental_financials
        # assert
        assert isinstance(_fin, list)
        assert len(_fin) > 1
        assert isinstance(_fin[0], _class)
        assert _fin[0].report_type == _report_type
        assert _fin[0].period == _period_type
        assert _fin[0].currency == "USD"

    def test_analyst_forecast(self, fundamental_data: FundamentalData):
        """Test FundamentalData analyst forecast"""
        # act
        _fund_data = fundamental_data
        _analyst = _fund_data.analyst_forecast
        # assert
        assert isinstance(_analyst, AnalystForecast)
        assert hasattr(_analyst, "target_price")
        assert isinstance(_analyst.target_price, float)
        assert hasattr(_analyst, "proj_eps")
        assert isinstance(_analyst.proj_eps, float)

    def test_ratios(self, fundamental_data: FundamentalData):
        """Test FundamentalData ratios"""
        # act
        _fund_data = fundamental_data
        _ratios = _fund_data.ratios
        # assert
        assert isinstance(_ratios, RatioSnapshot)
        assert hasattr(_ratios, "ttmrev")

    def test_fundamental_rations(self, fundamental_data: FundamentalData):
        """Test FundamentalData fundamental ratios"""
        # act
        _fund_data = fundamental_data
        _f_ratios = _fund_data.fundamental_ratios
        # assert
        assert isinstance(_f_ratios, FundamentalRatios)
        assert hasattr(_fund_data, "ticker")
        assert isinstance(_fund_data.ticker, Ticker)

    def test_forward_year(self, fundamental_fy):
        """Test FundamentalData fy estimates and actuals"""
        _fy = fundamental_fy
        # assert
        assert isinstance(_fy, list)
        assert len(_fy) > 1
        assert isinstance(_fy[0], ForwardYear)

    def test_company_info(self, fundamental_data: FundamentalData):
        """Test FundamentalData company info"""
        # act
        _fund_data = fundamental_data
        _info = _fund_data.company_info
        # assert
        assert isinstance(_info, CompanyInfo)
        assert _info.ticker == _fund_data.parser.xml_report.client.symbol
