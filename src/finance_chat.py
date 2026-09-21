import pandas as pd

from src.database import get_connection
from src.llm_client import ask_llm
from src.ml_expense_prediction import get_prediction
from src.anomaly_detection import get_anomalies


# ============================================================
# LOAD FINANCIAL DATA
# ============================================================

def get_financial_data():
    """Load transaction data from SQLite."""

    connection = get_connection()

    query = """
        SELECT
            id,
            type,
            category,
            description,
            amount,
            date
        FROM transactions
    """

    try:
        df = pd.read_sql_query(
            query,
            connection
        )

    finally:
        connection.close()

    return df


# ============================================================
# FINANCIAL SUMMARY
# ============================================================

def build_financial_summary(df):
    """Build an aggregated financial summary."""

    if df.empty:

        return {
            "income": 0.0,
            "expenses": 0.0,
            "savings": 0.0,
            "savings_rate": 0.0,
            "highest_category": "None",
            "highest_category_amount": 0.0,
            "category_spending": {},
        }

    # --------------------------------------------------------
    # INCOME
    # --------------------------------------------------------

    income = float(
        df.loc[
            df["type"].astype(str).str.lower() == "income",
            "amount"
        ].sum()
    )

    # --------------------------------------------------------
    # EXPENSES
    # --------------------------------------------------------

    expense_df = df[
        df["type"].astype(str).str.lower() == "expense"
    ].copy()

    expenses = float(
        expense_df["amount"].sum()
    )

    # --------------------------------------------------------
    # SAVINGS
    # --------------------------------------------------------

    savings = income - expenses

    savings_rate = (
        (savings / income) * 100
        if income > 0
        else 0.0
    )

    # --------------------------------------------------------
    # CATEGORY SPENDING
    # --------------------------------------------------------

    if not expense_df.empty:

        category_spending = (
            expense_df
            .groupby("category")["amount"]
            .sum()
            .sort_values(ascending=False)
        )

        highest_category = str(
            category_spending.index[0]
        )

        highest_category_amount = float(
            category_spending.iloc[0]
        )

        category_dict = {
            str(category): float(amount)
            for category, amount
            in category_spending.items()
        }

    else:

        highest_category = "None"
        highest_category_amount = 0.0
        category_dict = {}

    return {
        "income": income,
        "expenses": expenses,
        "savings": savings,
        "savings_rate": savings_rate,
        "highest_category": highest_category,
        "highest_category_amount": highest_category_amount,
        "category_spending": category_dict,
    }


# ============================================================
# ML INFORMATION
# ============================================================

def get_ml_information():
    """
    Retrieve Random Forest prediction and
    Isolation Forest anomaly information.
    """

    result = {
        "prediction_available": False,
        "predicted_expense": None,
        "prediction_date": None,
        "mae": None,
        "rmse": None,
        "r2": None,

        "anomaly_available": False,
        "anomaly_count": 0,
        "anomalies": [],
    }

    # ========================================================
    # RANDOM FOREST
    # ========================================================

    try:

        prediction_result = get_prediction()

        if prediction_result is not None:

            result["prediction_available"] = True

            result["predicted_expense"] = float(
                prediction_result["prediction"]
            )

            result["prediction_date"] = (
                prediction_result["date"].date()
            )

            result["mae"] = float(
                prediction_result["mae"]
            )

            result["rmse"] = float(
                prediction_result["rmse"]
            )

            result["r2"] = float(
                prediction_result["r2"]
            )

    except Exception:

        pass

    # ========================================================
    # ISOLATION FOREST
    # ========================================================

    try:

        anomalies_df = get_anomalies()

        if anomalies_df is not None:

            result["anomaly_available"] = True

            result["anomaly_count"] = len(
                anomalies_df
            )

            if not anomalies_df.empty:

                for _, row in anomalies_df.iterrows():

                    result["anomalies"].append(
                        {
                            "date": str(
                                row["date"]
                            ),
                            "category": str(
                                row["category"]
                            ),
                            "description": str(
                                row["description"]
                            ),
                            "amount": float(
                                row["amount"]
                            ),
                            "anomaly_score": float(
                                row["anomaly_score"]
                            ),
                        }
                    )

    except Exception:

        pass

    return result


# ============================================================
# INTENT DETECTION
# ============================================================

