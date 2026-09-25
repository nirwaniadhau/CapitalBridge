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

from connectors.fno import fetch_fno_data


def test_fno_data():

    df = fetch_fno_data(
        symbol="RELIANCE",
        instrument_type="FUTSTK",
        from_date="23-08-2026",
        to_date="23-09-2026",
        expiry_date="29-SEP-2026"
    )

    # Check that DataFrame is returned
    assert isinstance(df, pd.DataFrame)

    # Required columns
    expected_columns = [
        "date",
        "symbol",
        "expiry_date",
        "option_type",
        "strike_price",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "open_interest",
        "source"
    ]

    assert list(df.columns) == expected_columns

    # DataFrame should contain data
    assert not df.empty

    # Check date types
    assert pd.api.types.is_datetime64_any_dtype(
        df["date"]
    )

    assert pd.api.types.is_datetime64_any_dtype(
        df["expiry_date"]
    )

    # Check price columns
    price_columns = [
        "strike_price",
        "open",
        "high",
        "low",
        "close"
    ]

    for column in price_columns:
        assert pd.api.types.is_float_dtype(
            df[column]
        )

    # Check integer columns
    assert pd.api.types.is_integer_dtype(
        df["volume"]
    )

    assert pd.api.types.is_integer_dtype(
        df["open_interest"]
    )

    # Check source
    assert (df["source"] == "NSE_FO").all()

    print("\nF&O test passed successfully!")
    print(f"Rows returned: {len(df)}")