#!/usr/bin/env python3
"""
Created on Fri Apr 30 16:21:58 2021

@author: gonzo
"""
# pylint: disable=attribute-defined-outside-init
# pylint: disable=missing-function-docstring

__all__ = [
    "CompanyFundamental",
]

from datetime import datetime
from typing import Optional

from ib_async import IB, FundamentalRatios, Stock, Ticker

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
    OwnershipReport,
    RatioSnapshot,
    Revenue,
)

from .ib_client import IBClient
from .xml_parser import XMLParser

fromisoformat = datetime.fromisoformat


class CompanyFundamental:
    """Company fundamental data"""

    # pylint: disable=too-many-arguments,too-many-public-methods
    # pylint: disable=too-many-instance-attributes
    def __init__(self, symbol: str, ib: IB) -> None:
        """Args:
        symbol (str): Company symbol/ticker
        host (str, optional): TWS API hostname. Defaults to "localhost".
        port (int, optional): Defaults to 7497. 4001/7496 live, 4002/7497 paper
        client_id (int, optional): TWS API client id. Defaults to 111.
        ib (Optional[IB], optional): IB instance. Defaults to None.
        """
        self.client = IBClient(symbol=symbol, ib=ib)
        self.symbol = symbol
        self.contract: Stock = self.client.contract
        self.ticker: Optional[Ticker] = None
        self.parser = XMLParser(ib_client=self.client)

    def __repr__(self):
        cls_name = self.__class__.__qualname__
        return (
            f"{cls_name}(symbol={self.symbol!r},host={self.client.host!r},"
            f"port={self.client.port!r},client_id={self.client.client_id!r},"
            f"IB={self.client.ib!r},contract={self.contract!r})"
        )

    def __del__(self):
        self.client.disconnect()

    def __enter__(self):
        return self

    def __exit__(self, *_exc):
        self.client.disconnect()

    @property
    def income_annual(self) -> list[IncomeStatement]:
        """
        income_annual
        """
        try:
            return self.__income_annual
        except AttributeError:
            self.__income_annual = self.parser.get_fin_statement(
                statement="INC", period="annual"
            )
            return self.__income_annual

    @property
    def income_annual_mr(self) -> IncomeStatement:
        """income_annualMR"""
        try:
            return self.__income_annual_mr
        except AttributeError:
            self.__income_annual_mr = self.income_annual[0]
            return self.__income_annual_mr

    @property
    def income_quarter(self) -> list[IncomeStatement]:
        """income_quarter"""
        try:
            return self.__income_quarter
        except AttributeError:
            self.__income_quarter = self.parser.get_fin_statement(
                statement="INC", period="quarter"
            )
            return self.__income_quarter

    @property
    def income_mrq(self) -> IncomeStatement:
        try:
            return self.__income_mrq
        except AttributeError:
            self.__income_mrq = self.income_quarter[0]
            return self.__income_mrq

    @property
    def balance_annual(self) -> list[BalanceSheetStatement]:
        try:
            return self.__balance_annual
        except AttributeError:
            self.__balance_annual = self.parser.get_fin_statement(
                statement="BAL", period="annual"
            )
            return self.__balance_annual

    @property
    def balance_annual_mr(self) -> BalanceSheetStatement:
        try:
            return self.__balance_annual_mr
        except AttributeError:
            self.__balance_annual_mr = self.balance_annual[0]
            return self.__balance_annual_mr

    @property
    def balance_quarter(self) -> list[BalanceSheetStatement]:
        try:
            return self.__balance_quarter
        except AttributeError:
            self.__balance_quarter = self.parser.get_fin_statement(
                statement="BAL", period="quarter"
            )
            return self.__balance_quarter

    @property
    def balance_mrq(self) -> BalanceSheetStatement:
        try:
            return self.__balance_mrq
        except AttributeError:
            self.__balance_mrq = self.balance_quarter[0]
            return self.__balance_mrq

    @property
    def cashflow_annual(self) -> list[CashFlowStatement]:
        try:
            return self.__cashflow_annual
        except AttributeError:
            self.__cashflow_annual = self.parser.get_fin_statement(
                statement="CAS", period="annual"
            )
            return self.__cashflow_annual

    @property
    def cashflow_annual_mr(self) -> CashFlowStatement:
        try:
            return self.__cashflow_annual_mr
        except AttributeError:
            self.__cashflow_annual_mr = self.cashflow_annual[0]
            return self.__cashflow_annual_mr

    @property
    def cashflow_quarter(self) -> list[CashFlowStatement]:
        try:
            return self.__cashflow_quarter
        except AttributeError:
            self.__cashflow_quarter = self.parser.get_fin_statement(
                statement="CAS", period="quarter"
            )
            return self.__cashflow_quarter

    @property
    def cashflow_mrq(self) -> CashFlowStatement:
        try:
            return self.__cashflow_mrq
        except AttributeError:
            self.__cashflow_mrq = self.cashflow_quarter[0]
            return self.__cashflow_mrq

    @property
    def ownership_report(self) -> OwnershipReport:
        """Ownership Report"""
        try:
            return self.__ownership_report
        except AttributeError:
            self.__ownership_report = self.parser.get_ownership_report()
            return self.__ownership_report

    @property
    def dividend(self) -> list[Dividend]:
        try:
            return self.__dividend
        except AttributeError:
            self.__dividend = self.parser.get_dividend()
            return self.__dividend

    @property
    def div_ps_q(self) -> list[DividendPerShare]:
        try:
            return self.__div_ps_q
        except AttributeError:
            self.__div_ps_q = self.parser.get_div_per_share(
                report_type="R", period="3M"
            )
            return self.__div_ps_q

    @property
    def div_ps_ttm(self) -> list[DividendPerShare]:
        try:
            return self.__div_ps_ttm
        except AttributeError:
            self.__div_ps_ttm = self.parser.get_div_per_share(report_type="TTM")
            return self.__div_ps_ttm

    @property
    def revenue_ttm(self) -> list[Revenue]:
        try:
            return self.__revenue_ttm
        except AttributeError:
            self.__revenue_ttm = self.parser.get_revenue(report_type="TTM")
            return self.__revenue_ttm

    @property
    def revenue_q(self) -> list[Revenue]:
        try:
            return self.__revenue_q
        except AttributeError:
            self.__revenue_q = self.parser.get_revenue(report_type="R", period="3M")
            return self.__revenue_q

    @property
    def revenue_mrq(self) -> Revenue:
        try:
            return self.__revenue_mrq
        except AttributeError:
            self.__revenue_mrq = self.revenue_ttm[0]
            return self.__revenue_mrq

    @property
    def eps_ttm(self) -> list[EarningsPerShare]:
        try:
            return self.__eps_ttm
        except AttributeError:
            self.__eps_ttm = self.parser.get_eps(report_type="TTM")
            return self.__eps_ttm

    @property
    def eps_q(self) -> list[EarningsPerShare]:
        try:
            return self.__eps_q
        except AttributeError:
            self.__eps_q = self.parser.get_eps(report_type="R", period="3M")
            return self.__eps_q

    @property
    def eps_mrq(self) -> EarningsPerShare:
        try:
            return self.__eps_mrq
        except AttributeError:
            self.__eps_mrq = self.eps_ttm[0]
            return self.__eps_mrq

    @property
    def analyst_forecast(self) -> AnalystForecast:
        try:
            return self.__analyst_forecast
        except AttributeError:
            self.__analyst_forecast = self.parser.get_analyst_forecast()
            return self.__analyst_forecast

    @property
    def ratios(self) -> RatioSnapshot:
        try:
            return self.__ratios
        except AttributeError:
            self.__ratios = self.parser.get_ratios()
            return self.__ratios

    @property
    def fundamental_ratios(self) -> FundamentalRatios:
        try:
            return self.__fundamental_ratios
        except AttributeError:
            self.__fundamental_ratios = self.client.get_ratios()
            self.ticker = self.client.ib.ticker(self.contract)
            return self.__fundamental_ratios

    @property
    def fy_estimates(self) -> list[ForwardYear]:
        try:
            return self.__fy_estimates
        except AttributeError:
            self.__fy_estimates = self.parser.get_fy_estimates()
            return self.__fy_estimates

    @property
    def fy_actuals(self) -> list[ForwardYear]:
        try:
            return self.__fy_actuals
        except AttributeError:
            self.__fy_actuals = self.parser.get_fy_actuals()
            return self.__fy_actuals

    @property
    def company_info(self) -> CompanyInfo:
        try:
            return self.__company_info
        except AttributeError:
            self.__company_info = self.parser.get_company_info()
            return self.__company_info
