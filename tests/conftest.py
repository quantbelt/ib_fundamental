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

import pytest
from ib_async import IB

from ib_fundamental.fundamental import FundamentalData
from ib_fundamental.ib_client import IBClient
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


@pytest.fixture(scope="class")
def xml_report(ib_client):
    """XMLReport fixture"""
    _ib_client = ib_client
    _xml_report = XMLReport(_ib_client)
    yield _xml_report
    del _xml_report


@pytest.fixture(scope="function")
def xml_parser(ib_client):
    """XMLReport fixture"""
    _ib_client = ib_client
    _xml_parser = XMLParser(ib_client=_ib_client)
    yield _xml_parser
    del _xml_parser


@pytest.fixture(scope="class", params=DJIA)
def fundamental_data(tws_client, request):
    """FundamentalData fixture"""
    _tws_client = tws_client
    _symbol = request.param
    _fund = FundamentalData(symbol=_symbol, ib=_tws_client)
    yield _fund
    del _fund
