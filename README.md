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
import ib_async
from ib_fundamental import CompanyFundamental

# connect to TWS API on localhost:7497
ib = ib_async.IB().connect('localhost',7497)
aapl = CompanyFundamental(symbol="AAPL",ib=ib)
aapl.company_info
```
