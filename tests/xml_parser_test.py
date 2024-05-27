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

"""Test xml_parser module"""

from ib_fundamental.objects import (
    AnalystForecast,
    BalanceSheetStatement,
    CashFlowStatement,
    CompanyInfo,
    Dividend,
    DividendPerShare,
    EarningsPerShare,
    ForwardYear,
    IncomeStatement,
    OwnershipCompany,
    OwnershipDetails,
    OwnershipReport,
    RatioSnapshot,
    Revenue,
    StatementMap,
)
from ib_fundamental.xml_parser import XMLParser


class TestXMLParser:
    """Test XMLParser class"""

    def test_statement_inc_annual(self, xml_parser: XMLParser):
        """Test XMLParser annual income statement"""
        # act
        _xml_parser = xml_parser
        _inc = _xml_parser.get_fin_statement(statement="INC")
        # assert
        assert isinstance(_inc, list)
        assert len(_inc) > 1
        assert isinstance(_inc[0], IncomeStatement)
        assert _inc[0].period == "Annual"

    def test_statement_inc_quarter(self, xml_parser: XMLParser):
        """Test XMLParser quarter income statement"""
        # act
        _xml_parser = xml_parser
        _inc = _xml_parser.get_fin_statement(statement="INC", period="quarter")
        # assert
        assert isinstance(_inc, list)
        assert len(_inc) > 1
        assert isinstance(_inc[0], IncomeStatement)
        assert _inc[0].period == "Interim"

    def test_statement_bal_annual(self, xml_parser: XMLParser):
        """Test XMLParser annual balance sheet"""
        # act
        _xml_parser = xml_parser
        _inc = _xml_parser.get_fin_statement(statement="BAL")
        # assert
        assert isinstance(_inc, list)
        assert len(_inc) > 1
        assert isinstance(_inc[0], BalanceSheetStatement)
        assert _inc[0].period == "Annual"

    def test_statement_bal_quarter(self, xml_parser: XMLParser):
        """Test XMLParser balance sheet quarter"""
        # act
        _xml_parser = xml_parser
        _inc = _xml_parser.get_fin_statement(statement="BAL", period="quarter")
        # assert
        assert isinstance(_inc, list)
        assert len(_inc) > 1
        assert isinstance(_inc[0], BalanceSheetStatement)
        assert _inc[0].period == "Interim"

    def test_statement_cas_annual(self, xml_parser: XMLParser):
        """Test XMLParser annual cashflow"""
        # act
        _xml_parser = xml_parser
        _inc = _xml_parser.get_fin_statement(statement="CAS")
        # assert
        assert isinstance(_inc, list)
        assert len(_inc) > 1
        assert isinstance(_inc[0], CashFlowStatement)
        assert _inc[0].period == "Annual"

    def test_statement_cas_quarter(self, xml_parser: XMLParser):
        """Test XMLParser cashflow quarter"""
        # act
        _xml_parser = xml_parser
        _inc = _xml_parser.get_fin_statement(statement="CAS", period="quarter")
        # assert
        assert isinstance(_inc, list)
        assert len(_inc) > 1
        assert isinstance(_inc[0], CashFlowStatement)
        assert _inc[0].period == "Interim"

    def test_map_items_bal(self, xml_parser: XMLParser):
        """Test XMLParser map_items balance sheet"""
        # act
        _xml_parser = xml_parser
        _statement = "BAL"
        _map_items = _xml_parser.get_map_items(statement=_statement)
        # assert
        assert isinstance(_map_items, list)
        assert len(_map_items) > 1
        assert isinstance(_map_items[0], StatementMap)
        assert _map_items[0].statement_type == _statement

    def test_map_items_cas(self, xml_parser: XMLParser):
        """Test XMLParser map_items cashflow"""
        # act
        _xml_parser = xml_parser
        _statement = "CAS"
        _map_items = _xml_parser.get_map_items(statement=_statement)
        # assert
        assert isinstance(_map_items, list)
        assert len(_map_items) > 1
        assert isinstance(_map_items[0], StatementMap)
        assert _map_items[0].statement_type == _statement

    def test_map_items_inc(self, xml_parser: XMLParser):
        """Test XMLParser map_items income"""
        # act
        _xml_parser = xml_parser
        _statement = "INC"
        _map_items = _xml_parser.get_map_items(statement=_statement)
        # assert
        assert isinstance(_map_items, list)
        assert len(_map_items) > 1
        assert isinstance(_map_items[0], StatementMap)
        assert _map_items[0].statement_type == _statement

    def test_ownership(self, xml_parser: XMLParser):
        """Test XMLParser ownership report"""
        # act
        _xml_parser = xml_parser
        _own = _xml_parser.get_ownership_report()
        # assert
        assert isinstance(_own, OwnershipReport)
        assert isinstance(_own.company, OwnershipCompany)
        assert isinstance(_own.ownership_details, list)
        assert len(_own.ownership_details) > 1
        assert isinstance(_own.ownership_details[0], OwnershipDetails)

    def test_dividen(self, xml_parser: XMLParser):
        """Test XMLParser dividends"""
        # act
        _xml_parser = xml_parser
        _div = _xml_parser.get_dividend()
        # assert
        assert isinstance(_div, list)
        assert len(_div) > 1
        assert isinstance(_div[0], Dividend)
        assert _div[0].currency == "USD"

    def test_div_per_share_ttm(self, xml_parser: XMLParser):
        """Test XMLparser div per share TTM"""
        # act
        _xml_parser = xml_parser
        _divps = _xml_parser.get_div_per_share(report_type="TTM")
        # assert
        assert isinstance(_divps, list)
        assert len(_divps) > 1
        assert isinstance(_divps[0], DividendPerShare)
        assert _divps[0].report_type == "TTM"
        assert _divps[0].period == "12M"
        assert _divps[0].currency == "USD"

    def test_div_per_share_q(self, xml_parser: XMLParser):
        """Test XMLparser div per share quarter"""
        # act
        _xml_parser = xml_parser
        _divps = _xml_parser.get_div_per_share(report_type="R", period="3M")
        # assert
        assert isinstance(_divps, list)
        assert len(_divps) > 1
        assert isinstance(_divps[0], DividendPerShare)
        assert _divps[0].report_type == "R"
        assert _divps[0].period == "3M"
        assert _divps[0].currency == "USD"

    def test_revenue_ttm(self, xml_parser: XMLParser):
        """Test XMLparser revenue ttm"""
        # act
        _xml_parser = xml_parser
        _rev = _xml_parser.get_revenue(report_type="TTM")
        # assert
        assert isinstance(_rev, list)
        assert len(_rev) > 1
        assert isinstance(_rev[0], Revenue)
        assert _rev[0].report_type == "TTM"
        assert _rev[0].period == "12M"

    def test_revenue_q(self, xml_parser: XMLParser):
        """Test XMLparser revenue quarter"""
        # act
        _xml_parser = xml_parser
        _rev = _xml_parser.get_revenue(report_type="R", period="3M")
        # assert
        assert isinstance(_rev, list)
        assert len(_rev) > 1
        assert isinstance(_rev[0], Revenue)
        assert _rev[0].report_type == "R"
        assert _rev[0].period == "3M"

    def test_eps_ttm(self, xml_parser: XMLParser):
        """Test XMLparser eps ttm"""
        # act
        _xml_parser = xml_parser
        _eps = _xml_parser.get_eps(report_type="TTM")
        # assert
        assert isinstance(_eps, list)
        assert len(_eps) > 1
        assert isinstance(_eps[0], EarningsPerShare)
        assert _eps[0].report_type == "TTM"
        assert _eps[0].period == "12M"

    def test_eps_q(self, xml_parser: XMLParser):
        """Test XMLparser eps quarter"""
        # act
        _xml_parser = xml_parser
        _eps = _xml_parser.get_eps(report_type="R", period="3M")
        # assert
        assert isinstance(_eps, list)
        assert len(_eps) > 1
        assert isinstance(_eps[0], EarningsPerShare)
        assert _eps[0].report_type == "R"
        assert _eps[0].period == "3M"

    def test_analyst_forecast(self, xml_parser: XMLParser):
        """Test XMLParser analyst forecast"""
        # act
        _xml_parser = xml_parser
        _analyst = _xml_parser.get_analyst_forecast()
        # assert
        assert isinstance(_analyst, AnalystForecast)
        assert hasattr(_analyst, "target_price")
        assert isinstance(_analyst.target_price, float)
        assert hasattr(_analyst, "proj_eps")
        assert isinstance(_analyst.proj_eps, float)

    def test_ratios(self, xml_parser: XMLParser):
        """Test XMLParser ratios"""
        # act
        _xml_parser = xml_parser
        _ratios = _xml_parser.get_ratios()
        # assert
        assert isinstance(_ratios, RatioSnapshot)
        assert hasattr(_ratios, "ttmrev")

    def test_fy_estimates(self, xml_parser: XMLParser):
        """Test XMLParser fy estimates"""
        # act
        _xml_parser = xml_parser
        _estimates = _xml_parser.get_fy_estimates()
        # assert
        assert isinstance(_estimates, list)
        assert len(_estimates) > 1
        assert isinstance(_estimates[0], ForwardYear)

    def test_fy_actuals(self, xml_parser: XMLParser):
        """Test XMLParser fy actuals"""
        # act
        _xml_parser = xml_parser
        _actuals = _xml_parser.get_fy_actuals()
        # assert
        assert isinstance(_actuals, list)
        assert len(_actuals) > 1
        assert isinstance(_actuals[0], ForwardYear)

    def test_company_info(self, xml_parser: XMLParser):
        """Test XMLParser company info"""
        # act
        _xml_parser = xml_parser
        _info = _xml_parser.get_company_info()
        # assert
        assert isinstance(_info, CompanyInfo)
        assert _info.ticker == _xml_parser.xml_report.client.symbol
