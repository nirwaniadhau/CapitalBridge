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


def fetch_index_history(index_name, from_date, to_date):
    """
    Fetch historical index data from NSE.

    Example:
        index_name = "NIFTY 50"
        from_date = "18-09-2026"
        to_date = "25-09-2026"
    """

    columns = [
        "date",
        "index_name",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "source"
    ]

    try:

        session = create_nse_session()

        url = "https://www.nseindia.com/api/historicalOR/indicesHistory"

        params = {
            "indexType": index_name,
            "from": from_date,
            "to": to_date
        }

        response = session.get(
            url,
            params=params,
            timeout=30
        )

        print("Status Code:", response.status_code)
        print("Final URL:", response.url)
        print("Content-Type:", response.headers.get("Content-Type"))

        response.raise_for_status()

        data = response.json().get("data", [])

        if not data:
            print("No index data found.")
            return pd.DataFrame(columns=columns)

        df = pd.DataFrame(data)

        # Rename NSE fields to our standard format
        df = df.rename(columns={
            "EOD_TIMESTAMP": "date",
            "EOD_INDEX_NAME": "index_name",
            "EOD_OPEN_INDEX_VAL": "open",
            "EOD_HIGH_INDEX_VAL": "high",
            "EOD_LOW_INDEX_VAL": "low",
            "EOD_CLOSE_INDEX_VAL": "close",
            "HIT_TRADED_QTY": "volume"
        })

        # Add source
        df["source"] = "NSE"

        # Keep only required columns
        df = df[columns]

        # Convert date
        df["date"] = pd.to_datetime(
            df["date"],
            format="%d-%b-%Y",
            errors="coerce"
        )

        # Convert price columns to float64
        price_columns = [
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

        return df

    except Exception as e:

        print(f"Error fetching index data: {e}")

        return pd.DataFrame(columns=columns)


def save_index_data(df, file_path):
    """
    Save index DataFrame to CSV.
    """

    try:

        df.to_csv(
            file_path,
            index=False
        )

        print(
            f"Index data saved successfully to: {file_path}"
        )

    except Exception as e:

        print(f"Error saving index data: {e}")


if __name__ == "__main__":

    df = fetch_index_history(
        index_name="NIFTY 50",
        from_date="18-09-2026",
        to_date="25-09-2026"
    )

    print("\nIndex Data:\n")
    print(df.to_string(index=False))

    print("\nData Types:\n")
    print(df.dtypes)

    file_path = "data/indices/NIFTY50_20260918_20260925.csv"

    save_index_data(
        df,
        file_path
    )