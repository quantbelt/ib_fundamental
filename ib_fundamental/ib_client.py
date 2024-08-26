#!/usr/bin/env python3
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

"""
Created on Fri Apr 30 16:21:58 2021

@author: gonzo
"""

__all__ = [
    "IBClient",
]

from ib_async import IB, Dividends, FundamentalRatios, Stock, Ticker

from .objects import ReportType


class IBClient:
    """IB client"""

    ticker: Ticker
    tick_list: str = "258,456"

    # pylint: disable=too-many-arguments
    def __init__(
        self, ib: IB, symbol: str, exchange: str = "SMART", currency: str = "USD"
    ):
        """_summary_

        Args:
            ib (IB): ib async connection
            symbol (str): symbol
            exchange (str, optional): exchange. Defaults to "SMART".
            currency (str, optional): currency. Defaults to "USD".

        Raises:
            ValueError: on invalid symbol, IB not connected
        """
        self.ib = ib
        if symbol:
            self.contract: Stock = self.make_contract(symbol, exchange, currency)
            self.symbol: str = symbol
        else:
            raise ValueError("No symbol defined.")

        if self.ib.isConnected():
            self.host = self.ib.client.host
            self.port = self.ib.client.port
            self.client_id = self.ib.client.clientId
        else:
            raise ValueError("IB is not connected.")

    def __repr__(self):
        cls_name = self.__class__.__qualname__
        return (
            f"{cls_name}(symbol={self.symbol!r},host={self.host!r},"
            f"port={self.port!r},client_id={self.client_id!r},IB={self.ib!r},"
            f"contract={self.contract!r})"
        )

    def __del__(self):
        self.cancel_ticket()

    def __enter__(self):
        return self

    def __exit__(self, *_exc):
        self.cancel_ticket()

    def make_contract(
        self, symbol: str, exchange: str = "SMART", currency: str = "USD"
    ) -> Stock:
        """Stock contract factory method

        Args:
            symbol (str): stock symbol
            exchange (str, optional): exchange. Defaults to "SMART".
            currency (str, optional): currency. Defaults to "USD".

        Returns:
            Contract: Stock contract
        """
        _stock = Stock(symbol=symbol, exchange=exchange, currency=currency)
        self.ib.qualifyContracts(_stock)
        return _stock

    def ib_req_fund(self, report_type: ReportType) -> str:
        """
        reportType:
            - 'ReportsFinSummary': Financial summary
            - 'ReportsOwnership': Company's ownership
            - 'ReportSnapshot': Company's financial overview
            - 'ReportsFinStatements': Financial Statements
            - 'RESC': Analyst Estimates
            - 'CalendarReport': Company's calendar
        """
        xml = self.ib.reqFundamentalData(self.contract, report_type)
        if xml:
            return xml
        raise ValueError(
            f"No response for report {report_type}, contract: {self.contract}"
        )

    def get_ticker(self) -> Ticker:
        """get ticker data"""
        self.ticker = self.ib.reqMktData(
            contract=self.contract,
            genericTickList=self.tick_list,
            snapshot=False,
        )
        return self.ticker

    def get_ratios(self) -> FundamentalRatios:
        """request market data ticker with fundamental ratios"""
        self.get_ticker()
        if self.ticker.fundamentalRatios is None:
            while self.ticker.fundamentalRatios is None:
                self.ib.sleep(0.0)
        return self.ticker.fundamentalRatios

    def get_dividends(self) -> Dividends:
        """get dividend information from ticker"""
        self.get_ticker()
        if self.ticker.dividends is None:
            while self.ticker.dividends is None:
                self.ib.sleep(0.0)
        return self.ticker.dividends

    def cancel_ticket(self) -> None:
        """cancel ticket market data"""
        if not hasattr(self, "ticker"):
            return None
        if self.ticker in self.ib.tickers() and self.is_connected():
            self.ib.cancelMktData(self.contract)
        return None

    def is_connected(self) -> bool:
        """is connected to TWS api"""
        return self.ib.isConnected()

    def disconnect(self) -> None:
        """Disconnect from TWS API"""
        self.ib.disconnect()
