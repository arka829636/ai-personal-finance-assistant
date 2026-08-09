import pandas as pd
import sqlite3
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


DB_PATH = "data/finance.db"


def get_expense_data():
    connection = sqlite3.connect(DB_PATH)

    query = """
    SELECT date, amount
    FROM transactions
    WHERE type = 'Expense'
    ORDER BY date
    """

    df = pd.read_sql_query(query, connection)

    connection.close()

    return df


def prepare_dataset(df):

    df["date"] = pd.to_datetime(df["date"])
    df["amount"] = pd.to_numeric(df["amount"])

    df["day_of_week"] = df["date"].dt.dayofweek
    df["day_of_month"] = df["date"].dt.day
    df["month"] = df["date"].dt.month

    df["previous_day_expense"] = df["amount"].shift(1)

    df["previous_7_day_expense"] = (
        df["amount"].rolling(7).sum().shift(1)
    )

    df["rolling_7_day_avg"] = (
        df["amount"].rolling(7).mean().shift(1)
    )

    df = df.dropna().reset_index(drop=True)

    return df


def train_model(df):

    features = [
        "day_of_week",
        "day_of_month",
        "month",
        "previous_day_expense",
        "previous_7_day_expense",
        "rolling_7_day_avg"
    ]

    X = df[features]
    y = df["amount"]

    split_index = int(len(df) * 0.8)

    X_train = X.iloc[:split_index]
    X_test = X.iloc[split_index:]

    y_train = y.iloc[:split_index]
    y_test = y.iloc[split_index:]

    model = RandomForestRegressor(
        n_estimators=200,
        random_state=42,
        max_depth=8
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)

    rmse = mean_squared_error(
        y_test,
        predictions
    ) ** 0.5

    r2 = r2_score(y_test, predictions)

    return model, mae, rmse, r2


def predict_next_day(model, df):

    last_date = df["date"].max()

    next_date = last_date + pd.Timedelta(days=1)

    features = pd.DataFrame({
        "day_of_week": [next_date.dayofweek],

        "day_of_month": [next_date.day],

        "month": [next_date.month],

        "previous_day_expense": [
            df["amount"].iloc[-1]
        ],

        "previous_7_day_expense": [
            df["amount"].tail(7).sum()
        ],

        "rolling_7_day_avg": [
            df["amount"].tail(7).mean()
        ]
    })

    prediction = model.predict(features)[0]

    return next_date, prediction


def get_prediction():

    df = get_expense_data()

    if df.empty or len(df) < 10:
        return None

    df = prepare_dataset(df)

    if len(df) < 10:
        return None

    model, mae, rmse, r2 = train_model(df)

    next_date, prediction = predict_next_day(
        model,
        df
    )

    return {
        "date": next_date,
        "prediction": prediction,
        "mae": mae,
        "rmse": rmse,
        "r2": r2
    }


if __name__ == "__main__":

    result = get_prediction()

    if result:

        print("\n========================================")
        print("       ML EXPENSE PREDICTION")
        print("========================================")

        print(
            f"\nPrediction date: "
            f"{result['date'].date()}"
        )

        print(
            f"Predicted expense: "
            f"₹{result['prediction']:,.2f}"
        )

        print(
            f"MAE: ₹{result['mae']:,.2f}"
        )

        print(
            f"RMSE: ₹{result['rmse']:,.2f}"
        )

        print(
            f"R²: {result['r2']:.4f}"
        )

    else:

        print("Not enough expense data.")