def detect_intent(question):
    """
    Identify the main intent of a Finance Chat question.

    Possible intents:

        income
        expenses
        savings
        category
        prediction
        anomaly
        comparison
        general
    """

    text = question.lower().strip()

    # ========================================================
    # PREDICTION VS HISTORICAL COMPARISON
    # ========================================================

    if (
        (
            "predicted" in text
            or "prediction" in text
            or "forecast" in text
        )
        and
        (
            "compare" in text
            or "compared" in text
            or "historical" in text
            or "current spending" in text
            or "normal spending" in text
        )
    ):

        return "comparison"

    # ========================================================
    # ANOMALY
    # ========================================================

    if (
        "anomal" in text
        or "unusual spending" in text
        or "unusual transaction" in text
        or "suspicious spending" in text
    ):

        return "anomaly"

    # ========================================================
    # PREDICTION
    # ========================================================

    if (
        "predicted expense" in text
        or "expense prediction" in text
        or "predict my expense" in text
        or "next day expense" in text
        or "next-day expense" in text
        or "forecast expense" in text
        or "predicted spending" in text
    ):

        return "prediction"

    # ========================================================
    # CATEGORY
    #
    # IMPORTANT:
    # Category detection comes before generic expense
    # detection.
    # ========================================================

    categories = [
        "shopping",
        "food",
        "bills",
        "education",
        "healthcare",
        "transport",
        "entertainment",
    ]

    if (
        "category" in text
        or any(
            category in text
            for category in categories
        )
    ):

        if (
            "spend" in text
            or "spent" in text
            or "expense" in text
            or "cost" in text
            or "amount" in text
            or "how much" in text
        ):

            return "category"

    # ========================================================
    # SAVINGS RATE
    # ========================================================

    if (
        "savings rate" in text
        or "saving rate" in text
    ):

        return "savings"

    # ========================================================
    # SAVINGS
    # ========================================================

    if (
        "my savings" in text
        or "how much did i save" in text
        or "how much have i saved" in text
        or "money saved" in text
    ):

        return "savings"

    # ========================================================
    # INCOME
    # ========================================================

    if (
        "total income" in text
        or "my income" in text
        or "how much did i earn" in text
        or "how much did i make" in text
        or "earnings" in text
    ):

        return "income"

    # ========================================================
    # TOTAL EXPENSES
    # ========================================================

    if (
        "total expense" in text
        or "total expenses" in text
        or "total spending" in text
        or "how much did i spend" in text
        or "how much have i spent" in text
    ):

        return "expenses"

    # ========================================================
    # GENERAL
    # ========================================================

    return "general"


# ============================================================
# INTENT-BASED CONTEXT RETRIEVAL
# ============================================================

