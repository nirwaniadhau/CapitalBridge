# NSE Data Connectors

Implemented three NSE data connectors for PyCapital:

- **F&O Data** – Fetches historical futures/options contract data.
- **Corporate Actions** – Fetches dividends, bonuses, splits, rights, buybacks, etc.
- **Indices** – Fetches historical OHLC and volume data for NSE indices such as NIFTY 50.

## Files

```text
connectors/
├── fno.py
├── corporate.py
└── indices.py

data/
├── fno/
├── corporate/
└── indices/

tests/
├── test_fno.py
├── test_corporate.py
└── test_indices.py
NSE APIs Used
Data	Endpoint
F&O	https://www.nseindia.com/api/historicalOR/foCPV
Corporate Actions	https://www.nseindia.com/api/corporates-corporateActions
Indices	https://www.nseindia.com/api/historicalOR/indicesHistory

All requests use an NSE requests.Session() with browser-like headers and session warm-up.

Standardized DataFrames
F&O
date, symbol, expiry_date, option_type, strike_price,
open, high, low, close, volume, open_interest, source

Source: NSE_FO

Corporate Actions
symbol, ex_date, action_type, action_detail, record_date, source

Source: NSE

Indices
date, index_name, open, high, low, close, volume, source

Source: NSE

All CSV files are saved with index=False. Dates are converted to datetime, prices to float64, and volume/open-interest fields to int64.

Example Usage
from connectors.fno import fetch_fno_data
from connectors.corporate import fetch_corporate_actions
from connectors.indices import fetch_index_history

fno = fetch_fno_data(
    "RELIANCE", "FUTSTK",
    "23-08-2026", "23-09-2026",
    "29-SEP-2026"
)

actions = fetch_corporate_actions("RELIANCE")

indices = fetch_index_history(
    "NIFTY 50",
    "18-09-2026",
    "25-09-2026"
)
Testing

Run the connector tests with:

pytest tests/test_fno.py tests/test_corporate.py tests/test_indices.py -v

Each connector returns an empty DataFrame with the correct columns if the NSE request fails or no data is available.


**That's the one I'd use.** It is short enough that your teammates will actually read it, but it tells them exactly