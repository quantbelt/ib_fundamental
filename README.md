# IB Fundamental

Interactive Brokers Fundamental data for humans.

## Setup

### Installation

You can install ib_fundamental using pip

```bash
pip install ib_fundamental
```

## Usage


```python
from ib_fundamental import CompanyFundamental

# connect to TWS API on localhost:7497
aapl = CompanyFundamental(symbol="AAPL")
aapl.company_info
```
