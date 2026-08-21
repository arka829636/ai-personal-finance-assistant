import pandas as pd

from src.database import get_connection
from src.llm_client import ask_llm


def get_financial_data():
    """Load transaction data from the SQLite database."""
    connection = get_connection()

    query = """
        SELECT
            id,
            type,
            category,
            description,
            amount
        FROM transactions
    """

    try:
        df = pd.read_sql_query(query, connection)
    finally:
        connection.close()

    return df


def build_financial_summary(df):
    """Create a compact financial summary for the LLM."""
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

    income = float(
        df.loc[df["type"].str.lower() == "income", "amount"].sum()
    )

    expense_df = df[
        df["type"].astype(str).str.lower() == "expense"
    ].copy()

    expenses = float(expense_df["amount"].sum())
    savings = income - expenses

    savings_rate = (
        (savings / income) * 100
        if income > 0
        else 0.0
    )

    if not expense_df.empty:
        category_spending = (
            expense_df
            .groupby("category")["amount"]
            .sum()
            .sort_values(ascending=False)
        )

        highest_category = str(category_spending.index[0])
        highest_category_amount = float(category_spending.iloc[0])

        category_dict = {
            str(category): float(amount)
            for category, amount in category_spending.items()
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


def answer_rule_based(question, df):
    """
    Handle common financial questions locally.

    This keeps deterministic answers for known intents and avoids
    unnecessary LLM calls.
    """
    text = question.lower().strip()

    if df.empty:
        return "There is no financial transaction data available."

    summary = build_financial_summary(df)

    # Total income
    if (
        "total income" in text
        or "how much did i earn" in text
        or "how much did i make" in text
        or "my income" in text
    ):
        return f"Your total income is ₹{summary['income']:,.2f}."

    # Total expenses
    if (
        "total expense" in text
        or "total spending" in text
        or "how much did i spend" in text
        or "how much have i spent" in text
    ):
        return f"Your total expenses are ₹{summary['expenses']:,.2f}."

    # Savings
    if (
        "how much did i save" in text
        or "my savings" in text
        or "how much have i saved" in text
    ):
        return f"Your current savings are ₹{summary['savings']:,.2f}."

    # Savings rate
    if (
        "savings rate" in text
        or "saving rate" in text
    ):
        return (
            f"Your savings rate is "
            f"{summary['savings_rate']:.2f}%."
        )

    # Highest spending category
    if (
        "highest spending category" in text
        or "biggest spending category" in text
        or "most money" in text
    ):
        return (
            f"Your highest spending category is "
            f"{summary['highest_category']} with "
            f"₹{summary['highest_category_amount']:,.2f} spent."
        )

    # Category-specific spending
    for category, amount in summary["category_spending"].items():
        if category.lower() in text and (
            "spend" in text
            or "spent" in text
            or "expense" in text
        ):
            return (
                f"You spent ₹{amount:,.2f} on "
                f"{category}."
            )

    return None


def build_llm_prompt(question, summary):
    """Create a restricted prompt using aggregated financial data."""
    category_lines = "\n".join(
        f"- {category}: ₹{amount:,.2f}"
        for category, amount in summary["category_spending"].items()
    )

    return f"""
You are a personal finance assistant for a portfolio application.

Answer the user's question using ONLY the financial summary supplied below.
Do not invent transactions, amounts, dates, accounts, or financial facts.

Important:
- This is a financial analytics application, not a licensed financial advisor.
- Do not recommend specific stocks, securities, loans, or other regulated
  financial products.
- If the information needed to answer the question is not available,
  clearly say that it is not available.
- Keep the answer concise and easy to understand.
- Use Indian Rupee formatting when discussing amounts.

FINANCIAL SUMMARY
-----------------
Total income: ₹{summary["income"]:,.2f}
Total expenses: ₹{summary["expenses"]:,.2f}
Savings: ₹{summary["savings"]:,.2f}
Savings rate: {summary["savings_rate"]:.2f}%
Highest spending category: {summary["highest_category"]}
Highest category spending: ₹{summary["highest_category_amount"]:,.2f}

Spending by category:
{category_lines if category_lines else "- No expense categories available"}

USER QUESTION
-------------
{question}
""".strip()


def answer_question(question):
    """
    Answer a finance question.

    1. Try deterministic local rules first.
    2. For unsupported questions, send a compact financial summary
       to the LLM/mock layer.
    """
    if not question or not question.strip():
        return "Please enter a financial question."

    df = get_financial_data()

    local_answer = answer_rule_based(question, df)

    if local_answer is not None:
        return local_answer

    summary = build_financial_summary(df)
    prompt = build_llm_prompt(question, summary)

    return ask_llm(prompt)


def run_chat():
    """Terminal-based finance chat."""
    print("\n" + "=" * 45)
    print("        💬 FINANCE CHAT ASSISTANT")
    print("=" * 45)
    print("Ask a question about your stored financial data.")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("You: ").strip()

        if question.lower() in {"exit", "quit"}:
            print("Finance Chat closed.")
            break

        try:
            answer = answer_question(question)
            print(f"\nAssistant: {answer}\n")
        except Exception as exc:
            print(
                "\nAssistant: Sorry, I couldn't process that "
                "question."
            )
            print(f"Technical error: {type(exc).__name__}\n")


if __name__ == "__main__":
    run_chat()
