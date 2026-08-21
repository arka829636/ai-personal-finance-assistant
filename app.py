import streamlit as st
import pandas as pd

from src.database import get_connection
from src.finance_chat import answer_question
from src.ai_advisor import generate_advice


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Personal Finance Assistant",
    page_icon="💰",
    layout="wide",
)


# ============================================================
# MODERN FINTECH UI
# ============================================================

st.markdown(
    """
    <style>
    .stApp {
        background: #0B1220 !important;
        color: #E5E7EB !important;
    }

    .main .block-container {
        max-width: 1250px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .stApp p, .stApp label, .stApp span, .stApp li {
        color: #E5E7EB;
    }

    .stApp h1, .stApp h2, .stApp h3, .stApp h4 {
        color: #F8FAFC !important;
    }

    .hero {
        background: linear-gradient(135deg, #102A43 0%, #176B87 100%);
        padding: 30px 34px;
        border-radius: 20px;
        margin-bottom: 26px;
        border: 1px solid #24536B;
        box-shadow: 0 12px 35px rgba(0, 0, 0, .28);
    }

    .hero h1 {
        margin: 0;
        color: #FFFFFF !important;
        font-size: 31px;
    }

    .hero p {
        margin: 8px 0 0;
        color: #D7EEF7 !important;
        font-size: 15px;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #07111F 0%, #102A43 100%) !important;
        border-right: 1px solid #20354D;
    }

    section[data-testid="stSidebar"] * {
        color: #F8FAFC !important;
    }

    .kpi-card {
        background: #111C2E;
        border: 1px solid #263852;
        border-radius: 16px;
        padding: 18px 20px;
        min-height: 105px;
        box-shadow: 0 6px 20px rgba(0, 0, 0, .20);
    }

    .kpi-label {
        color: #94A3B8 !important;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: .06em;
    }

    .kpi-value {
        color: #F8FAFC !important;
        font-size: 25px;
        font-weight: 750;
        margin-top: 8px;
    }

    [data-testid="stMetric"] {
        background: #111C2E;
        border: 1px solid #263852;
        border-radius: 14px;
        padding: 16px;
    }

    [data-testid="stMetricLabel"] {
        color: #94A3B8 !important;
    }

    [data-testid="stMetricValue"] {
        color: #F8FAFC !important;
    }

    .stButton > button {
        background: #176B87 !important;
        color: #FFFFFF !important;
        border: 1px solid #2A8AA8 !important;
        border-radius: 10px;
        font-weight: 650;
    }

    .stButton > button:hover {
        background: #2188A5 !important;
    }

    .stTextInput input,
    .stNumberInput input,
    .stDateInput input {
        background: #111C2E !important;
        color: #F8FAFC !important;
        border: 1px solid #334155 !important;
    }

    div[data-baseweb="select"] > div {
        background: #111C2E !important;
        color: #F8FAFC !important;
        border-color: #334155 !important;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid #263852;
        border-radius: 12px;
        overflow: hidden;
    }

    hr {
        border-color: #263852 !important;
    }

    /* ---------------- FINANCE CHAT ---------------- */

    .chat-shell {
        background: #0E1929;
        border: 1px solid #233A55;
        border-radius: 20px;
        padding: 22px;
        margin-top: 8px;
        margin-bottom: 18px;
    }

    .chat-intro {
        background: linear-gradient(135deg, #102A43, #123C52);
        border: 1px solid #24536B;
        border-radius: 16px;
        padding: 20px 22px;
        margin-bottom: 20px;
    }

    .chat-intro-title {
        color: #FFFFFF;
        font-size: 22px;
        font-weight: 750;
        margin-bottom: 5px;
    }

    .chat-intro-text {
        color: #BFD8E5;
        font-size: 14px;
    }

    .chat-status {
        display: inline-block;
        margin-top: 10px;
        padding: 5px 10px;
        border-radius: 999px;
        background: #123C52;
        border: 1px solid #2A8AA8;
        color: #BDEBFA;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: .04em;
    }

    .suggestion {
        background: #111C2E;
        border: 1px solid #263852;
        border-radius: 12px;
        padding: 12px 14px;
        color: #CBD5E1;
        font-size: 13px;
        margin-bottom: 8px;
    }

    [data-testid="stChatMessage"] {
        border: 1px solid #263852;
        border-radius: 16px;
        padding: 13px 16px;
        margin-bottom: 12px;
        background: #111C2E;
    }

    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
        background: #102A43;
    }

    [data-testid="stChatMessageContent"] {
        color: #E5E7EB !important;
    }

    [data-testid="stChatInput"] {
        border-color: #2A8AA8 !important;
    }

    .chat-empty {
        text-align: center;
        padding: 35px 20px;
        color: #94A3B8;
    }

    .chat-empty-icon {
        font-size: 38px;
        margin-bottom: 8px;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# DATABASE FUNCTIONS
# ============================================================

def get_transactions():
    """Load all stored transactions."""
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
        return pd.read_sql_query(query, connection)
    finally:
        connection.close()


def get_budgets():
    """Load all stored budgets."""
    connection = get_connection()

    query = """
        SELECT
            category,
            budget
        FROM budgets
    """

    try:
        return pd.read_sql_query(query, connection)
    finally:
        connection.close()


# ============================================================
# LOAD DATA
# ============================================================

try:
    transactions_df = get_transactions()
except Exception as e:
    transactions_df = pd.DataFrame()
    st.error(f"Unable to load transaction data: {e}")


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown("# 💰 FinanceAI")
st.sidebar.caption("Personal Finance Assistant")
st.sidebar.markdown("---")
st.sidebar.markdown("### NAVIGATION")

page = st.sidebar.radio(
    "Go to",
    [
        "🏠 Dashboard",
        "💳 Transactions",
        "📊 Analysis",
        "💰 Budget",
        "🤖 AI Advisor",
        "💬 Finance Chat",
        "🚨 Anomaly Detection",
    ],
)


# ============================================================
# DASHBOARD
# ============================================================

if page == "🏠 Dashboard":

    st.markdown(
        """
        <div class="hero">
            <h1>Good to see you 👋</h1>
            <p>Your financial overview, spending insights and budget health in one place.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if transactions_df.empty:
        st.warning("No financial data available.")
    else:
        income = transactions_df[
            transactions_df["type"] == "Income"
        ]["amount"].sum()

        expenses = transactions_df[
            transactions_df["type"] == "Expense"
        ]["amount"].sum()

        savings = income - expenses
        savings_rate = (savings / income) * 100 if income > 0 else 0

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(
                f"<div class='kpi-card'><div class='kpi-label'>💵 TOTAL INCOME</div><div class='kpi-value'>₹{income:,.2f}</div></div>",
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown(
                f"<div class='kpi-card'><div class='kpi-label'>💸 TOTAL EXPENSES</div><div class='kpi-value'>₹{expenses:,.2f}</div></div>",
                unsafe_allow_html=True,
            )

        with col3:
            st.markdown(
                f"<div class='kpi-card'><div class='kpi-label'>💰 SAVINGS</div><div class='kpi-value'>₹{savings:,.2f}</div></div>",
                unsafe_allow_html=True,
            )

        with col4:
            st.markdown(
                f"<div class='kpi-card'><div class='kpi-label'>📈 SAVINGS RATE</div><div class='kpi-value'>{savings_rate:.1f}%</div></div>",
                unsafe_allow_html=True,
            )

        st.markdown("---")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📊 Expenses by Category")

            expense_data = transactions_df[
                transactions_df["type"] == "Expense"
            ]

            if not expense_data.empty:
                category_expenses = (
                    expense_data
                    .groupby("category")["amount"]
                    .sum()
                    .sort_values(ascending=False)
                )
                st.bar_chart(category_expenses)
            else:
                st.info("No expense data available.")

        with col2:
            st.subheader("📈 Income vs Expenses")

            comparison = pd.DataFrame(
                {"Amount": [income, expenses]},
                index=["Income", "Expenses"],
            )

            st.bar_chart(comparison)


# ============================================================
# TRANSACTIONS
# ============================================================

elif page == "💳 Transactions":

    st.markdown(
        """
        <div class="hero">
            <h1>💳 Transactions</h1>
            <p>Review and explore your stored financial transactions.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if transactions_df.empty:
        st.warning("No transactions available.")
    else:
        st.dataframe(
            transactions_df,
            use_container_width=True,
            hide_index=True,
        )

        st.markdown("---")
        st.subheader("📌 Transaction Summary")

        income = transactions_df[
            transactions_df["type"] == "Income"
        ]["amount"].sum()

        expenses = transactions_df[
            transactions_df["type"] == "Expense"
        ]["amount"].sum()

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Total Income", f"₹{income:,.2f}")

        with col2:
            st.metric("Total Expenses", f"₹{expenses:,.2f}")


# ============================================================
# ANALYSIS
# ============================================================

elif page == "📊 Analysis":

    st.markdown(
        """
        <div class="hero">
            <h1>📊 Financial Analytics</h1>
            <p>Understand your spending patterns and financial performance.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if transactions_df.empty:
        st.warning("No financial data available.")
    else:
        income = transactions_df[
            transactions_df["type"] == "Income"
        ]["amount"].sum()

        expenses_df = transactions_df[
            transactions_df["type"] == "Expense"
        ]

        expenses = expenses_df["amount"].sum()
        savings = income - expenses

        st.subheader("📌 Financial Summary")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Income", f"₹{income:,.2f}")

        with col2:
            st.metric("Expenses", f"₹{expenses:,.2f}")

        with col3:
            st.metric("Savings", f"₹{savings:,.2f}")

        st.markdown("---")
        st.subheader("📊 Spending by Category")

        if not expenses_df.empty:
            category_data = (
                expenses_df
                .groupby("category")["amount"]
                .sum()
                .sort_values(ascending=False)
            )

            st.bar_chart(category_data)

            st.markdown("---")
            st.subheader("🏆 Highest Spending Category")

            highest_category = category_data.index[0]
            highest_amount = category_data.iloc[0]

            st.success(
                f"Your highest spending category is "
                f"**{highest_category}** with "
                f"**₹{highest_amount:,.2f}**."
            )


# ============================================================
# BUDGET
# ============================================================

elif page == "💰 Budget":

    st.markdown(
        """
        <div class="hero">
            <h1>💰 Budget Health</h1>
            <p>Compare planned budgets with actual spending.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    try:
        budgets_df = get_budgets()

        if budgets_df.empty:
            st.warning("No budget data available.")
        else:
            expenses_df = transactions_df[
                transactions_df["type"] == "Expense"
            ]

            if not expenses_df.empty:
                spent_df = (
                    expenses_df
                    .groupby("category")["amount"]
                    .sum()
                    .reset_index()
                )
            else:
                spent_df = pd.DataFrame(
                    columns=["category", "amount"]
                )

            budget_df = budgets_df.merge(
                spent_df,
                on="category",
                how="left",
            )

            budget_df["amount"] = budget_df["amount"].fillna(0)
            budget_df["remaining"] = (
                budget_df["budget"] - budget_df["amount"]
            )

            def get_status(row):
                budget = row["budget"]
                spent = row["amount"]

                if budget <= 0:
                    return "⚪ No Budget"

                percentage = (spent / budget) * 100

                if percentage >= 100:
                    return "🔴 Over Budget"
                elif percentage >= 80:
                    return "🟡 Near Limit"
                return "🟢 Within Budget"

            budget_df["status"] = budget_df.apply(
                get_status,
                axis=1,
            )

            st.subheader("📊 Budget Overview")

            display_df = budget_df[
                [
                    "category",
                    "budget",
                    "amount",
                    "remaining",
                    "status",
                ]
            ].copy()

            display_df.columns = [
                "Category",
                "Budget",
                "Spent",
                "Remaining",
                "Status",
            ]

            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True,
            )

            st.markdown("---")
            st.subheader("📈 Budget vs Actual Spending")

            chart_df = budget_df[
                ["category", "budget", "amount"]
            ].copy()

            chart_df = chart_df.set_index("category")
            chart_df.columns = [
                "Budget",
                "Actual Spending",
            ]

            st.bar_chart(chart_df)

    except Exception as e:
        st.error(f"Budget analysis could not be loaded: {e}")


# ============================================================
# AI FINANCIAL ADVISOR
# ============================================================

elif page == "🤖 AI Advisor":

    st.markdown(
        """
        <div class="hero">
            <h1>🤖 Financial Advisor</h1>
            <p>Get explainable financial recommendations based on your current data.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write(
        "Get personalized financial recommendations based on your income and spending."
    )

    if st.button("🧠 Generate Financial Advice", type="primary"):

        try:
            generate_advice()

            if not transactions_df.empty:

                income = transactions_df[
                    transactions_df["type"] == "Income"
                ]["amount"].sum()

                expenses_df = transactions_df[
                    transactions_df["type"] == "Expense"
                ]

                expenses = expenses_df["amount"].sum()
                savings = income - expenses
                savings_rate = (
                    (savings / income) * 100
                    if income > 0
                    else 0
                )

                st.subheader("💡 Your Financial Overview")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("Income", f"₹{income:,.2f}")

                with col2:
                    st.metric("Expenses", f"₹{expenses:,.2f}")

                with col3:
                    st.metric(
                        "Savings Rate",
                        f"{savings_rate:.2f}%",
                    )

                if savings_rate >= 30:
                    st.success(
                        "✅ Excellent savings rate! You are saving a healthy portion of your income."
                    )
                elif savings_rate >= 20:
                    st.info(
                        "🟢 Good savings rate. Try to maintain it consistently."
                    )
                elif savings_rate >= 10:
                    st.warning(
                        "🟡 Your savings rate is moderate. Consider reducing unnecessary expenses."
                    )
                else:
                    st.error(
                        "🔴 Your savings rate is low. Review your spending."
                    )

                if not expenses_df.empty and expenses > 0:

                    category_spending = (
                        expenses_df
                        .groupby("category")["amount"]
                        .sum()
                        .sort_values(ascending=False)
                    )

                    highest_category = category_spending.index[0]
                    highest_amount = category_spending.iloc[0]

                    percentage = (
                        highest_amount / expenses
                    ) * 100

                    st.markdown("---")
                    st.subheader("📌 Spending Recommendation")

                    st.write(
                        f"Your highest spending category is "
                        f"**{highest_category}** with spending of "
                        f"**₹{highest_amount:,.2f}**."
                    )

                    if percentage > 40:
                        st.warning(
                            f"⚠️ {highest_category} represents "
                            f"{percentage:.1f}% of your total expenses. "
                            "Consider reviewing this category."
                        )
                    else:
                        st.info(
                            f"👍 {highest_category} represents "
                            f"{percentage:.1f}% of your total expenses."
                        )

        except Exception as e:
            st.error(f"Unable to generate financial advice: {e}")


# ============================================================
# FINANCE CHAT — IMPROVED AI CHAT UI
# ============================================================

elif page == "💬 Finance Chat":

    st.markdown(
        """
        <div class="hero">
            <h1>💬 Finance Chat</h1>
            <p>Your personal financial assistant for questions about income, spending and savings.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="chat-shell">
            <div class="chat-intro">
                <div class="chat-intro-title">🤖 Ask FinanceAI</div>
                <div class="chat-intro-text">
                    Ask questions about your stored financial data and get
                    clear, easy-to-understand answers.
                </div>
                <div class="chat-status">● FINANCIAL DATA CONNECTED</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # CHAT SESSION
    # --------------------------------------------------------

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # --------------------------------------------------------
    # STARTER QUESTIONS
    # --------------------------------------------------------

    if not st.session_state.chat_history:

        st.markdown("### 💡 Try asking")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(
                '<div class="suggestion">💸 How much did I spend?</div>',
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown(
                '<div class="suggestion">🏆 What is my highest spending category?</div>',
                unsafe_allow_html=True,
            )

        with col3:
            st.markdown(
                '<div class="suggestion">📊 Give me a financial summary</div>',
                unsafe_allow_html=True,
            )

        st.markdown("---")

        st.markdown(
            """
            <div class="chat-empty">
                <div class="chat-empty-icon">💬</div>
                Start a conversation with your financial assistant.
            </div>
            """,
            unsafe_allow_html=True,
        )

    # --------------------------------------------------------
    # DISPLAY CHAT HISTORY
    # --------------------------------------------------------

    for message in st.session_state.chat_history:

        with st.chat_message(
            message["role"],
            avatar="👤" if message["role"] == "user" else "🤖",
        ):
            st.markdown(message["content"])

    # --------------------------------------------------------
    # CHAT INPUT
    # --------------------------------------------------------

    question = st.chat_input(
        "Ask about your income, spending or savings..."
    )

    if question:

        st.session_state.chat_history.append(
            {
                "role": "user",
                "content": question,
            }
        )

        with st.chat_message("user", avatar="👤"):
            st.markdown(question)

        with st.chat_message("assistant", avatar="🤖"):

            with st.spinner("Analyzing your financial data..."):

                try:
                    response = answer_question(question)

                except Exception:
                    response = (
                        "Sorry, I couldn't process that question right now. "
                        "Please try another financial question."
                    )

            st.markdown(response)

        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "content": response,
            }
        )

    # --------------------------------------------------------
    # CLEAR CHAT
    # --------------------------------------------------------

    if st.session_state.chat_history:

        st.markdown("---")

        col1, col2 = st.columns([5, 1])

        with col2:

            if st.button(
                "🗑️ Clear Chat",
                use_container_width=True,
            ):
                st.session_state.chat_history = []
                st.rerun()


# ============================================================
# ANOMALY DETECTION
# ============================================================

elif page == "🚨 Anomaly Detection":

    st.markdown(
        """
        <div class="hero">
            <h1>🚨 Spending Anomaly Detection</h1>
            <p>Review unusual spending patterns detected by your ML module.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    expense_count = (
        len(
            transactions_df[
                transactions_df["type"] == "Expense"
            ]
        )
        if not transactions_df.empty
        else 0
    )

    st.info(
        "Isolation Forest anomaly detection is implemented and tested. "
        "The detector remains in src/anomaly_detection.py."
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Expense Transactions", expense_count)

    with c2:
        st.metric("Detection Method", "Isolation Forest")

    with c3:
        st.metric("Status", "Model Ready")

    st.markdown("### 🔍 What this module does")

    st.write(
        "The anomaly detector identifies transactions that differ "
        "significantly from normal spending patterns without requiring "
        "manually labelled anomaly data."
    )

    st.warning(
        "The detector itself remains in src/anomaly_detection.py. "
        "This UI page does not duplicate or change its ML logic."
    )