def retrieve_context(question, df):
    """
    Retrieve only the information relevant to the
    detected intent.
    """

    intent = detect_intent(question)

    # ========================================================
    # INCOME
    # ========================================================

    if intent == "income":

        income = float(
            df.loc[
                df["type"].astype(str).str.lower()
                == "income",
                "amount"
            ].sum()
        )

        return {
            "intent": "income",
            "income": income,
        }

    # ========================================================
    # TOTAL EXPENSES
    # ========================================================

    if intent == "expenses":

        expenses = float(
            df.loc[
                df["type"].astype(str).str.lower()
                == "expense",
                "amount"
            ].sum()
        )

        return {
            "intent": "expenses",
            "expenses": expenses,
        }

    # ========================================================
    # SAVINGS
    # ========================================================

    if intent == "savings":

        income = float(
            df.loc[
                df["type"].astype(str).str.lower()
                == "income",
                "amount"
            ].sum()
        )

        expenses = float(
            df.loc[
                df["type"].astype(str).str.lower()
                == "expense",
                "amount"
            ].sum()
        )

        savings = income - expenses

        savings_rate = (
            (savings / income) * 100
            if income > 0
            else 0.0
        )

        return {
            "intent": "savings",
            "income": income,
            "expenses": expenses,
            "savings": savings,
            "savings_rate": savings_rate,
        }

    # ========================================================
    # CATEGORY
    # ========================================================

    if intent == "category":

        expense_df = df[
            df["type"].astype(str).str.lower()
            == "expense"
        ].copy()

        if expense_df.empty:

            return {
                "intent": "category",
                "categories": {},
            }

        category_spending = (
            expense_df
            .groupby("category")["amount"]
            .sum()
            .sort_values(ascending=False)
        )

        # ----------------------------------------------------
        # Find a specific category mentioned in question
        # ----------------------------------------------------

        question_text = question.lower()

        requested_category = None

        for category in category_spending.index:

            if str(category).lower() in question_text:

                requested_category = str(category)

                break

        # ----------------------------------------------------
        # Specific category
        # ----------------------------------------------------

        if requested_category is not None:

            amount = float(
                category_spending[
                    requested_category
                ]
            )

            return {
                "intent": "category",
                "category": requested_category,
                "amount": amount,
            }

        # ----------------------------------------------------
        # All categories
        # ----------------------------------------------------

        return {
            "intent": "category",
            "categories": {
                str(category): float(amount)
                for category, amount
                in category_spending.items()
            },
        }

    # ========================================================
    # PREDICTION
    # ========================================================

    if intent == "prediction":

        ml = get_ml_information()

        return {
            "intent": "prediction",
            "prediction_available":
                ml["prediction_available"],
            "predicted_expense":
                ml["predicted_expense"],
            "prediction_date":
                ml["prediction_date"],
            "mae":
                ml["mae"],
            "rmse":
                ml["rmse"],
            "r2":
                ml["r2"],
        }

    # ========================================================
    # ANOMALY
    # ========================================================

    if intent == "anomaly":

        ml = get_ml_information()

        return {
            "intent": "anomaly",
            "anomaly_available":
                ml["anomaly_available"],
            "anomaly_count":
                ml["anomaly_count"],
            "anomalies":
                ml["anomalies"],
        }

    # ========================================================
    # COMPARISON
    # ========================================================

    if intent == "comparison":

        ml = get_ml_information()

        expense_df = df[
            df["type"].astype(str).str.lower()
            == "expense"
        ]

        historical_average = (
            float(
                expense_df["amount"].mean()
            )
            if not expense_df.empty
            else 0.0
        )

        predicted_expense = (
            ml["predicted_expense"]
            if ml["prediction_available"]
            else None
        )

        if (
            predicted_expense is not None
            and historical_average > 0
        ):

            difference = (
                predicted_expense
                - historical_average
            )

            percentage_change = (
                difference
                / historical_average
                * 100
            )

        else:

            difference = None
            percentage_change = None

        return {
            "intent": "comparison",
            "prediction_available":
                ml["prediction_available"],
            "predicted_expense":
                predicted_expense,
            "prediction_date":
                ml["prediction_date"],
            "historical_average":
                historical_average,
            "difference":
                difference,
            "percentage_change":
                percentage_change,
        }

    # ========================================================
    # GENERAL
    # ========================================================

    summary = build_financial_summary(df)

    return {
        "intent": "general",
        "summary": summary,
    }


# ============================================================
# RULE-BASED ANSWERS
# ============================================================

def answer_rule_based(question, df):
    """
    Generate deterministic answers using the
    intent-based retrieval system.
    """

    if df.empty:

        return (
            "There is no financial transaction data available."
        )

    context = retrieve_context(
        question,
        df
    )

    intent = context["intent"]

    # ========================================================
    # INCOME
    # ========================================================

    if intent == "income":

        return (
            f"Your total income is "
            f"₹{context['income']:,.2f}."
        )

    # ========================================================
    # EXPENSES
    # ========================================================

    if intent == "expenses":

        return (
            f"Your total expenses are "
            f"₹{context['expenses']:,.2f}."
        )

    # ========================================================
    # SAVINGS
    # ========================================================

    if intent == "savings":

        return (
            f"Your savings are "
            f"₹{context['savings']:,.2f}, "
            f"with a savings rate of "
            f"{context['savings_rate']:.2f}%."
        )

    # ========================================================
    # CATEGORY
    # ========================================================

    if intent == "category":

        if "category" in context:

            return (
                f"You spent "
                f"₹{context['amount']:,.2f} on "
                f"{context['category']}."
            )

        categories = context.get(
            "categories",
            {}
        )

        if not categories:

            return (
                "There is no expense category data available."
            )

        lines = []

        for category, amount in categories.items():

            lines.append(
                f"- {category}: ₹{amount:,.2f}"
            )

        return (
            "Here is your spending by category:\n"
            + "\n".join(lines)
        )

    # ========================================================
    # PREDICTION
    # ========================================================

    if intent == "prediction":

        if not context["prediction_available"]:

            return (
                "Expense prediction is currently "
                "unavailable because there is not "
                "enough valid expense data."
            )

        return (
            f"The predicted expense for "
            f"{context['prediction_date']} is "
            f"₹{context['predicted_expense']:,.2f}."
        )

    # ========================================================
    # ANOMALY
    # ========================================================

    if intent == "anomaly":

        if not context["anomaly_available"]:

            return (
                "Anomaly detection is currently unavailable."
            )

        count = context["anomaly_count"]

        if count == 0:

            return (
                "The Isolation Forest model did not "
                "identify any unusual expense transactions."
            )

        return (
            f"The Isolation Forest model detected "
            f"{count} unusual expense transaction"
            f"{'s' if count != 1 else ''}."
        )

    # ========================================================
    # COMPARISON
    # ========================================================

    if intent == "comparison":

        if not context["prediction_available"]:

            return (
                "Expense prediction is currently unavailable, "
                "so I cannot make the comparison."
            )

        if context["percentage_change"] is None:

            return (
                "There is not enough historical expense data "
                "to make this comparison."
            )

        predicted = context["predicted_expense"]
        historical = context["historical_average"]
        difference = context["difference"]
        percentage = context["percentage_change"]

        if percentage > 0:

            return (
                f"Your predicted expense for "
                f"{context['prediction_date']} is "
                f"₹{predicted:,.2f}, compared with your "
                f"historical average of "
                f"₹{historical:,.2f}. "
                f"The prediction is "
                f"{percentage:.1f}% higher, "
                f"a difference of "
                f"₹{abs(difference):,.2f}."
            )

        if percentage < 0:

            return (
                f"Your predicted expense for "
                f"{context['prediction_date']} is "
                f"₹{predicted:,.2f}, compared with your "
                f"historical average of "
                f"₹{historical:,.2f}. "
                f"The prediction is "
                f"{abs(percentage):.1f}% lower, "
                f"a difference of "
                f"₹{abs(difference):,.2f}."
            )

        return (
            f"Your predicted expense for "
            f"{context['prediction_date']} is "
            f"₹{predicted:,.2f}, which is approximately "
            f"the same as your historical average of "
            f"₹{historical:,.2f}."
        )

    # No deterministic answer
    return None


