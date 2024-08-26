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
    "XMLParser",
]

from datetime import date, datetime
from typing import Literal, Optional

import pandas as pd

from .ib_client import IBClient
from .objects import (
    AnalystForecast,
    CompanyInfo,
    Dividend,
    DividendPerShare,
    EarningsPerShare,
    ForwardYear,
    OwnershipCompany,
    OwnershipDetails,
    OwnershipReport,
    PeriodType,
    RatioSnapshot,
    Revenue,
    StatementCode,
    StatementMap,
    StatementMapping,
    statement_map,
)
from .utils import camel_to_snake
from .xml_report import XMLReport

fromisoformat = datetime.fromisoformat

SummaryReportType = Literal["A", "TTM", "R", "P", None]
SummaryPeriod = Literal["12M", "3M", None]


class XMLParser:
    """Parser for IBKR xml company fundamental data"""

    def __init__(self, ib_client: IBClient):
        self.xml_report = XMLReport(ib_client=ib_client)

    def __repr__(self):
        cls_name = self.__class__.__qualname__
        return f"{cls_name}(ib_client={self.xml_report.client!r}"

    def get_fin_statement(
        self,
        statement: StatementCode = "INC",
        period: PeriodType = "annual",
        end_date: Optional[date] = None,
    ):
        """

        Parameters
        ----------
        period : 'annual' OR 'quarter', mandatory.
            statement period, annual or quarter. The default is 'annual'.
        statement : 'INC', 'BAL'or 'CAS'. mandatory.
            the statement to be generated
        end_date : 'YYYY-MM-DD' str format, optional
            statement date. The default is None.

        Raises
        ------
        Exception
            if period parameter is missing

        Returns
        -------
        list
            DESCRIPTION.

        """
        xpath = {
            "annual": ".//AnnualPeriods/FiscalPeriod",
            "quarter": ".//InterimPeriods/FiscalPeriod",
            "xp_fiscal_period": '[@EndDate="{0}"]/Statement[@Type="{1}"]/lineItem',
        }

        # statement type
        xp_statement = statement
        # period type
        xp_line = xpath[period]
        # filter by end_date
        if end_date is not None:
            xp_line_ed = xp_line + f'[@EndDate="{end_date.isoformat()}"]'
        else:
            xp_line_ed = xp_line

        fp = self.xml_report.fin_statements.findall(xp_line_ed)

        if period == "quarter":
            fperiods = [
                {
                    "period": fperiod.attrib["Type"],
                    "end_date": fperiod.attrib["EndDate"],
                    "fiscal_year": fperiod.attrib["FiscalYear"],
                    "period_number": fperiod.attrib["FiscalPeriodNumber"],
                    "date_10Q": fperiod.find(".//Source").attrib["Date"],
                }
                for fperiod in fp
            ]
        else:
            fperiods = [
                {
                    "period": fperiod.attrib["Type"],
                    "end_date": fperiod.attrib["EndDate"],
                    "fiscal_year": fperiod.attrib["FiscalYear"],
                    "date_10K": fperiod.find(".//Source").attrib["Date"],
                }
                for fperiod in fp
            ]

        fs = []

        for p in fperiods:
            if end_date is not None:
                ed = end_date.isoformat()
            else:
                ed = p["end_date"]

            xp = xpath["xp_fiscal_period"].format(ed, xp_statement)
            fs_line = self.xml_report.fin_statements.findall(xp_line + xp)

            fs.append({i.attrib["coaCode"].lower(): float(i.text) for i in fs_line})

        return [statement_map[statement](**i, **j) for i, j in zip(fperiods, fs)]

    def get_map_items(
        self, statement: Optional[StatementCode] = None
    ) -> StatementMapping:
        """
        mapItems

        Returns
        -------
        list of dict with FinStatement name mapping
        """

        fa = ".//COAMap/"
        fs = self.xml_report.fin_statements.findall(fa)

        _map_items: StatementMapping = [
            StatementMap(
                coa_item=mi.attrib["coaItem"],
                map_item=mi.text,
                statement_type=mi.attrib["statementType"],
                line_id=int(mi.attrib["lineID"]),
            )
            for mi in fs
            if statement is None
            or (statement is not None and mi.attrib["statementType"] == statement)
        ]
        return _map_items

    def get_ownership_report(self) -> OwnershipReport:
        """Ownership Report"""
        fs = self.xml_report.ownership
        (isin,) = fs.findall("./ISIN")
        (fa,) = fs.findall("./floatShares")
        company = OwnershipCompany(
            ISIN=isin.text,
            float_shares=int(fa.text),
            as_of_date=fromisoformat(fa.attrib["asofDate"]),
        )
        _l = []
        fa = fs.findall("./Owner")

        for i in fa:
            d = {}
            d["owner_id"] = i.attrib["ownerId"]

            for j in i.findall("./"):
                if "as_of_date" not in d and j.attrib:
                    d["as_of_date"] = datetime.fromisoformat(j.attrib["asofDate"])
                d[j.tag] = float(j.text) if j.tag == "quantity" else j.text

            _l.append(OwnershipDetails(**d))

        return OwnershipReport(company=company, ownership_details=_l)

    def get_dividend(self) -> list[Dividend] | None:
        """get dividends"""
        fa = "./Dividends"
        fs = self.xml_report.fin_summary.find(fa)
        if fs is None:
            return None
        curr = fs.attrib["currency"]
        _dividend = [
            Dividend(
                type=i.attrib["type"],
                ex_date=fromisoformat(i.attrib["exDate"]),
                record_date=fromisoformat(i.attrib["recordDate"]),
                pay_date=fromisoformat(i.attrib["payDate"]),
                declaration_date=fromisoformat(i.attrib["declarationDate"]),
                currency=curr,
                value=float(i.text),
            )
            for i in fs
        ]
        return _dividend

    def get_div_per_share(
        self,
        report_type: SummaryReportType = None,
        period: SummaryPeriod = None,
    ) -> list[DividendPerShare] | None:
        """Dividend per share"""
        fa = "./DividendPerShares"
        fs = self.xml_report.fin_summary.find(fa)
        if fs is None:
            return None
        curr = fs.attrib["currency"]

        _div_ps = [
            DividendPerShare(
                as_of_date=fromisoformat(i.attrib["asofDate"]),
                report_type=i.attrib["reportType"],
                period=i.attrib["period"],
                currency=curr,
                value=float(i.text),
            )
            for i in fs
            if (
                report_type is None
                or (report_type is not None and i.attrib["reportType"] == report_type)
            )
            and (
                period is None or (period is not None and i.attrib["period"] == period)
            )
        ]
        return _div_ps

    def get_revenue(
        self,
        report_type: SummaryReportType = None,
        period: SummaryPeriod = None,
    ) -> list[Revenue]:
        """Revenue"""
        fa = "./TotalRevenues"
        fs = self.xml_report.fin_summary.find(fa)
        curr = fs.attrib["currency"]

        _revenue = [
            Revenue(
                as_of_date=fromisoformat(tr.attrib["asofDate"]),
                report_type=tr.attrib["reportType"],
                period=tr.attrib["period"],
                currency=curr,
                revenue=float(tr.text),
            )
            for tr in fs
            if (
                report_type is None
                or (report_type is not None and tr.attrib["reportType"] == report_type)
            )
            and (
                period is None or (period is not None and tr.attrib["period"] == period)
            )
        ]
        return _revenue

    def get_eps(
        self,
        report_type: SummaryReportType = None,
        period: SummaryPeriod = None,
    ) -> list[EarningsPerShare]:
        """Earnings per share"""
        fa = "./EPSs"
        fs = self.xml_report.fin_summary.find(fa)
        curr = fs.attrib["currency"]

        _eps = [
            EarningsPerShare(
                as_of_date=fromisoformat(tr.attrib["asofDate"]),
                report_type=tr.attrib["reportType"],
                period=tr.attrib["period"],
                currency=curr,
                eps=float(tr.text),
            )
            for tr in fs
            if (
                report_type is None
                or (report_type is not None and tr.attrib["reportType"] == report_type)
            )
            and (
                period is None or (period is not None and tr.attrib["period"] == period)
            )
        ]
        return _eps

    def get_analyst_forecast(self) -> AnalystForecast:
        """Analyst forecast"""
        fa = ".//ForecastData/Ratio"
        fs = self.xml_report.snapshot.findall(fa)

        _analyst_forecast = AnalystForecast(
            **{
                camel_to_snake(g.attrib["FieldName"]): float(
                    g.findall("./Value")[0].text
                )
                for g in fs
            }
        )
        return _analyst_forecast

    def get_ratios(self) -> RatioSnapshot:
        """Company ratios snapshot"""
        fa = ".//Ratios/Group/Ratio"
        fs = self.xml_report.snapshot.findall(fa)

        _ratios = RatioSnapshot(
            **{
                r.attrib["FieldName"].lower(): (
                    fromisoformat(r.text) if r.attrib["Type"] == "D" else float(r.text)
                )
                for r in fs
            }
        )
        return _ratios

    def get_fy_estimates(self) -> list[ForwardYear]:
        """Forward Year estimates"""
        fs = self.xml_report.resc
        _fy_estimates = [
            ForwardYear(
                type="Estimate",
                item=a.attrib["type"],
                unit=a.attrib["unit"],
                period_type=p.attrib["periodType"],
                fyear=int(p.attrib["fYear"]),
                end_month=int(p.attrib["endMonth"]),
                end_cal_year=int(p.attrib["endCalYear"]),
                value=float(e[0].text),
                est_type=e.attrib["type"],
            )
            for a in fs.iter("FYEstimate")
            for p in a.iter("FYPeriod")
            for e in p.iter("ConsEstimate")
        ]
        return _fy_estimates

    def get_fy_actuals(self) -> list[ForwardYear]:
        """Forward year actuals"""
        fs = self.xml_report.resc
        _fy_actuals = [
            ForwardYear(
                type="Actual",
                item=a.attrib["type"],
                unit=a.attrib["unit"],
                period_type=p.attrib["periodType"],
                fyear=int(p.attrib["fYear"]),
                end_month=int(p.attrib["endMonth"]),
                end_cal_year=int(p.attrib["endCalYear"]),
                value=float(p[0].text),
                updated=pd.to_datetime(p[0].attrib["updated"]),
            )
            for a in fs.iter("FYActual")
            for p in a.iter("FYPeriod")
        ]
        return _fy_actuals

    def get_company_info(self) -> CompanyInfo:
        """Company Info"""
        fs = self.xml_report.fin_statements
        coids = {r.attrib["Type"]: r.text for r in fs.findall("./CoIDs/CoID")}
        issue_id = {
            r.attrib["Type"]: r.text for r in fs.findall("./Issues/Issue/IssueID")
        }
        exchange = {r.tag: r.text for r in fs.findall("./Issues/Issue/Exchange")}
        exchange_code = {
            "code": r.attrib["Code"] for r in fs.findall("./Issues/Issue/Exchange")
        }
        _company_info = CompanyInfo(
            ticker=issue_id.get("Ticker"),
            company_name=coids.get("CompanyName"),
            cik=coids.get("CIKNo"),
            exchange_code=exchange_code.get("code"),
            exchange=exchange.get("Exchange"),
            irs=coids.get("IRSNo"),
        )
        return _company_info
