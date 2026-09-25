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


def fetch_corporate_actions(symbol):
    """
    Fetch corporate actions for a given symbol from NSE.

    Example:
        symbol = "RELIANCE"
    """

    columns = [
        "symbol",
        "ex_date",
        "action_type",
        "action_detail",
        "record_date",
        "source"
    ]

    try:

        session = create_nse_session()

        url = "https://www.nseindia.com/api/corporates-corporateActions"

        params = {
            "index": "equities",
            "symbol": symbol
        }

        response = session.get(
            url,
            params=params,
            timeout=30
        )

        print("Status Code:", response.status_code)
        print("Final URL:", response.url)
        print("Content-Type:", response.headers.get("Content-Type"))
        print("Response Preview:", response.text[:500])

        response.raise_for_status()

        data = response.json()

        if not data:
            print("No corporate actions found.")
            return pd.DataFrame(columns=columns)

        df = pd.DataFrame(data)

        # Rename NSE fields to our standard format
        df = df.rename(columns={
            "symbol": "symbol",
            "exDate": "ex_date",
            "subject": "action_detail",
            "recDate": "record_date"
        })

        # Add action_type
        df["action_type"] = df["action_detail"].apply(
            extract_action_type
        )

        # Add source
        df["source"] = "NSE"

        # Keep only required columns
        df = df[columns]

        # Convert date columns
        df["ex_date"] = pd.to_datetime(
            df["ex_date"],
            errors="coerce"
        )

        df["record_date"] = pd.to_datetime(
            df["record_date"],
            errors="coerce"
        )

        return df

    except Exception as e:

        print(f"Error fetching corporate actions: {e}")

        return pd.DataFrame(columns=columns)


def extract_action_type(action_detail):
    """
    Extract a simple action type from NSE's subject field.
    """

    if pd.isna(action_detail):
        return ""

    action_detail = str(action_detail).upper()

    if "DIVIDEND" in action_detail:
        return "DIVIDEND"

    if "BONUS" in action_detail:
        return "BONUS"

    if "SPLIT" in action_detail:
        return "SPLIT"

    if "RIGHT" in action_detail:
        return "RIGHTS"

    if "BUYBACK" in action_detail:
        return "BUYBACK"

    if "MERGER" in action_detail:
        return "MERGER"

    return "OTHER"


def save_corporate_actions(df, file_path):
    """
    Save corporate actions DataFrame to CSV.
    """

    try:

        df.to_csv(
            file_path,
            index=False
        )

        print(
            f"Corporate actions saved successfully to: {file_path}"
        )

    except Exception as e:

        print(f"Error saving corporate actions: {e}")


if __name__ == "__main__":

    df = fetch_corporate_actions(
        symbol="RELIANCE"
    )

    print("\nCorporate Actions:\n")
    print(df.to_string(index=False))

    print("\nData Types:\n")
    print(df.dtypes)

    file_path = "data/corporate/RELIANCE_actions.csv"

    save_corporate_actions(
        df,
        file_path
    )