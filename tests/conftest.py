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

"""IB Fundamental test fixtures"""

import os
from itertools import chain, product, repeat

import pytest
from ib_async import IB

from ib_fundamental.fundamental import FundamentalData
from ib_fundamental.ib_client import IBClient
from ib_fundamental.objects import (
    BalanceSheetStatement,
    CashFlowStatement,
    DividendPerShare,
    EarningsPerShare,
    IncomeStatement,
    Revenue,
)
from ib_fundamental.xml_parser import XMLParser
from ib_fundamental.xml_report import XMLReport

DJIA = [
    "MMM",
    "AXP",
    "AMGN",
    "AMZN",
    "AAPL",
    "BA",
    "CAT",
    "CVX",
    "CSCO",
    "KO",
    "DIS",
    "DOW",
    "GS",
    "HD",
    "HON",
    "IBM",
    "INTC",
    "JNJ",
    "JPM",
    "MCD",
    "MRK",
    "MSFT",
    "NKE",
    "PG",
    "CRM",
    "TRV",
    "UNH",
    "VZ",
    "V",
    "WMT",
]

# all but calendar
xml_report_attributes = [
    "fin_statements",
    "fin_summary",
    "ownership",
    "resc",
    "snapshot",
]

statement = [CashFlowStatement, BalanceSheetStatement, IncomeStatement]
stament_period = ["Annual", "Interim"]
statement_period_type = ["annual", "quarter"]

financials = [DividendPerShare, Revenue, EarningsPerShare]
fin_attrs_parser = ["get_div_per_share", "get_revenue", "get_eps"]
statement_attrs_fun_data = [
    "cashflow_annual",
    "cashflow_quarter",
    "balance_annual",
    "balance_quarter",
    "income_annual",
    "income_quarter",
]
fin_attrs_fun = [
    "div_ps_ttm",
    "div_ps_q",
    "revenue_ttm",
    "revenue_q",
    "eps_ttm",
    "eps_q",
]

report_type = ["TTM", "R"]
period_type = ["12M", "3M"]
forward_year_attrs = ["fy_estimates", "fy_actuals"]
forward_year_parser_attrs = ["get_fy_estimates", "get_fy_actuals"]

req_report_type = [
    "ReportsFinStatements",
    "ReportsFinSummary",
    "ReportSnapshot",
    "RESC",
    "ReportsOwnership",
    # "CalendarReport", # test for failure
]

map_items_statement_type = ["CAS", "BAL", "INC"]


def repeat_each(iterable, n=2):
    """Repeat each element in *iterable* *n* times.

    >>> list(repeat_each('ABC', 3))
    ['A', 'A', 'A', 'B', 'B', 'B', 'C', 'C', 'C']
    """
    return chain.from_iterable(map(repeat, iterable, repeat(n)))


def ncycles(iterable, n):
    """Returns the sequence elements *n* times

    >>> list(ncycles(["a", "b"], 3))
    ['a', 'b', 'a', 'b', 'a', 'b']

    """
    return chain.from_iterable(repeat(tuple(iterable), n))


@pytest.fixture(scope="session")
def tws_client():
    """tws client fixture"""
    _ib = IB()
    _ib.connect(
        host=os.getenv("IBFUND_HOST", "localhost"),
        port=int(os.getenv("IBFUND_PORT", "7497")),
        clientId=int(os.getenv("IBFUND_CLI_ID", "120")),
    )
    yield _ib
    _ib.disconnect()


@pytest.fixture(scope="module", params=DJIA)
def ib_client(tws_client, request):
    """IBClient fixture"""
    _symbol = request.param
    _ib_client = IBClient(symbol=_symbol, ib=tws_client)
    yield _ib_client
    del _ib_client


@pytest.fixture(scope="function", params=req_report_type)
def ib_client_req_fund(ib_client, request):
    """IBClient ib_req_fund combinations"""
    _report = request.param
    yield ib_client.ib_req_fund(_report)


@pytest.fixture(scope="class")
def xml_report(ib_client):
    """XMLReport fixture"""
    _ib_client = ib_client
    _xml_report = XMLReport(_ib_client)
    yield _xml_report
    del _xml_report


@pytest.fixture(scope="function", params=xml_report_attributes)
def xml_report_attrs(xml_report, request):
    """XMLReport get attributes"""
    _attr = request.param
    yield getattr(xml_report, _attr)


@pytest.fixture(scope="function")
def xml_parser(ib_client):
    """XMLReport fixture"""
    _ib_client = ib_client
    _xml_parser = XMLParser(ib_client=_ib_client)
    yield _xml_parser
    del _xml_parser


gen_parser_statement = (
    (*_m, *_p)
    for _m in zip(map_items_statement_type, statement)
    for _p in zip(stament_period, statement_period_type)
)


@pytest.fixture(scope="function", params=gen_parser_statement)
def xml_parser_statement(xml_parser, request):
    """XMLParser statement combinations"""
    _statement_type, _statement, _stament_period, _statement_period_type = request.param
    _parser_statement = xml_parser.get_fin_statement(
        _statement_type, _statement_period_type
    )
    yield _parser_statement, _statement, _stament_period


@pytest.fixture(scope="function", params=map_items_statement_type)
def xml_parser_map_items(xml_parser, request):
    """XMLParser map_items statement type combinations"""
    _statement_type = request.param
    _map_items = xml_parser.get_map_items(_statement_type)
    yield _map_items, _statement_type


gen_parser_fin = (
    (*_f, *_t)
    for _f in zip(financials, fin_attrs_parser)
    for _t in zip(report_type, period_type)
)


@pytest.fixture(scope="function", params=gen_parser_fin)
def xml_parser_financials(xml_parser, request):
    """XMLParser div ps, rev, eps combinations"""
    _financials, _fin_attrs_parser, _report_type, _period_type = request.param
    _fin = getattr(xml_parser, _fin_attrs_parser)(_report_type, _period_type)
    yield _financials, _fin, _report_type, _period_type


@pytest.fixture(scope="function", params=forward_year_parser_attrs)
def xml_parser_fy(xml_parser, request):
    """XMLParser fy estimates and actuals"""
    _attr = request.param
    _fy = getattr(xml_parser, _attr)()
    yield _fy


@pytest.fixture(scope="class", params=DJIA)
def fundamental_data(tws_client, request):
    """FundamentalData fixture"""
    _tws_client = tws_client
    _symbol = request.param
    _fund = FundamentalData(symbol=_symbol, ib=_tws_client)
    yield _fund
    del _fund


gen_fund_statement = (
    (a, *b)
    for a, b in zip(statement_attrs_fun_data, product(statement, stament_period))
)


@pytest.fixture(scope="function", params=gen_fund_statement)
def fundamental_statement(fundamental_data, request):
    """FundamentalData statements"""
    _attr, _class, _period = request.param
    _statement = getattr(fundamental_data, _attr)
    yield _statement, _class, _period


gen_financials = (
    (_class, _attr, *_t)
    for _class, _attr, _t in zip(
        repeat_each(financials, 2),
        fin_attrs_fun,
        ncycles(zip(report_type, period_type), 3),
    )
)


@pytest.fixture(scope="function", params=gen_financials)
def fundamental_financials(fundamental_data, request):
    """FundamentalData financials"""
    _class, _attr, _report_type, _period_type = request.param
    yield getattr(fundamental_data, _attr), _class, _report_type, _period_type


@pytest.fixture(scope="function", params=forward_year_attrs)
def fundamental_fy(fundamental_data, request):
    """FundamentalData fy estimates and actuals"""
    _attr = request.param
    _fy = getattr(fundamental_data, _attr)
    yield _fy
