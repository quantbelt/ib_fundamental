#!/usr/bin/env python3
"""
Created on Thu May 9 16:21:58 2021

@author: gonzo
"""
from dataclasses import dataclass
from datetime import date, datetime
from typing import Literal, Optional

# pylint: disable-next=unused-import
from ib_async.objects import FundamentalRatios

# StatementType = Literal["Income", "Balance", "Cash"]
StatementCode = Literal["INC", "BAL", "CAS"]
PeriodType = Literal["annual", "quarter"]
StatementPeriod = Literal["Interim", "Annual"]
ReportType = Literal[
    "ReportsFinStatements",
    "ReportsFinSummary",
    "ReportSnapshot",
    "RESC",
    "ReportsOwnership",
    "CalendarReport",
]


@dataclass
class FinancialStatement:
    """Financial Statement Base class"""

    period: Optional[StatementPeriod] = None
    end_date: Optional[date] = None
    fiscal_year: Optional[int] = None
    period_number: Optional[int] = None
    date_10Q: str = ""  # pylint: disable=invalid-name
    date_10K: str = ""  # pylint: disable=invalid-name


@dataclass
class IncomeStatement(FinancialStatement):
    """Income Statement"""

    statement = "Income Statement"
    srev: Optional[float] = None
    sore: Optional[float] = None
    rtlr: Optional[float] = None
    scor: Optional[float] = None
    sgrp: Optional[float] = None
    ssga: Optional[float] = None
    erad: Optional[float] = None
    sdpr: Optional[float] = None
    sinn: Optional[float] = None
    suie: Optional[float] = None
    sooe: Optional[float] = None
    etoe: Optional[float] = None
    sopi: Optional[float] = None
    snin: Optional[float] = None
    ngla: Optional[float] = None
    sont: Optional[float] = None
    eibt: Optional[float] = None
    ttax: Optional[float] = None
    tiat: Optional[float] = None
    cmin: Optional[float] = None
    ceia: Optional[float] = None
    cgap: Optional[float] = None
    nibx: Optional[float] = None
    stxi: Optional[float] = None
    ninc: Optional[float] = None
    sani: Optional[float] = None
    ciac: Optional[float] = None
    xnic: Optional[float] = None
    sdaj: Optional[float] = None
    sdni: Optional[float] = None
    sdws: Optional[float] = None
    sdbf: Optional[float] = None
    ddps1: Optional[float] = None
    vdes: Optional[float] = None


@dataclass
class BalanceSheetStatement(FinancialStatement):
    """Balance Sheet class"""

    statement = "Balance Sheet Statement"
    acsh: Optional[float] = None
    acae: Optional[float] = None
    asti: Optional[float] = None
    scsi: Optional[float] = None
    aacr: Optional[float] = None
    atrc: Optional[float] = None
    aitl: Optional[float] = None
    appy: Optional[float] = None
    soca: Optional[float] = None
    atca: Optional[float] = None
    aptc: Optional[float] = None
    adep: Optional[float] = None
    appn: Optional[float] = None
    agwi: Optional[float] = None
    aint: Optional[float] = None
    sinv: Optional[float] = None
    altr: Optional[float] = None
    sola: Optional[float] = None
    atot: Optional[float] = None
    lapb: Optional[float] = None
    lpba: Optional[float] = None
    laex: Optional[float] = None
    lstd: Optional[float] = None
    lcld: Optional[float] = None
    socl: Optional[float] = None
    ltcl: Optional[float] = None
    lltd: Optional[float] = None
    lclo: Optional[float] = None
    lttd: Optional[float] = None
    stld: Optional[float] = None
    sbdt: Optional[float] = None
    lmin: Optional[float] = None
    sltl: Optional[float] = None
    ltll: Optional[float] = None
    srpr: Optional[float] = None
    sprs: Optional[float] = None
    scms: Optional[float] = None
    qpic: Optional[float] = None
    qred: Optional[float] = None
    qtsc: Optional[float] = None
    qedg: Optional[float] = None
    qugl: Optional[float] = None
    sote: Optional[float] = None
    qtle: Optional[float] = None
    qtel: Optional[float] = None
    qtco: Optional[float] = None
    qtpo: Optional[float] = None
    stbp: Optional[float] = None


