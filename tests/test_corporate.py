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

from connectors.corporate import fetch_corporate_actions


def test_corporate_actions():

    df = fetch_corporate_actions(
        symbol="RELIANCE"
    )

    # Check DataFrame
    assert isinstance(df, pd.DataFrame)

    # Required columns
    expected_columns = [
        "symbol",
        "ex_date",
        "action_type",
        "action_detail",
        "record_date",
        "source"
    ]

    assert list(df.columns) == expected_columns

    # Data should be returned
    assert not df.empty

    # Date columns
    assert pd.api.types.is_datetime64_any_dtype(
        df["ex_date"]
    )

    assert pd.api.types.is_datetime64_any_dtype(
        df["record_date"]
    )

    # Symbol should match requested symbol
    assert (df["symbol"] == "RELIANCE").all()

    # Source should be NSE
    assert (df["source"] == "NSE").all()

    print("\nCorporate Actions test passed successfully!")
    print(f"Rows returned: {len(df)}")