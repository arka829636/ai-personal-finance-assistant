import re

from openai import OpenAI

from src.config import OPENAI_API_KEY, OPENAI_MODEL, MOCK_LLM


def _money(prompt: str, label: str) -> float:
    """Extract a financial amount from the prepared summary."""
    pattern = rf"{re.escape(label)}:\s*₹(-?[\d,]+(?:\.\d+)?)"
    match = re.search(pattern, prompt)

    if not match:
        return 0.0

    return float(match.group(1).replace(",", ""))


def _percent(prompt: str, label: str) -> float:
    pattern = rf"{re.escape(label)}:\s*(-?[\d,]+(?:\.\d+)?)%"
    match = re.search(pattern, prompt)

    if not match:
        return 0.0

    return float(match.group(1).replace(",", ""))


def _category(prompt: str, label: str) -> str:
    pattern = rf"{re.escape(label)}:\s*(.+)"
    match = re.search(pattern, prompt)

    if not match:
        return "None"

    return match.group(1).strip()


def _mock_response(prompt: str) -> str:
    """
    Generate a realistic local development response from the
    financial summary supplied by finance_chat.py.

    No external API call is made in mock mode.
    """
    income = _money(prompt, "Total income")
    expenses = _money(prompt, "Total expenses")
    savings = _money(prompt, "Savings")
    savings_rate = _percent(prompt, "Savings rate")
    highest_category = _category(prompt, "Highest spending category")
    highest_category_amount = _money(prompt, "Highest category spending")

    if income == 0 and expenses == 0:
        return (
            "I don't have enough financial data to generate a useful "
            "summary yet."
        )

    if savings < 0:
        health = (
            "Your expenses are currently higher than your income, "
            "so your cash flow is under pressure."
        )
        action = (
            f"Your highest spending category is {highest_category} "
            f"at ₹{highest_category_amount:,.2f}. Reviewing this category "
            "could be a good starting point for reducing expenses."
        )
    elif savings_rate < 10:
        health = (
            "You are saving money, but your current savings rate is relatively low."
        )
        action = (
            f"Your highest spending category is {highest_category} "
            f"at ₹{highest_category_amount:,.2f}. Monitoring this category "
            "may help increase your savings."
        )
    elif savings_rate < 20:
        health = (
            "You have a positive savings position, with room to improve "
            "your savings rate."
        )
        action = (
            f"Your largest expense category is {highest_category} "
            f"at ₹{highest_category_amount:,.2f}. Keeping it under control "
            "could improve your savings."
        )
    else:
        health = "You have a healthy positive savings position."
        action = (
            f"Your largest expense category is {highest_category} "
            f"at ₹{highest_category_amount:,.2f}. Continue monitoring it "
            "to maintain your current financial position."
        )

    return (
        f"**Financial Summary**\n\n"
        f"- Income: ₹{income:,.2f}\n"
        f"- Expenses: ₹{expenses:,.2f}\n"
        f"- Savings: ₹{savings:,.2f}\n"
        f"- Savings rate: {savings_rate:.2f}%\n\n"
        f"**Insight:** {health}\n\n"
        f"**Recommendation:** {action}"
    )


def ask_llm(prompt: str) -> str:
    """Send a prompt to the LLM or use local mock mode."""

    if MOCK_LLM:
        return _mock_response(prompt)

    if not OPENAI_API_KEY:
        return (
            "The live LLM is unavailable because OPENAI_API_KEY is not "
            "configured. Enable MOCK_LLM=true for local development."
        )

    try:
        client = OpenAI(api_key=OPENAI_API_KEY)

        response = client.responses.create(
            model=OPENAI_MODEL,
            input=prompt
        )

        return response.output_text

    except Exception as exc:
        return (
            "The live LLM request could not be completed. "
            "The application is still running in fallback mode.\n\n"
            f"Error type: {type(exc).__name__}"
        )
