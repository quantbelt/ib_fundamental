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

"""Company Fundamental class
"""
# pylint: disable=attribute-defined-outside-init
# pylint: disable=missing-function-docstring

__all__ = [
    "FundamentalData",
]

from datetime import datetime
from typing import Optional

import pandas as pd
from ib_async import IB, Dividends, FundamentalRatios, Stock, Ticker
from pandas import DataFrame

from ib_fundamental.objects import (
    AnalystForecast,
    BalanceSheetSet,
    CashFlowSet,
    CompanyInfo,
    Dividend,
    DividendPerShare,
    EarningsPerShare,
    ForwardYear,
    IncomeSet,
    OwnershipReport,
    RatioSnapshot,
    Revenue,
    StatementCode,
    StatementData,
    statement_type,
)
from ib_fundamental.utils import to_dataframe

from .ib_client import IBClient
from .xml_parser import XMLParser

fromisoformat = datetime.fromisoformat


class FundamentalData:
    """Company fundamental data"""

    # pylint: disable=too-many-arguments,too-many-public-methods
    # pylint: disable=too-many-instance-attributes
    def __init__(
        self, ib: IB, symbol: str, exchange: str = "SMART", currency: str = "USD"
    ) -> None:
        """Args:
        ib (ib_async.IB): ib_async.IB instance
        symbol (str): company symbol/ticker
        exchange (str, optional): exchange. Defaults to "SMART".
        currency (str, optional): currency. Defaults to "USD".
        """
        self.client = IBClient(
            symbol=symbol, ib=ib, exchange=exchange, currency=currency
        )
        self.symbol = symbol
        self.contract: Stock = self.client.contract
        self.ticker: Optional[Ticker] = None
        self.parser = XMLParser(ib_client=self.client)

    def __repr__(self):
        cls_name = self.__class__.__qualname__
        return f"{cls_name}(symbol={self.symbol!r},IB={self.client.ib!r})"

    def __enter__(self):
        return self

    @property
    def income_annual(self) -> IncomeSet:
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
    def income_quarter(self) -> IncomeSet:
        """income_quarter"""
        try:
            return self.__income_quarter
        except AttributeError:
            self.__income_quarter = self.parser.get_fin_statement(
                statement="INC", period="quarter"
            )
            return self.__income_quarter

    @property
    def balance_annual(self) -> BalanceSheetSet:
        try:
            return self.__balance_annual
        except AttributeError:
            self.__balance_annual = self.parser.get_fin_statement(
                statement="BAL", period="annual"
            )
            return self.__balance_annual

    @property
    def balance_quarter(self) -> BalanceSheetSet:
        try:
            return self.__balance_quarter
        except AttributeError:
            self.__balance_quarter = self.parser.get_fin_statement(
                statement="BAL", period="quarter"
            )
            return self.__balance_quarter

    @property
    def cashflow_annual(self) -> CashFlowSet:
        try:
            return self.__cashflow_annual
        except AttributeError:
            self.__cashflow_annual = self.parser.get_fin_statement(
                statement="CAS", period="annual"
            )
            return self.__cashflow_annual

    @property
    def cashflow_quarter(self) -> CashFlowSet:
        try:
            return self.__cashflow_quarter
        except AttributeError:
            self.__cashflow_quarter = self.parser.get_fin_statement(
                statement="CAS", period="quarter"
            )
            return self.__cashflow_quarter

    @property
    def ownership_report(self) -> OwnershipReport:
        """Ownership Report"""
        try:
            return self.__ownership_report
        except AttributeError:
            self.__ownership_report = self.parser.get_ownership_report()
            return self.__ownership_report

    @property
    def dividend(self) -> list[Dividend] | None:
        try:
            return self.__dividend
        except AttributeError:
            self.__dividend: list[Dividend] | None = self.parser.get_dividend()
            return self.__dividend

    @property
    def div_ps_q(self) -> list[DividendPerShare] | None:
        try:
            return self.__div_ps_q
        except AttributeError:
            self.__div_ps_q: list[DividendPerShare] | None = (
                self.parser.get_div_per_share(report_type="R", period="3M")
            )
            return self.__div_ps_q

    @property
    def div_ps_ttm(self) -> list[DividendPerShare] | None:
        try:
            return self.__div_ps_ttm
        except AttributeError:
            self.__div_ps_ttm: list[DividendPerShare] | None = (
                self.parser.get_div_per_share(report_type="TTM")
            )
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
    def dividend_summary(self) -> Dividends:
        try:
            return self.__dividend_summary
        except AttributeError:
            self.__dividend_summary = self.client.get_dividends()
            self.ticker = self.client.ib.ticker(self.contract)
            return self.__dividend_summary

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


