import sys
import os

import pandas as pd


# Add project root to Python path
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from connectors.indices import fetch_index_history


def test_index_history():

    df = fetch_index_history(
        index_name="NIFTY 50",
        from_date="18-09-2026",
        to_date="25-09-2026"
    )

    # Check DataFrame
    assert isinstance(df, pd.DataFrame)

    # Required columns
    expected_columns = [
        "date",
        "index_name",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "source"
    ]

    assert list(df.columns) == expected_columns

    # Data should be returned
    assert not df.empty

    # Date type
    assert pd.api.types.is_datetime64_any_dtype(
        df["date"]
    )

    # Price columns should be float
    price_columns = [
        "open",
        "high",
        "low",
        "close"
    ]

    for column in price_columns:
        assert pd.api.types.is_float_dtype(
            df[column]
        )

    # Volume should be integer
    assert pd.api.types.is_integer_dtype(
        df["volume"]
    )

    # Index name
    assert (df["index_name"] == "NIFTY 50").all()

    # Source
    assert (df["source"] == "NSE").all()

    print("\nIndex test passed successfully!")
    print(f"Rows returned: {len(df)}")