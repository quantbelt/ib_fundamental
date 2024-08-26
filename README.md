# IB Fundamental

Interactive Brokers Fundamental data for humans.

This package will bring all fundamental data available through IBKR TWS API
into ready-to-use pandas data frames.

## Installation

You can install ib_fundamental using pip

```bash
pip install ib-fundamental
```

## Usage

You will need a TWS API port available

```python
import ib_async
from ib_fundamental import CompanyFinancials

# ib_async.util.startLoop() # if you are in a notebook

# connect to TWS API for ex on localhost:7497
ib = ib_async.IB().connect('localhost',7497)

# create your company financials instance
aapl = CompanyFinancials(ib=ib,symbol="AAPL")

# or specify exchange and currency
# aapl = CompanyFinancials(ib=ib,symbol="AAPL",exchange='SMART',currency='USD)

# get company info
aapl.company_information
                        0
ticker               AAPL
company_name    Apple Inc
cik            0000320193
exchange_code        NASD
exchange           NASDAQ
irs             942404110

# Annual income statement, while aapl.income_quarter will pull the quarterly report
aapl.income_annual

                                       map_item  2018-09-29  2019-09-28  2020-09-26  2021-09-25  2022-09-24  2023-09-30    statement_type
line_id
0                                        period      Annual      Annual      Annual      Annual      Annual      Annual  Income Statement
1                                      end_date  2018-09-29  2019-09-28  2020-09-26  2021-09-25  2022-09-24  2023-09-30  Income Statement
2                                   fiscal_year        2018        2019        2020        2021        2022        2023  Income Statement
4                                      date_10Q                                                                          Income Statement
5                                      date_10K  2018-11-05  2019-10-31  2020-10-30  2021-10-29  2022-10-28  2023-11-03  Income Statement
100                                     Revenue    265595.0    260174.0    274515.0    365817.0    394328.0    383285.0  Income Statement
310                               Total Revenue    265595.0    260174.0    274515.0    365817.0    394328.0    383285.0  Income Statement
360                      Cost of Revenue, Total    163756.0    161782.0    169559.0    212981.0    223546.0    214137.0  Income Statement
370                                Gross Profit    101839.0     98392.0    104956.0    152836.0    170782.0    169148.0  Income Statement
550      Selling/General/Admin. Expenses, Total     16705.0     18245.0     19916.0     21973.0     25094.0     24932.0  Income Statement
560                      Research & Development     14236.0     16217.0     18752.0     21914.0     26251.0     29915.0  Income Statement
830                     Total Operating Expense    194697.0    196244.0    208227.0    256868.0    274891.0    268984.0  Income Statement
840                            Operating Income     70898.0     63930.0     66288.0    108949.0    119437.0    114301.0  Income Statement
911      Interest Inc.(Exp.),Net-Non-Op., Total      2446.0      1385.0       890.0       198.0      -106.0      -183.0  Income Statement
1270                                 Other, Net      -441.0       422.0       -87.0        60.0      -228.0      -382.0  Income Statement
1280                    Net Income Before Taxes     72903.0     65737.0     67091.0    109207.0    119103.0    113736.0  Income Statement
1290                 Provision for Income Taxes     11872.0     10481.0      9680.0     14527.0     19300.0     16741.0  Income Statement
1300                     Net Income After Taxes     61031.0     55256.0     57411.0     94680.0     99803.0     96995.0  Income Statement
1340             Net Income Before Extra. Items     61031.0     55256.0     57411.0     94680.0     99803.0     96995.0  Income Statement
1400                                 Net Income     59531.0     55256.0     57411.0     94680.0     99803.0     96995.0  Income Statement
1470      Income Available to Com Excl ExtraOrd     61031.0     55256.0     57411.0     94680.0     99803.0     96995.0  Income Statement
1480      Income Available to Com Incl ExtraOrd     59531.0     55256.0     57411.0     94680.0     99803.0     96995.0  Income Statement
1530                         Diluted Net Income     59531.0     55256.0     57411.0     94680.0     99803.0     96995.0  Income Statement
1540            Diluted Weighted Average Shares   20000.436   18595.652   17528.214   16864.919   16325.819   15812.547  Income Statement
1550       Diluted EPS Excluding ExtraOrd Items     3.05148     2.97145     3.27535     5.61402      6.1132     6.13405  Income Statement
1570           DPS - Common Stock Primary Issue        0.68        0.75       0.795        0.85         0.9        0.94  Income Statement
1770                     Diluted Normalized EPS     3.05148     2.97145     3.27535     5.61402      6.1132     6.13405  Income Statement

# get earnings per share, appl.eps_ttm will pull trailing twelve months eps
aapl.eps_ttm

           report_type period     eps
as_of_date
2017-06-30         TTM    12M   8.870
2017-09-30         TTM    12M   9.270
2017-12-31         TTM    12M   9.810
2018-03-31         TTM    12M  10.460
2018-06-30         TTM    12M  11.160
2018-09-30         TTM    12M  12.010
2018-12-31         TTM    12M  12.310
2019-03-31         TTM    12M  12.020
2019-06-30         TTM    12M  11.860
2019-09-30         TTM    12M  11.970
2019-12-31         TTM    12M  12.790
2020-03-31         TTM    12M  12.900
2020-06-30         TTM    12M   3.325
2020-09-30         TTM    12M   3.310
2020-12-31         TTM    12M   3.750
2021-03-31         TTM    12M   4.510
2021-06-30         TTM    12M   5.170
2021-09-30         TTM    12M   5.670
2021-12-31         TTM    12M   6.080
2022-03-31         TTM    12M   6.210
2022-06-30         TTM    12M   6.110
2022-09-30         TTM    12M   6.150
2022-12-31         TTM    12M   5.930
2023-03-31         TTM    12M   5.920
2023-06-30         TTM    12M   5.980
2023-09-30         TTM    12M   6.160
2023-12-31         TTM    12M   6.460
2024-03-31         TTM    12M   6.460

# get data in json format

from ib_fundamental.utils import to_json

# CompanyFinancials.data property contains all data in dataclass format
to_json(aapl.data.eps_ttm)
'[{"as_of_date": "2024-03-31T00:00:00", "report_type": "TTM", "period": "12M", "eps": 6.46}, {"as_of_date": "2023-12-31T00:00:00", "report_type": "TTM", "period": "12M", "eps": 6.46}, ...'

# and much more
```

