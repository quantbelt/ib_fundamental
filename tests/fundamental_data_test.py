"""Test fundamental FundamentalData module"""

from ib_async import Dividends, FundamentalRatios, Ticker

from ib_fundamental.fundamental import FundamentalData
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
)


class TestFundamentalData:
    """Test FundamentalData class"""

    def test_statement_inc_annual(self, fundamental_data: FundamentalData):
        """Test FundamentalData annual income statement"""
        # act
        _fund_data = fundamental_data
        _inc = _fund_data.income_annual
        # assert
        assert isinstance(_inc, list)
        assert len(_inc) > 1
        assert isinstance(_inc[0], IncomeStatement)
        assert _inc[0].period == "Annual"

    def test_statement_inc_quarter(self, fundamental_data: FundamentalData):
        """Test FundamentalData quarter income statement"""
        # act
        _fund_data = fundamental_data
        _inc = _fund_data.income_quarter
        # assert
        assert isinstance(_inc, list)
        assert len(_inc) > 1
        assert isinstance(_inc[0], IncomeStatement)
        assert _inc[0].period == "Interim"

    def test_statement_bal_annual(self, fundamental_data: FundamentalData):
        """Test FundamentalData annual balance sheet"""
        # act
        _fund_data = fundamental_data
        _inc = _fund_data.balance_annual
        # assert
        assert isinstance(_inc, list)
        assert len(_inc) > 1
        assert isinstance(_inc[0], BalanceSheetStatement)
        assert _inc[0].period == "Annual"

    def test_statement_bal_quarter(self, fundamental_data: FundamentalData):
        """Test FundamentalData balance sheet quarter"""
        # act
        _fund_data = fundamental_data
        _inc = _fund_data.balance_quarter
        # assert
        assert isinstance(_inc, list)
        assert len(_inc) > 1
        assert isinstance(_inc[0], BalanceSheetStatement)
        assert _inc[0].period == "Interim"

    def test_statement_cas_annual(self, fundamental_data: FundamentalData):
        """Test FundamentalData annual cashflow"""
        # act
        _fund_data = fundamental_data
        _inc = _fund_data.cashflow_annual
        # assert
        assert isinstance(_inc, list)
        assert len(_inc) > 1
        assert isinstance(_inc[0], CashFlowStatement)
        assert _inc[0].period == "Annual"

    def test_statement_cas_quarter(self, fundamental_data: FundamentalData):
        """Test FundamentalData cashflow quarter"""
        # act
        _fund_data = fundamental_data
        _inc = _fund_data.cashflow_quarter
        # assert
        assert isinstance(_inc, list)
        assert len(_inc) > 1
        assert isinstance(_inc[0], CashFlowStatement)
        assert _inc[0].period == "Interim"

    def test_ownership(self, fundamental_data: FundamentalData):
        """Test FundamentalData ownership report"""
        # act
        _fund_data = fundamental_data
        _own = _fund_data.ownership_report
        # assert
        assert isinstance(_own, OwnershipReport)
        assert isinstance(_own.company, OwnershipCompany)
        assert isinstance(_own.ownership_details, list)
        assert len(_own.ownership_details) > 1
        assert isinstance(_own.ownership_details[0], OwnershipDetails)

    def test_dividend(self, fundamental_data: FundamentalData):
        """Test FundamentalData dividends"""
        # act
        _fund_data = fundamental_data
        _div = _fund_data.dividend
        # assert
        assert isinstance(_div, list)
        assert len(_div) > 1
        assert isinstance(_div[0], Dividend)
        assert _div[0].currency == "USD"

    def test_dividend_summary(self, fundamental_data: FundamentalData):
        """Test FundamentalData dividend summary"""
        # act
        _fund_data = fundamental_data
        _div_summary = _fund_data.dividend_summary
        # assert
        assert isinstance(_div_summary, Dividends)

    def test_div_per_share_ttm(self, fundamental_data: FundamentalData):
        """Test XMLparser div per share TTM"""
        # act
        _fund_data = fundamental_data
        _divps = _fund_data.div_ps_ttm
        # assert
        assert isinstance(_divps, list)
        assert len(_divps) > 1
        assert isinstance(_divps[0], DividendPerShare)
        assert _divps[0].report_type == "TTM"
        assert _divps[0].period == "12M"
        assert _divps[0].currency == "USD"

    def test_div_per_share_q(self, fundamental_data: FundamentalData):
        """Test XMLparser div per share quarter"""
        # act
        _fund_data = fundamental_data
        _divps = _fund_data.div_ps_q
        # assert
        assert isinstance(_divps, list)
        assert len(_divps) > 1
        assert isinstance(_divps[0], DividendPerShare)
        assert _divps[0].report_type == "R"
        assert _divps[0].period == "3M"
        assert _divps[0].currency == "USD"

    def test_revenue_ttm(self, fundamental_data: FundamentalData):
        """Test XMLparser revenue ttm"""
        # act
        _fund_data = fundamental_data
        _rev = _fund_data.revenue_ttm
        # assert
        assert isinstance(_rev, list)
        assert len(_rev) > 1
        assert isinstance(_rev[0], Revenue)
        assert _rev[0].report_type == "TTM"
        assert _rev[0].period == "12M"

    def test_revenue_q(self, fundamental_data: FundamentalData):
        """Test XMLparser revenue quarter"""
        # act
        _fund_data = fundamental_data
        _rev = _fund_data.revenue_q
        # assert
        assert isinstance(_rev, list)
        assert len(_rev) > 1
        assert isinstance(_rev[0], Revenue)
        assert _rev[0].report_type == "R"
        assert _rev[0].period == "3M"

    def test_eps_ttm(self, fundamental_data: FundamentalData):
        """Test XMLparser eps ttm"""
        # act
        _fund_data = fundamental_data
        _eps = _fund_data.eps_ttm
        # assert
        assert isinstance(_eps, list)
        assert len(_eps) > 1
        assert isinstance(_eps[0], EarningsPerShare)
        assert _eps[0].report_type == "TTM"
        assert _eps[0].period == "12M"

    def test_eps_q(self, fundamental_data: FundamentalData):
        """Test XMLparser eps quarter"""
        # act
        _fund_data = fundamental_data
        _eps = _fund_data.eps_q
        # assert
        assert isinstance(_eps, list)
        assert len(_eps) > 1
        assert isinstance(_eps[0], EarningsPerShare)
        assert _eps[0].report_type == "R"
        assert _eps[0].period == "3M"

    def test_analyst_forecast(self, fundamental_data: FundamentalData):
        """Test FundamentalData analyst forecast"""
        # act
        _fund_data = fundamental_data
        _analyst = _fund_data.analyst_forecast
        # assert
        assert isinstance(_analyst, AnalystForecast)
        assert hasattr(_analyst, "target_price")
        assert isinstance(_analyst.target_price, float)
        assert hasattr(_analyst, "proj_eps")
        assert isinstance(_analyst.proj_eps, float)

    def test_ratios(self, fundamental_data: FundamentalData):
        """Test FundamentalData ratios"""
        # act
        _fund_data = fundamental_data
        _ratios = _fund_data.ratios
        # assert
        assert isinstance(_ratios, RatioSnapshot)
        assert hasattr(_ratios, "ttmrev")

    def test_fundamental_rations(self, fundamental_data: FundamentalData):
        """Test FundamentalData fundamental ratios"""
        # act
        _fund_data = fundamental_data
        _f_ratios = _fund_data.fundamental_ratios
        # assert
        assert isinstance(_f_ratios, FundamentalRatios)
        assert hasattr(_fund_data, "ticker")
        assert isinstance(_fund_data.ticker, Ticker)

    def test_fy_estimates(self, fundamental_data: FundamentalData):
        """Test FundamentalData fy estimates"""
        # act
        _fund_data = fundamental_data
        _estimates = _fund_data.fy_estimates
        # assert
        assert isinstance(_estimates, list)
        assert len(_estimates) > 1
        assert isinstance(_estimates[0], ForwardYear)

    def test_fy_actuals(self, fundamental_data: FundamentalData):
        """Test FundamentalData fy actuals"""
        # act
        _fund_data = fundamental_data
        _actuals = _fund_data.fy_actuals
        # assert
        assert isinstance(_actuals, list)
        assert len(_actuals) > 1
        assert isinstance(_actuals[0], ForwardYear)

    def test_company_info(self, fundamental_data: FundamentalData):
        """Test FundamentalData company info"""
        # act
        _fund_data = fundamental_data
        _info = _fund_data.company_info
        # assert
        assert isinstance(_info, CompanyInfo)
        assert _info.ticker == _fund_data.parser.xml_report.client.symbol
