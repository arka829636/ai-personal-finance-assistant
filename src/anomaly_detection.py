import sqlite3
import pandas as pd
from sklearn.ensemble import IsolationForest


DB_PATH = "data/finance.db"


# ============================================================
# LOAD EXPENSE DATA
# ============================================================

def get_expense_data():

    connection = sqlite3.connect(DB_PATH)

    query = """
        SELECT
            id,
            date,
            category,
            description,
            amount,
            payment_method
        FROM transactions
        WHERE type = 'Expense'
        ORDER BY date
    """

    df = pd.read_sql_query(
        query,
        connection
    )

    connection.close()

    return df


# ============================================================
# DETECT ANOMALIES
# ============================================================

def detect_anomalies():

    df = get_expense_data()

    if df.empty:
        return None

    if len(df) < 10:
        return None

    # Make sure amount is numeric
    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce"
    )

    # Remove invalid amounts
    df = df.dropna(
        subset=["amount"]
    ).copy()

    if len(df) < 10:
        return None

    # --------------------------------------------------------
    # ISOLATION FOREST
    # --------------------------------------------------------

    model = IsolationForest(
        contamination=0.05,
        random_state=42
    )

    # Train using transaction amount
    model.fit(
        df[["amount"]]
    )

    # Prediction:
    # 1  = Normal
    # -1 = Anomaly

    df["anomaly_prediction"] = model.predict(
        df[["amount"]]
    )

    # Anomaly score
    df["anomaly_score"] = model.decision_function(
        df[["amount"]]
    )

    # Human-readable label

    df["status"] = df[
        "anomaly_prediction"
    ].apply(
        lambda x:
        "🚨 Anomaly"
        if x == -1
        else "✅ Normal"
    )

    return df


# ============================================================
# GET ONLY ANOMALIES
# ============================================================

def get_anomalies():

    df = detect_anomalies()

    if df is None:
        return None

    anomalies = df[
        df["anomaly_prediction"] == -1
    ].copy()

    return anomalies


# ============================================================
# MAIN TEST
# ============================================================

if __name__ == "__main__":

    print("\n========================================")
    print("       SPENDING ANOMALY DETECTION")
    print("========================================")

    df = detect_anomalies()

    if df is None:

        print(
            "\nNot enough expense data "
            "for anomaly detection."
        )

    else:

        print(
            f"\nTotal expense transactions: "
            f"{len(df)}"
        )

        anomalies = df[
            df["anomaly_prediction"] == -1
        ]

        print(
            f"Anomalies detected: "
            f"{len(anomalies)}"
        )

        print("\n----------------------------------------")
        print("ALL TRANSACTIONS")
        print("----------------------------------------")

        print(
            df[
                [
                    "date",
                    "category",
                    "amount",
                    "status"
                ]
            ].to_string(
                index=False
            )
        )

        print("\n----------------------------------------")
        print("ANOMALIES")
        print("----------------------------------------")

        if anomalies.empty:

            print(
                "No unusual transactions detected."
            )

        else:

            print(
                anomalies[
                    [
                        "date",
                        "category",
                        "description",
                        "amount",
                        "anomaly_score",
                        "status"
                    ]
                ].to_string(
                    index=False
                )
            )

    print("\n========================================")
    print("       ANALYSIS COMPLETE")
    print("========================================")