# ============================================================
# BUILD LLM PROMPT FROM RETRIEVED CONTEXT
# ============================================================

def build_llm_prompt(question, context):
    """
    Build a focused LLM prompt using only the
    context retrieved for the user's intent.
    """

    intent = context["intent"]

    # ========================================================
    # INCOME
    # ========================================================

    if intent == "income":

        data = (
            f"Intent: Income\n"
            f"Total income: ₹{context['income']:,.2f}"
        )

    # ========================================================
    # EXPENSES
    # ========================================================

    elif intent == "expenses":

        data = (
            f"Intent: Total Expenses\n"
            f"Total expenses: ₹{context['expenses']:,.2f}"
        )

    # ========================================================
    # SAVINGS
    # ========================================================

    elif intent == "savings":

        data = (
            f"Intent: Savings\n"
            f"Income: ₹{context['income']:,.2f}\n"
            f"Expenses: ₹{context['expenses']:,.2f}\n"
            f"Savings: ₹{context['savings']:,.2f}\n"
            f"Savings rate: "
            f"{context['savings_rate']:.2f}%"
        )

    # ========================================================
    # CATEGORY
    # ========================================================

    elif intent == "category":

        if "category" in context:

            data = (
                f"Intent: Category Spending\n"
                f"Category: {context['category']}\n"
                f"Amount spent: "
                f"₹{context['amount']:,.2f}"
            )

        else:

            category_lines = "\n".join(
                f"- {category}: ₹{amount:,.2f}"
                for category, amount
                in context.get(
                    "categories",
                    {}
                ).items()
            )

            data = (
                "Intent: Category Spending\n"
                "Spending by category:\n"
                f"{category_lines}"
            )

    # ========================================================
    # PREDICTION
    # ========================================================

    elif intent == "prediction":

        if context["prediction_available"]:

            data = (
                "Intent: Expense Prediction\n"
                f"Predicted expense: "
                f"₹{context['predicted_expense']:,.2f}\n"
                f"Prediction date: "
                f"{context['prediction_date']}\n"
                f"MAE: ₹{context['mae']:,.2f}\n"
                f"RMSE: ₹{context['rmse']:,.2f}\n"
                f"R²: {context['r2']:.3f}"
            )

        else:

            data = (
                "Intent: Expense Prediction\n"
                "Prediction is unavailable."
            )

    # ========================================================
    # ANOMALY
    # ========================================================

    elif intent == "anomaly":

        lines = []

        for anomaly in context.get(
            "anomalies",
            []
        ):

            lines.append(
                f"- {anomaly['date']} | "
                f"{anomaly['category']} | "
                f"{anomaly['description']} | "
                f"₹{anomaly['amount']:,.2f} | "
                f"score {anomaly['anomaly_score']:.4f}"
            )

        data = (
            "Intent: Anomaly Detection\n"
            f"Anomalies detected: "
            f"{context['anomaly_count']}\n"
            + (
                "\n".join(lines)
                if lines
                else "No anomaly details available."
            )
        )

    # ========================================================
    # COMPARISON
    # ========================================================

    elif intent == "comparison":

        if context["prediction_available"]:

            data = (
                "Intent: Prediction Comparison\n"
                f"Predicted expense: "
                f"₹{context['predicted_expense']:,.2f}\n"
                f"Historical average: "
                f"₹{context['historical_average']:,.2f}\n"
                f"Difference: "
                f"₹{context['difference']:,.2f}\n"
                f"Percentage change: "
                f"{context['percentage_change']:.2f}%"
            )

        else:

            data = (
                "Intent: Prediction Comparison\n"
                "Prediction is unavailable."
            )

    # ========================================================
    # GENERAL
    # ========================================================

    else:

        summary = context["summary"]

        category_lines = "\n".join(
            f"- {category}: ₹{amount:,.2f}"
            for category, amount
            in summary[
                "category_spending"
            ].items()
        )

        data = (
            "Intent: General Financial Question\n"
            f"Income: ₹{summary['income']:,.2f}\n"
            f"Expenses: ₹{summary['expenses']:,.2f}\n"
            f"Savings: ₹{summary['savings']:,.2f}\n"
            f"Savings rate: "
            f"{summary['savings_rate']:.2f}%\n"
            f"Highest spending category: "
            f"{summary['highest_category']}\n"
            f"Highest category amount: "
            f"₹{summary['highest_category_amount']:,.2f}\n"
            f"Category spending:\n"
            f"{category_lines}"
        )

    # ========================================================
    # FINAL PROMPT
    # ========================================================

    return f"""
You are FinanceAI, a personal finance assistant
inside a portfolio application.

Answer the user's question using ONLY the retrieved
financial context below.

Do not invent:
- transactions
- amounts
- dates
- predictions
- accounts
- financial facts

If the required information is unavailable,
say so clearly.

Keep the response concise and easy to understand.

Use Indian Rupee formatting.

This application is a financial analytics tool,
not a licensed financial advisor.

Do not recommend specific stocks, securities,
loans, or regulated financial products.

RETRIEVED CONTEXT
-----------------
{data}

USER QUESTION
-------------
{question}
""".strip()


