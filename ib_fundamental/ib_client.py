#!/usr/bin/env python3
"""
Created on Fri Apr 30 16:21:58 2021

@author: gonzo
"""

__all__ = [
    "IBClient",
]

from typing import Optional

from ib_async import IB, FundamentalRatios, Stock

from .objects import ReportType


class IBClient:
    """IB client"""

    def __init__(
        self,
        symbol: str,
        host: str = "localhost",
        port: int = 7497,
        client_id=111,
        ib: Optional[IB] = None,
    ):

        if symbol:
            self.contract: Stock = self.make_contract(symbol)
            self.symbol: str = symbol
        else:
            raise ValueError("No symbol defined.")
        if ib is not None:
            self.ib: IB = ib
        else:
            self.ib = IB()

        if self.ib.isConnected():
            self.host = self.ib.client.host
            self.port = self.ib.client.port
            self.client_id = self.ib.client.clientId
        else:
            self.host = host
            self.port = port
            self.client_id = client_id
            self.ib.connect(host, port, client_id)

    def __repr__(self):
        cls_name = self.__class__.__qualname__
        return (
            f"{cls_name}(symbol={self.symbol!r},host={self.host!r},"
            f"port={self.port!r},client_id={self.client_id!r},IB={self.ib!r},"
            f"contract={self.contract!r})"
        )

    def __del__(self):
        self.disconnect()

    def __enter__(self):
        return self

    def __exit__(self, *_exc):
        self.disconnect()

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
        return Stock(symbol=symbol, exchange=exchange, currency=currency)

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

    def get_ratios(self) -> FundamentalRatios:
        """request market data ticker with fundamental ratios"""
        self.ticker = self.ib.reqMktData(
            contract=self.contract,
            genericTickList="258",  # fundamentalRatios
            snapshot=False,
        )
        if self.ticker.fundamentalRatios is None:
            while self.ticker.fundamentalRatios is None:
                self.ib.sleep(0.0)
        return self.ticker.fundamentalRatios

    def cancel_ticket(self) -> None:
        """cancel ticket market data"""
        self.ib.cancelMktData(self.contract)

    def is_connected(self) -> bool:
        """is connected to TWS api"""
        return self.ib.isConnected()

    def disconnect(self) -> None:
        """Disconnect from TWS API"""
        self.ib.disconnect()
