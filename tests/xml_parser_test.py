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

import pytest

from ib_fundamental.objects import (
    AnalystForecast,
    CompanyInfo,
    Dividend,
    ForwardYear,
    OwnershipCompany,
    OwnershipDetails,
    OwnershipReport,
    RatioSnapshot,
    StatementMap,
)
from ib_fundamental.xml_parser import XMLParser


class TestXMLParser:
    """Test XMLParser class"""

    def test_statement(self, xml_parser_statement):
        """Test XML Parser statements"""
        _parser_statement, _statement, _period = xml_parser_statement
        print(_parser_statement, _statement, _period)
        # assert
        assert isinstance(_parser_statement, list)
        assert len(_parser_statement) > 1
        assert isinstance(_parser_statement[0], _statement)
        assert _parser_statement[0].period == _period

    def test_map_items(self, xml_parser_map_items):
        """Test XML Parser map_items"""
        _map_items, _statement = xml_parser_map_items
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

    @pytest.mark.xfail(reason="Non dividend paying companies will fail")
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

    @pytest.mark.xfail(reason="Non dividend paying companies will fail")
    def test_financials(self, xml_parser_financials):
        """Test XMLParser div ps, revenue, eps"""
        # act
        _financials, _fin, _report_type, _period_type = xml_parser_financials
        # assert
        assert isinstance(_fin, list)
        assert len(_fin) > 1
        assert isinstance(_fin[0], _financials)
        assert _fin[0].report_type == _report_type
        assert _fin[0].period == _period_type
        assert _fin[0].currency == "USD"

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

    def test_forward_year(self, xml_parser_fy):
        """Test XMLParser fy estimates & actuals"""
        _fy = xml_parser_fy
        # assert
        assert isinstance(_fy, list)
        assert len(_fy) > 1
        assert isinstance(_fy[0], ForwardYear)

    def test_company_info(self, xml_parser: XMLParser):
        """Test XMLParser company info"""
        # act
        _xml_parser = xml_parser
        _info = _xml_parser.get_company_info()
        # assert
        assert isinstance(_info, CompanyInfo)
        assert _info.ticker == _xml_parser.xml_report.client.symbol