@dataclass
class CashFlowStatement(FinancialStatement):
    """Cash flow statement class"""

    statement = "Cash Flow Statement"
    onet: Optional[float] = None
    sded: Optional[float] = None
    samt: Optional[float] = None
    obdt: Optional[float] = None
    snci: Optional[float] = None
    socf: Optional[float] = None
    otlo: Optional[float] = None
    scex: Optional[float] = None
    sicf: Optional[float] = None
    itli: Optional[float] = None
    sfcf: Optional[float] = None
    fcdp: Optional[float] = None
    fpss: Optional[float] = None
    fprd: Optional[float] = None
    ftlf: Optional[float] = None
    sfee: Optional[float] = None
    sncc: Optional[float] = None
    scip: Optional[float] = None
    sctp: Optional[float] = None


@dataclass
class StatementMap:
    """Financial statement map item"""

    coa_item: str
    map_item: str
    statement_type: StatementCode
    line_id: int


StatementMapping = list[StatementMap]

statement_map = {
    "INC": IncomeStatement,
    "BAL": BalanceSheetStatement,
    "CAS": CashFlowStatement,
}


@dataclass
class Dividend:
    """Dividend"""

    type: str
    ex_date: datetime
    record_date: datetime
    pay_date: datetime
    declaration_date: datetime
    currency: str
    value: float


@dataclass
class DividendPerShare:
    """Dividen per share"""

    as_of_date: str
    report_type: str
    period: str
    currency: str
    value: float


@dataclass
class Revenue:
    """Revenue"""

    as_of_date: datetime
    report_type: str
    revenue: float


@dataclass
class EarningsPerShare:
    """Earnings per share"""

    as_of_date: datetime
    report_type: str
    eps: float


@dataclass
class AnalystForecast:
    """Analyst Forecast"""

    cons_recom: float
    target_price: float
    proj_lt_growth_rate: float
    proj_pe: float
    proj_sales: float
    proj_sales_q: float
    proj_eps: float
    proj_epsq: float
    proj_profit: float
    proj_dps: float


@dataclass
class RatioSnapshot:
    """Company Ratios"""

    nprice: float
    nhig: float
    nlow: float
    pdate: date
    vol10davg: float
    ev: float
    mktcap: float
    ttmrev: float
    ttmebitd: float
    ttmniac: float
    ttmepsxclx: float
    ttmrevps: float
    qbvps: float
    qcshps: float
    ttmcfshr: float
    ttmdivshr: float
    ttmgrosmgn: float
    ttmroepct: float
    ttmpr2rev: float
    peexclxor: float
    price2bk: float
    employees: float


@dataclass
class ForwardYear:
    """Forward Year"""

    type: Literal["Estimate", "Actual"]
    item: str  # type
    unit: Literal["U", "M"]
    period_type: Literal["A", "Q"]
    fyear: int
    end_month: int
    end_cal_year: int
    value: float
    est_type: Optional[
        Literal["High", "Low", "Mean", "Median", "NumOfEst", "StdDev"]
    ] = ""
    updated: Optional[datetime] = None


@dataclass
class CompanyInfo:
    """Company Info"""

    ticker: str
    company_name: str
    cik: str
    exchange_code: str
    exchange: str
    irs: str


@dataclass
class OwnershipCompany:
    """Ownership Company details"""

    ISIN: str
    float_shares: int
    as_of_date: datetime


@dataclass
class OwnershipDetails:
    """Ownership details"""

    owner_id: str
    type: int
    as_of_date: datetime
    name: str
    quantity: float
    currency: Optional[str] = ""


@dataclass
class OwnershipReport:
    """Ownership Report"""

    company: OwnershipCompany
    ownership_details: list[OwnershipDetails]
