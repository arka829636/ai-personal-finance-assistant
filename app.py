import streamlit as st
import pandas as pd

from src.database import get_connection, initialize_database
from src.finance_chat import answer_question, detect_intent
from src.ml_expense_prediction import get_prediction
from src.anomaly_detection import get_anomalies


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

initialize_database()


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="FinanceAI",
    page_icon="💰",
    layout="wide",
)


# ============================================================
# CUSTOM CSS
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

.stApp h1,
.stApp h2,
.stApp h3,
.stApp h4 {
    color: #F8FAFC !important;
}

.stApp p,
.stApp label,
.stApp span,
.stApp li {
    color: #E5E7EB;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #07111F 0%,
        #102A43 100%
    ) !important;
    border-right: 1px solid #20354D;
}

section[data-testid="stSidebar"] * {
    color: #F8FAFC !important;
}

.hero {
    background: linear-gradient(
        135deg,
        #102A43 0%,
        #176B87 100%
    );
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


/* ============================================================
   FINANCE CHAT
   ============================================================ */

.chat-shell {
    background: #0E1929;
    border: 1px solid #233A55;
    border-radius: 20px;
    padding: 22px;
    margin-bottom: 20px;
}

.chat-intro {
    background: linear-gradient(
        135deg,
        #102A43,
        #123C52
    );
    border: 1px solid #24536B;
    border-radius: 16px;
    padding: 20px 22px;
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

[data-testid="stChatMessageContent"] {
    color: #E5E7EB !important;
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

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# DATABASE FUNCTIONS
# ============================================================

def get_transactions():
    connection = get_connection()

    query = """
        SELECT
            id,
            date,
            type,
            category,
            description,
            amount,
            payment_method
        FROM transactions
        ORDER BY date
    """

    try:
        return pd.read_sql_query(
            query,
            connection,
        )

    finally:
        connection.close()


def get_budgets():
    connection = get_connection()

    query = """
        SELECT
            category,
            budget
        FROM budgets
        ORDER BY category
    """

    try:
        return pd.read_sql_query(
            query,
            connection,
        )

    finally:
        connection.close()


# ============================================================
# LOAD DATA
# ============================================================

try:

    transactions_df = get_transactions()

except Exception as e:

    transactions_df = pd.DataFrame()

    st.error(
        f"Unable to load transaction data: {e}"
    )


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown(
    "# 💰 FinanceAI"
)

st.sidebar.caption(
    "Personal Finance Assistant"
)

st.sidebar.markdown("---")

st.sidebar.markdown(
    "### NAVIGATION"
)

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
    key="main_navigation",
)


# ============================================================
# DASHBOARD
# ============================================================

if page == "🏠 Dashboard":

    st.markdown(
        """
<div class="hero">
<h1>Good to see you 👋</h1>
<p>Your financial overview, spending insights, budget health and ML predictions in one place.</p>
</div>
""",
        unsafe_allow_html=True,
    )

    if transactions_df.empty:

        st.warning(
            "No financial data available."
        )

    else:

        income = transactions_df.loc[
            transactions_df["type"] == "Income",
            "amount",
        ].sum()

        expenses_df = transactions_df[
            transactions_df["type"] == "Expense"
        ].copy()

        expenses = expenses_df["amount"].sum()

        savings = income - expenses

        savings_rate = (
            (savings / income) * 100
            if income > 0
            else 0
        )

        # ----------------------------------------------------
        # KPI CARDS
        # ----------------------------------------------------

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.markdown(
                f"""
<div class="kpi-card">
<div class="kpi-label">💵 TOTAL INCOME</div>
<div class="kpi-value">₹{income:,.2f}</div>
</div>
""",
                unsafe_allow_html=True,
            )

        with col2:

            st.markdown(
                f"""
<div class="kpi-card">
<div class="kpi-label">💸 TOTAL EXPENSES</div>
<div class="kpi-value">₹{expenses:,.2f}</div>
</div>
""",
                unsafe_allow_html=True,
            )

        with col3:

            st.markdown(
                f"""
<div class="kpi-card">
<div class="kpi-label">💰 SAVINGS</div>
<div class="kpi-value">₹{savings:,.2f}</div>
</div>
""",
                unsafe_allow_html=True,
            )

        with col4:

            st.markdown(
                f"""
<div class="kpi-card">
<div class="kpi-label">📈 SAVINGS RATE</div>
<div class="kpi-value">{savings_rate:.1f}%</div>
</div>
""",
                unsafe_allow_html=True,
            )

        st.markdown("---")

        # ----------------------------------------------------
        # CHARTS
        # ----------------------------------------------------

        col1, col2 = st.columns(2)

        with col1:

            st.subheader(
                "📊 Expenses by Category"
            )

            if not expenses_df.empty:

                category_expenses = (
                    expenses_df
                    .groupby("category")["amount"]
                    .sum()
                    .sort_values(
                        ascending=False
                    )
                )

                st.bar_chart(
                    category_expenses
                )

            else:

                st.info(
                    "No expense data available."
                )

        with col2:

            st.subheader(
                "📈 Income vs Expenses"
            )

            comparison_df = pd.DataFrame(
                {
                    "Amount": [
                        income,
                        expenses,
                    ]
                },
                index=[
                    "Income",
                    "Expenses",
                ],
            )

            st.bar_chart(
                comparison_df
            )

        # ----------------------------------------------------
        # EXPENSE PREDICTION
        # ----------------------------------------------------

        st.markdown("---")

        st.subheader(
            "🔮 Expense Prediction"
        )

        try:

            prediction = get_prediction()

            if prediction is None:

                st.info(
                    "Not enough expense data "
                    "to generate a prediction."
                )

            else:

                predicted_expense = float(
                    prediction["prediction"]
                )

                prediction_date = (
                    prediction["date"].date()
                )

                historical_average = float(
                    expenses_df["amount"].mean()
                )

                expected_change = (
                    (
                        predicted_expense
                        - historical_average
                    )
                    / historical_average
                    * 100
                    if historical_average > 0
                    else 0
                )

                p1, p2, p3 = st.columns(3)

                with p1:

                    st.metric(
                        "Predicted Next-Day Expense",
                        f"₹{predicted_expense:,.2f}",
                    )

                with p2:

                    st.metric(
                        "Historical Average",
                        f"₹{historical_average:,.2f}",
                    )

                with p3:

                    st.metric(
                        "Expected Change",
                        f"{expected_change:.1f}%",
                    )

                st.caption(
                    f"Prediction for "
                    f"{prediction_date}"
                )

                if expected_change > 0:

                    st.warning(
                        f"⚠️ The predicted expense is "
                        f"{expected_change:.1f}% higher "
                        "than your historical average."
                    )

                elif expected_change < 0:

                    st.success(
                        f"✅ The predicted expense is "
                        f"{abs(expected_change):.1f}% lower "
                        "than your historical average."
                    )

                else:

                    st.info(
                        "The predicted expense is "
                        "close to your historical average."
                    )

                with st.expander(
                    "⚙️ View ML Model Performance"
                ):

                    m1, m2, m3 = st.columns(3)

                    with m1:

                        st.metric(
                            "MAE",
                            f"₹{prediction['mae']:,.2f}",
                        )

                    with m2:

                        st.metric(
                            "RMSE",
                            f"₹{prediction['rmse']:,.2f}",
                        )

                    with m3:

                        st.metric(
                            "R²",
                            f"{prediction['r2']:.4f}",
                        )

        except Exception as e:

            st.warning(
                f"Expense prediction unavailable: {e}"
            )

        # ----------------------------------------------------
        # FINANCIAL HEALTH
        # ----------------------------------------------------

        st.markdown("---")

        st.subheader(
            "💡 Financial Health Snapshot"
        )

        health1, health2 = st.columns(2)

        with health1:

            if savings_rate >= 20:

                st.success(
                    "🟢 Healthy savings performance"
                )

            elif savings_rate >= 10:

                st.warning(
                    "🟡 Moderate savings performance"
                )

            else:

                st.error(
                    "🔴 Low savings performance"
                )

        with health2:

            if not expenses_df.empty:

                category_spending = (
                    expenses_df
                    .groupby("category")["amount"]
                    .sum()
                    .sort_values(
                        ascending=False
                    )
                )

                highest_category = (
                    category_spending.index[0]
                )

                highest_amount = float(
                    category_spending.iloc[0]
                )

                st.info(
                    f"🏆 Highest spending category: "
                    f"**{highest_category}** "
                    f"(₹{highest_amount:,.2f})"
                )


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

        st.warning(
            "No transactions available."
        )

    else:

        st.dataframe(
            transactions_df,
            use_container_width=True,
            hide_index=True,
        )


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

        st.warning(
            "No financial data available."
        )

    else:

        income = transactions_df.loc[
            transactions_df["type"] == "Income",
            "amount",
        ].sum()

        expenses_df = transactions_df[
            transactions_df["type"] == "Expense"
        ].copy()

        expenses = expenses_df["amount"].sum()

        savings = income - expenses

        c1, c2, c3 = st.columns(3)

        with c1:

            st.metric(
                "Income",
                f"₹{income:,.2f}",
            )

        with c2:

            st.metric(
                "Expenses",
                f"₹{expenses:,.2f}",
            )

        with c3:

            st.metric(
                "Savings",
                f"₹{savings:,.2f}",
            )

        st.markdown("---")

        st.subheader(
            "📊 Spending by Category"
        )

        if not expenses_df.empty:

            category_data = (
                expenses_df
                .groupby("category")["amount"]
                .sum()
                .sort_values(
                    ascending=False
                )
            )

            st.bar_chart(
                category_data
            )

            highest_category = (
                category_data.index[0]
            )

            highest_amount = float(
                category_data.iloc[0]
            )

            st.success(
                f"🏆 Highest spending category: "
                f"**{highest_category}** "
                f"₹{highest_amount:,.2f}"
            )

        else:

            st.info(
                "No expense data available."
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

            st.warning(
                "No budget data available."
            )

        else:

            expenses_df = transactions_df[
                transactions_df["type"] == "Expense"
            ].copy()

            if expenses_df.empty:

                spent_df = pd.DataFrame(
                    columns=[
                        "category",
                        "amount",
                    ]
                )

            else:

                spent_df = (
                    expenses_df
                    .groupby("category")["amount"]
                    .sum()
                    .reset_index()
                )

            budget_df = budgets_df.merge(
                spent_df,
                on="category",
                how="left",
            )

            budget_df["amount"] = (
                budget_df["amount"]
                .fillna(0)
            )

            budget_df["remaining"] = (
                budget_df["budget"]
                - budget_df["amount"]
            )

            def budget_status(row):

                budget = float(
                    row["budget"]
                )

                spent = float(
                    row["amount"]
                )

                if budget <= 0:

                    return "⚪ No Budget"

                percentage = (
                    spent / budget
                ) * 100

                if percentage >= 100:

                    return "🔴 Over Budget"

                if percentage >= 80:

                    return "🟡 Near Limit"

                return "🟢 Within Budget"

            budget_df["status"] = (
                budget_df.apply(
                    budget_status,
                    axis=1,
                )
            )

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

            chart_df = budget_df[
                [
                    "category",
                    "budget",
                    "amount",
                ]
            ].copy()

            chart_df = (
                chart_df
                .set_index("category")
            )

            chart_df.columns = [
                "Budget",
                "Actual Spending",
            ]

            st.bar_chart(
                chart_df
            )

    except Exception as e:

        st.error(
            f"Budget analysis failed: {e}"
        )


# ============================================================
# AI ADVISOR
# ============================================================

elif page == "🤖 AI Advisor":

    st.markdown(
        """
<div class="hero">
<h1>🤖 Financial Advisor</h1>
<p>Get explainable financial recommendations based on your current financial data.</p>
</div>
""",
        unsafe_allow_html=True,
    )

    if transactions_df.empty:

        st.warning(
            "No financial data available."
        )

    else:

        income = transactions_df.loc[
            transactions_df["type"] == "Income",
            "amount",
        ].sum()

        expenses_df = transactions_df[
            transactions_df["type"] == "Expense"
        ].copy()

        expenses = expenses_df["amount"].sum()

        savings = income - expenses

        savings_rate = (
            (savings / income) * 100
            if income > 0
            else 0
        )

        c1, c2, c3 = st.columns(3)

        with c1:

            st.metric(
                "Total Income",
                f"₹{income:,.2f}",
            )

        with c2:

            st.metric(
                "Total Expenses",
                f"₹{expenses:,.2f}",
            )

        with c3:

            st.metric(
                "Savings Rate",
                f"{savings_rate:.2f}%",
            )

        st.markdown("---")

        st.subheader(
            "🧠 Financial Insights"
        )

        if savings_rate >= 30:

            st.success(
                "✅ Your savings rate is strong."
            )

        elif savings_rate >= 20:

            st.info(
                "🟢 Your savings rate is good."
            )

        elif savings_rate >= 10:

            st.warning(
                "🟡 Your savings rate is moderate."
            )

        else:

            st.error(
                "🔴 Your savings rate is low. "
                "Review your spending."
            )

        if not expenses_df.empty:

            category_spending = (
                expenses_df
                .groupby("category")["amount"]
                .sum()
                .sort_values(
                    ascending=False
                )
            )

            highest_category = (
                category_spending.index[0]
            )

            highest_amount = float(
                category_spending.iloc[0]
            )

            percentage = (
                highest_amount / expenses * 100
                if expenses > 0
                else 0
            )

            st.info(
                f"🏆 Highest spending category: "
                f"**{highest_category}** "
                f"₹{highest_amount:,.2f} "
                f"({percentage:.1f}% of expenses)"
            )

            if savings <= 0:

                st.error(
                    "🚨 Expenses are currently "
                    "higher than income."
                )


# ============================================================
# FINANCE CHAT
# ============================================================

elif page == "💬 Finance Chat":

    st.markdown(
        """
<div class="hero">
<h1>💬 Finance Chat</h1>
<p>Ask questions about income, spending, savings, predictions and unusual transactions.</p>
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
FinanceAI identifies your question type and retrieves the relevant financial or machine-learning context.
</div>
<div class="chat-status">● FINANCIAL DATA CONNECTED</div>
</div>
</div>
""",
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # INITIALIZE CHAT HISTORY
    # --------------------------------------------------------

    if "chat_history" not in st.session_state:

        st.session_state.chat_history = []

    # --------------------------------------------------------
    # STARTER QUESTIONS
    # --------------------------------------------------------

    if not st.session_state.chat_history:

        st.markdown(
            "### 💡 Try asking"
        )

        q1, q2, q3 = st.columns(3)

        with q1:

            st.markdown(
                """
<div class="suggestion">
💸 How much did I spend?
</div>
""",
                unsafe_allow_html=True,
            )

        with q2:

            st.markdown(
                """
<div class="suggestion">
🔮 What is my predicted expense?
</div>
""",
                unsafe_allow_html=True,
            )

        with q3:

            st.markdown(
                """
<div class="suggestion">
🚨 Did you detect unusual spending?
</div>
""",
                unsafe_allow_html=True,
            )

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
    # INTENT LABELS
    # --------------------------------------------------------

    intent_labels = {
        "income": "💵 Income",
        "expenses": "💸 Total Expenses",
        "savings": "💰 Savings",
        "category": "📊 Category Spending",
        "prediction": "🔮 Expense Prediction",
        "anomaly": "🚨 Anomaly Detection",
        "comparison": "⚖️ Prediction Comparison",
        "general": "🧠 General Financial Question",
    }

    # --------------------------------------------------------
    # DISPLAY CHAT HISTORY
    # --------------------------------------------------------

    for message in st.session_state.chat_history:

        role = message["role"]

        avatar = (
            "👤"
            if role == "user"
            else "🤖"
        )

        with st.chat_message(
            role,
            avatar=avatar,
        ):

            st.markdown(
                message["content"]
            )

            if (
                role == "assistant"
                and "intent" in message
            ):

                intent = message["intent"]

                st.caption(
                    f"🔎 Detected intent: "
                    f"`{intent_labels.get(intent, intent)}`"
                )

    # --------------------------------------------------------
    # ONE CHAT INPUT
    # --------------------------------------------------------

    question = st.chat_input(
        "Ask about your income, spending, savings or predictions...",
        key="finance_chat_input",
    )

    if question:

        # ----------------------------------------------------
        # USER MESSAGE
        # ----------------------------------------------------

        st.session_state.chat_history.append(
            {
                "role": "user",
                "content": question,
            }
        )

        with st.chat_message(
            "user",
            avatar="👤",
        ):

            st.markdown(
                question
            )

        # ----------------------------------------------------
        # DETECT INTENT
        # ----------------------------------------------------

        intent = detect_intent(
            question
        )

        # ----------------------------------------------------
        # GENERATE ANSWER
        # ----------------------------------------------------

        with st.chat_message(
            "assistant",
            avatar="🤖",
        ):

            with st.spinner(
                "Analyzing your financial data..."
            ):

                try:

                    response = answer_question(
                        question
                    )

                except Exception as e:

                    response = (
                        "Sorry, I couldn't process "
                        "that question right now."
                    )

                    st.error(
                        f"Technical error: {e}"
                    )

            st.markdown(
                response
            )

            st.caption(
                f"🔎 Detected intent: "
                f"`{intent_labels.get(intent, intent)}`"
            )

        # ----------------------------------------------------
        # SAVE ASSISTANT RESPONSE
        # ----------------------------------------------------

        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "content": response,
                "intent": intent,
            }
        )

    # --------------------------------------------------------
    # ONE CLEAR CHAT BUTTON
    # --------------------------------------------------------

    if st.session_state.chat_history:

        st.markdown("---")

        clear_col1, clear_col2 = (
            st.columns([5, 1])
        )

        with clear_col2:

            if st.button(
                "🗑️ Clear Chat",
                key="finance_chat_clear_button",
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
<p>Review unusual spending patterns detected by the Isolation Forest model.</p>
</div>
""",
        unsafe_allow_html=True,
    )

    try:

        expenses_df = transactions_df[
            transactions_df["type"] == "Expense"
        ].copy()

        expense_count = len(
            expenses_df
        )

        anomalies_df = get_anomalies()

        if anomalies_df is None:

            anomalies_df = pd.DataFrame()

        anomaly_count = len(
            anomalies_df
        )

        normal_count = max(
            expense_count - anomaly_count,
            0,
        )

        anomaly_rate = (
            anomaly_count
            / expense_count
            * 100
            if expense_count > 0
            else 0
        )

        # ----------------------------------------------------
        # KPI CARDS
        # ----------------------------------------------------

        c1, c2, c3, c4 = st.columns(4)

        with c1:

            st.metric(
                "Expense Transactions",
                expense_count,
            )

        with c2:

            st.metric(
                "Anomalies Detected",
                anomaly_count,
            )

        with c3:

            st.metric(
                "Normal Transactions",
                normal_count,
            )

        with c4:

            st.metric(
                "Anomaly Rate",
                f"{anomaly_rate:.1f}%",
            )

        st.markdown("---")

        # ----------------------------------------------------
        # ANOMALY TABLE
        # ----------------------------------------------------

        st.subheader(
            "🚨 Detected Unusual Spending"
        )

        if anomalies_df.empty:

            st.success(
                "No unusual expense transactions "
                "were detected."
            )

        else:

            display_columns = [
                "date",
                "category",
                "description",
                "amount",
                "anomaly_score",
            ]

            available_columns = [
                column
                for column in display_columns
                if column in anomalies_df.columns
            ]

            display_df = anomalies_df[
                available_columns
            ].copy()

            if "amount" in display_df.columns:

                display_df["amount"] = (
                    display_df["amount"]
                    .map(
                        lambda x:
                        f"₹{float(x):,.2f}"
                    )
                )

            if "anomaly_score" in display_df.columns:

                display_df["anomaly_score"] = (
                    display_df["anomaly_score"]
                    .map(
                        lambda x:
                        f"{float(x):.4f}"
                    )
                )

            rename_map = {
                "date": "Date",
                "category": "Category",
                "description": "Description",
                "amount": "Amount",
                "anomaly_score": "Anomaly Score",
            }

            display_df = display_df.rename(
                columns=rename_map
            )

            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True,
            )

            st.warning(
                "These transactions were flagged by "
                "Isolation Forest because their spending "
                "amounts differ from the normal pattern "
                "learned from the expense data."
            )

        # ----------------------------------------------------
        # HOW IT WORKS
        # ----------------------------------------------------

        st.markdown("---")

        st.subheader(
            "🔍 How the Detection Works"
        )

        left, right = st.columns(2)

        with left:

            st.markdown(
                "**Model:** Isolation Forest"
            )

            st.markdown(
                "**Learning type:** Unsupervised ML"
            )

            st.markdown(
                "**Input feature:** Transaction amount"
            )

            st.markdown(
                "**Labels required:** No"
            )

        with right:

            st.markdown(
                "**Prediction:**"
            )

            st.markdown(
                "`-1` = Anomaly"
            )

            st.markdown(
                "`1` = Normal"
            )

            st.markdown(
                "**Anomaly score:** Lower values "
                "indicate more unusual observations."
            )

    except Exception as e:

        st.error(
            f"Unable to run anomaly detection: {e}"
        )