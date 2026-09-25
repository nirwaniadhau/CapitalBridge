import requests
import pandas as pd
import time


def create_nse_session():
    """
    Create and warm up an NSE session.
    """

    session = requests.Session()

    session.headers.update({
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Referer": "https://www.nseindia.com",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "Connection": "keep-alive"
    })

    # Warm up NSE session
    session.get(
        "https://www.nseindia.com",
        timeout=15
    )

    time.sleep(3)

    return session


def fetch_fno_data(
    symbol,
    instrument_type,
    from_date,
    to_date,
    expiry_date
):
    """
    Fetch historical F&O data from NSE.

    Example:
        symbol = "RELIANCE"
        instrument_type = "FUTSTK"
        from_date = "23-08-2026"
        to_date = "23-09-2026"
        expiry_date = "29-SEP-2026"
    """

    columns = [
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

    try:

        session = create_nse_session()

        url = "https://www.nseindia.com/api/historicalOR/foCPV"

        params = {
            "from": from_date,
            "to": to_date,
            "instrumentType": instrument_type,
            "symbol": symbol,
            "year": expiry_date[-4:],
            "expiryDate": expiry_date
        }

        response = session.get(
            url,
            params=params,
            timeout=30
        )

        # Debug information
        print("Status Code:", response.status_code)
        print("Final URL:", response.url)
        print("Content-Type:", response.headers.get("Content-Type"))
        print("Response Preview:", response.text[:500])

        response.raise_for_status()

        data = response.json().get("data", [])

        if not data:
            print("No F&O data found.")
            return pd.DataFrame(columns=columns)

        df = pd.DataFrame(data)

        # Rename NSE fields to our standard format
        df = df.rename(columns={
            "FH_TIMESTAMP": "date",
            "FH_SYMBOL": "symbol",
            "FH_EXPIRY_DT": "expiry_date",
            "FH_OPTION_TYPE": "option_type",
            "FH_STRIKE_PRICE": "strike_price",
            "FH_OPENING_PRICE": "open",
            "FH_TRADE_HIGH_PRICE": "high",
            "FH_TRADE_LOW_PRICE": "low",
            "FH_CLOSING_PRICE": "close",
            "FH_TOT_TRADED_QTY": "volume",
            "FH_OPEN_INT": "open_interest"
        })

        # Add source
        df["source"] = "NSE_FO"

        # Keep only required columns
        df = df[columns]

        # Convert date columns
        df["date"] = pd.to_datetime(
            df["date"],
            errors="coerce"
        )

        df["expiry_date"] = pd.to_datetime(
            df["expiry_date"],
            errors="coerce"
        )

        # Convert price columns to float64
        price_columns = [
            "strike_price",
            "open",
            "high",
            "low",
            "close"
        ]

        for column in price_columns:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            ).astype("float64")

        # Convert volume to int64
        df["volume"] = pd.to_numeric(
            df["volume"],
            errors="coerce"
        ).fillna(0).astype("int64")

        # Convert open interest to int64
        df["open_interest"] = pd.to_numeric(
            df["open_interest"],
            errors="coerce"
        ).fillna(0).astype("int64")

        return df

    except Exception as e:

        print(f"Error fetching F&O data: {e}")

        return pd.DataFrame(columns=columns)
    
def save_fno_data(df, file_path):
    """
    Save F&O DataFrame to CSV.
    """

    try:
        df.to_csv(file_path, index=False)
        print(f"F&O data saved successfully to: {file_path}")

    except Exception as e:
        print(f"Error saving F&O data: {e}")

if __name__ == "__main__":

    df = fetch_fno_data(
        symbol="RELIANCE",
        instrument_type="FUTSTK",
        from_date="23-08-2026",
        to_date="23-09-2026",
        expiry_date="29-SEP-2026"
    )

    print("\nF&O Data:\n")
    print(df.to_string(index=False))

    print("\nData Types:\n")
    print(df.dtypes)

    # Save F&O data to CSV
    file_path = "data/fno/23092026_fno_bhavcopy.csv"

    save_fno_data(df, file_path)