# ============================================================
# MAIN QUESTION HANDLER
# ============================================================

def answer_question(question):
    """
    Main Finance Chat pipeline.

    Flow:

    Question
       ↓
    Intent Detection
       ↓
    Context Retrieval
       ↓
    Rule-Based Answer
       ↓
    If necessary → Mock LLM / Live LLM
    """

    if not question or not question.strip():

        return (
            "Please enter a financial question."
        )

    # --------------------------------------------------------
    # LOAD DATA
    # --------------------------------------------------------

    df = get_financial_data()

    if df.empty:

        return (
            "There is no financial transaction data available."
        )

    # --------------------------------------------------------
    # INTENT-BASED RETRIEVAL
    # --------------------------------------------------------

    context = retrieve_context(
        question,
        df
    )

    # --------------------------------------------------------
    # DETERMINISTIC ANSWER
    # --------------------------------------------------------

    local_answer = answer_rule_based(
        question,
        df
    )

    if local_answer is not None:

        return local_answer

    # --------------------------------------------------------
    # LLM FALLBACK
    # --------------------------------------------------------

    prompt = build_llm_prompt(
        question,
        context
    )

    return ask_llm(
        prompt
    )


# ============================================================
# TERMINAL CHAT
# ============================================================

def run_chat():
    """Run Finance Chat from the terminal."""

    print(
        "\n" + "=" * 45
    )

    print(
        "        💬 FINANCE CHAT ASSISTANT"
    )

    print(
        "=" * 45
    )

    print(
        "Ask a question about your stored "
        "financial data."
    )

    print(
        "Type 'exit' to quit.\n"
    )

    while True:

        question = input(
            "You: "
        ).strip()

        if question.lower() in {
            "exit",
            "quit"
        }:

            print(
                "Finance Chat closed."
            )

            break

        try:

            answer = answer_question(
                question
            )

            print(
                f"\nAssistant: {answer}\n"
            )

        except Exception as exc:

            print(
                "\nAssistant: Sorry, I couldn't "
                "process that question."
            )

            print(
                f"Technical error: "
                f"{type(exc).__name__}\n"
            )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    run_chat()