## What fundamental data is available?

`ib_fundamental` is a wrapper around IBKR TWS API. It will connect to a running TWS or
ibgateway instance and request fundamental data through
[reqFundamentalData][reqFundamental] method and ticker `258`. TWS API will return a set of XML
files with all the fundamental data. `ib_fundamental` will parse and transform
all those XMLs into python dataclasses and pandas data frames.

Available data includes:

- Financial Statements
  - Balance sheet, annual/quarter
  - Income Statement, annual/quarter
  - Cash flow, annual/quarter
- Financial ratios
  - earnings per share, quarterly and trailing twelve months (ttm)
  - revenue, quarterly and trailing twelve months(ttm)
  - dividends and dividends per share,  quarterly and trailing twelve months(ttm)
  - financial ratios like ROE, ROC, EV, BVPS, CSHPS, etc
  - full list of [financial ratios][fin_ratios]
  - analyst forecast
  - forward year estimates and actuals
- Company ownership

This is the full list of methods of `CompanyFinancials` class

- analyst_forecast
- balance_annual
- balance_quarter
- cashflow_annual
- cashflow_quarter
- company_information
- dividends
- dividends_ps_q
- dividends_ps_ttm
- eps_q
- eps_ttm
- fundamental_ratios
- fy_actuals
- fy_estimates
- income_annual
- income_quarter
- ownership
- ratios
- revenue_q
- revenue_tt

You can use `FundamentalData` class that will return company fundamental
information in `dataclass` format. Each instance of `CompanyFinancials`
contains an instance of `FundamentalData` in its `data` property.