class CompanyFinancials:
    """Company Financials"""

    def __init__(
        self, ib: IB, symbol: str, exchange: str = "SMART", currency: str = "USD"
    ) -> None:
        """
        Args:
            ib (ib_async.IB): ib_async.IB instance
            symbol (str): company symbol/ticker
            exchange (str, optional): exchange. Defaults to "SMART".
            currency (str, optional): currency. Defaults to "USD".
        """
        self.data = FundamentalData(
            symbol=symbol, ib=ib, exchange=exchange, currency=currency
        )

    def __repr__(self):
        cls_name = self.__class__.__qualname__
        return f"{cls_name}(symbol={self.data.symbol!r},IB={self.data.client.ib!r})"

    def _get_data_frame(
        self,
        statement: StatementData,
    ) -> DataFrame:
        """Build dataframe for pp"""
        _df = to_dataframe(statement)
        return _df.T.sort_index(axis=1, ascending=False)  # sort columns

    def _get_map_items(self, stat_code: StatementCode) -> DataFrame:
        """build map items for pp"""
        _df = to_dataframe(self.data.parser.get_map_items(statement=stat_code))
        _df.coa_item = _df.coa_item.str.lower()
        return _df

    def _get_header(
        self, data: DataFrame, statement_code: StatementCode, idx: int = 6
    ) -> DataFrame:
        """build header for pp"""
        _header = data.iloc[:idx]
        _header = (
            _header.assign(line_id=range(idx))
            .assign(statement_type=statement_code)
            .reset_index()
            .rename(columns={"index": "map_item"})
        )
        return _header.assign(coa_item=_header["map_item"])

    def _join(
        self, data: DataFrame, header: DataFrame, mapping: DataFrame, idx: int
    ) -> DataFrame:
        """join data to present"""
        _pp = mapping.join(data, on="coa_item")
        _df = pd.concat([header, _pp]).set_index("line_id")

        (_names,) = _df.loc[
            _df["coa_item"] == "end_date", _df.columns[1:idx]
        ].values.tolist()
        _l = _df.columns.to_list()
        _l[1:idx] = _names
        _df.columns = _l
        _df.statement_type = _df.statement_type.map(lambda x: statement_type[x])
        _df = _df.drop(columns="coa_item").dropna()
        return _df

    def _build_statement(
        self, data: StatementData, statement_code: StatementCode, idx: int
    ) -> DataFrame:
        """build statement pp"""
        _map = self._get_map_items(stat_code=statement_code)
        _data = self._get_data_frame(statement=data)
        _header = self._get_header(data=_data, statement_code=statement_code)
        # pp
        return self._join(data=_data, header=_header, mapping=_map, idx=idx)

    @property
    def balance_quarter(self) -> DataFrame | None:
        """Quarterly balance statement"""
        if self.data.balance_quarter:
            return self._build_statement(self.data.balance_quarter, "BAL", 6)
        return None

    @property
    def balance_annual(self) -> DataFrame | None:
        if self.data.balance_annual:
            return self._build_statement(self.data.balance_annual, "BAL", 7)
        return None

    @property
    def income_quarter(self) -> DataFrame | None:
        if self.data.income_quarter:
            return self._build_statement(self.data.income_quarter, "INC", 6)
        return None

    @property
    def income_annual(self) -> DataFrame | None:
        if self.data.income_annual:
            return self._build_statement(self.data.income_annual, "INC", 7)
        return None

    @property
    def cashflow_quarter(self) -> DataFrame | None:
        if self.data.cashflow_annual:
            return self._build_statement(self.data.cashflow_quarter, "CAS", 6)
        return None

    @property
    def cashflow_annual(self) -> DataFrame | None:
        if self.data.cashflow_annual:
            return self._build_statement(self.data.cashflow_annual, "CAS", 7)
        return None

    @property
    def dividends(self) -> DataFrame | None:
        if self.data.dividend:
            return to_dataframe(self.data.dividend, key="ex_date")
        return None

    @property
    def dividends_ps_q(self) -> DataFrame | None:
        if self.data.div_ps_q:
            return to_dataframe(self.data.div_ps_q, key="as_of_date")
        return None

    @property
    def dividends_ps_ttm(self) -> DataFrame | None:
        if self.data.div_ps_ttm:
            return to_dataframe(self.data.div_ps_ttm, key="as_of_date")
        return None

    @property
    def revenue_q(self) -> DataFrame | None:
        if self.data.revenue_q:
            return to_dataframe(self.data.revenue_q, key="as_of_date")
        return None

    @property
    def revenue_ttm(self) -> DataFrame | None:
        if self.data.revenue_ttm:
            return to_dataframe(self.data.revenue_ttm, key="as_of_date")
        return None

    @property
    def eps_q(self) -> DataFrame | None:
        if self.data.eps_q:
            return to_dataframe(self.data.eps_q, key="as_of_date")
        return None

    @property
    def eps_ttm(self) -> DataFrame | None:
        if self.data.eps_ttm:
            return to_dataframe(self.data.eps_ttm, key="as_of_date")
        return None

    @property
    def ownership(self) -> DataFrame | None:
        if self.data.ownership_report:
            return to_dataframe(self.data.ownership_report.ownership_details)
        return None

    @property
    def fy_actuals(self) -> DataFrame | None:
        if self.data.fy_actuals:
            return to_dataframe(self.data.fy_actuals, key="updated")
        return None

    @property
    def fy_estimates(self) -> DataFrame | None:
        if self.data.fy_estimates:
            return to_dataframe(self.data.fy_estimates)
        return None

    @property
    def analyst_forecast(self) -> DataFrame | None:
        if self.data.analyst_forecast:
            return to_dataframe([self.data.analyst_forecast]).T
        return None

    @property
    def company_information(self) -> DataFrame | None:
        if self.data.company_info:
            return to_dataframe([self.data.company_info]).T
        return None

    @property
    def ratios(self) -> DataFrame | None:
        if self.data.ratios:
            return to_dataframe([self.data.ratios]).T
        return None

    @property
    def fundamental_ratios(self) -> DataFrame | None:
        if self.data.fundamental_ratios:
            return to_dataframe([vars(self.data.fundamental_ratios)]).T
        return None