```python
from ib_fundamental.fundamental import FundamentalData

[_m for _m in dir(FundamentalData) if _m[:1] != "_"]

['analyst_forecast',
 'balance_annual',
 'balance_quarter',
 'cashflow_annual',
 'cashflow_quarter',
 'company_info',
 'div_ps_q',
 'div_ps_ttm',
 'dividend',
 'dividend_summary',
 'eps_q',
 'eps_ttm',
 'fundamental_ratios',
 'fy_actuals',
 'fy_estimates',
 'income_annual',
 'income_quarter',
 'ownership_report',
 'ratios',
 'revenue_q',
 'revenue_ttm']

# get quarterly revenue
aapl.data.revenue_q

[Revenue(as_of_date=datetime.datetime(2024, 3, 31, 0, 0), report_type='R', period='3M', revenue=90753000000.0),
 Revenue(as_of_date=datetime.datetime(2023, 12, 31, 0, 0), report_type='R', period='3M', revenue=119575000000.0),
 Revenue(as_of_date=datetime.datetime(2023, 9, 30, 0, 0), report_type='R', period='3M', revenue=89498000000.0),
 Revenue(as_of_date=datetime.datetime(2023, 6, 30, 0, 0), report_type='R', period='3M', revenue=81797000000.0),
 Revenue(as_of_date=datetime.datetime(2023, 3, 31, 0, 0), report_type='R', period='3M', revenue=94836000000.0),
 Revenue(as_of_date=datetime.datetime(2022, 12, 31, 0, 0), report_type='R', period='3M', revenue=117154000000.0),
 Revenue(as_of_date=datetime.datetime(2022, 9, 30, 0, 0), report_type='R', period='3M', revenue=90146000000.0),
 Revenue(as_of_date=datetime.datetime(2022, 6, 30, 0, 0), report_type='R', period='3M', revenue=82959000000.0),
 Revenue(as_of_date=datetime.datetime(2022, 3, 31, 0, 0), report_type='R', period='3M', revenue=97278000000.0),
 Revenue(as_of_date=datetime.datetime(2021, 12, 31, 0, 0), report_type='R', period='3M', revenue=123945000000.0),
 Revenue(as_of_date=datetime.datetime(2021, 9, 30, 0, 0), report_type='R', period='3M', revenue=83360000000.0),
 Revenue(as_of_date=datetime.datetime(2021, 6, 30, 0, 0), report_type='R', period='3M', revenue=81434000000.0),
 Revenue(as_of_date=datetime.datetime(2021, 3, 31, 0, 0), report_type='R', period='3M', revenue=89584000000.0),
 Revenue(as_of_date=datetime.datetime(2020, 12, 31, 0, 0), report_type='R', period='3M', revenue=111439000000.0),
 Revenue(as_of_date=datetime.datetime(2020, 9, 30, 0, 0), report_type='R', period='3M', revenue=64698000000.0),
 Revenue(as_of_date=datetime.datetime(2020, 6, 30, 0, 0), report_type='R', period='3M', revenue=59685000000.0),
 Revenue(as_of_date=datetime.datetime(2020, 3, 31, 0, 0), report_type='R', period='3M', revenue=58313000000.0),
 Revenue(as_of_date=datetime.datetime(2019, 12, 31, 0, 0), report_type='R', period='3M', revenue=91819000000.0),
 Revenue(as_of_date=datetime.datetime(2019, 9, 30, 0, 0), report_type='R', period='3M', revenue=64040000000.0),
 Revenue(as_of_date=datetime.datetime(2019, 6, 30, 0, 0), report_type='R', period='3M', revenue=53809000000.0),
 Revenue(as_of_date=datetime.datetime(2019, 3, 31, 0, 0), report_type='R', period='3M', revenue=58015000000.0),
 Revenue(as_of_date=datetime.datetime(2018, 12, 31, 0, 0), report_type='R', period='3M', revenue=84310000000.0),
 Revenue(as_of_date=datetime.datetime(2018, 9, 30, 0, 0), report_type='R', period='3M', revenue=62900000000.0),
 Revenue(as_of_date=datetime.datetime(2018, 6, 30, 0, 0), report_type='R', period='3M', revenue=53265000000.0),
 Revenue(as_of_date=datetime.datetime(2018, 3, 31, 0, 0), report_type='R', period='3M', revenue=61137000000.0),
 Revenue(as_of_date=datetime.datetime(2017, 12, 31, 0, 0), report_type='R', period='3M', revenue=88293000000.0),
 Revenue(as_of_date=datetime.datetime(2017, 9, 30, 0, 0), report_type='R', period='3M', revenue=52579000000.0),
 Revenue(as_of_date=datetime.datetime(2017, 6, 30, 0, 0), report_type='R', period='3M', revenue=45408000000.0)]

````

## Contributing

If you find a bug please open an issue, pull requests are always welcome.

To develop with `ib_fundamental` please follow these steps

```bash
git clone https://github.com/quantbelt/ib_fundamental.git
cd ib_fundamental
# install development dependencies
pip install .[dev]
# do your things
# run linters and code quality checks
pre-commit
# run tests with tox, requires pypy310,py{310,311,312}
tox
```

[reqFundamental]: https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqFundamentalData
[fin_ratios]: http://web.archive.org/web/20200725010343/https://interactivebrokers.github.io/tws-api/fundamental_ratios_tags.html
