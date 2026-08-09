import streamlit as st
import pandas as pd

from src.database import get_connection
from src.finance_chat import answer_question
from src.ai_advisor import generate_advice
from src.ml_expense_prediction import get_prediction


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Personal Finance Assistant",
    page_icon="💰",
    layout="wide"
)


# ===================== MODERN UI STYLING =====================
st.markdown("""
<style>
/* ============================================================
   FINANCEAI — PREMIUM DARK FINTECH UI
   ============================================================ */

.stApp {
    background:
        radial-gradient(circle at 85% 5%, rgba(34, 211, 238, .08), transparent 25%),
        radial-gradient(circle at 10% 20%, rgba(59, 130, 246, .06), transparent 25%),
        #08111F !important;
    color: #E5E7EB !important;
}

.main .block-container {
    max-width: 1450px;
    padding: 2rem 2.2rem 4rem;
}

/* Typography */
.stApp h1, .stApp h2, .stApp h3, .stApp h4,
.stApp h5, .stApp h6 {
    color: #F8FAFC !important;
}

.stApp p, .stApp label {
    color: #B8C5D4;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #050C16 0%, #0B1B2D 55%, #0E263B 100%) !important;
    border-right: 1px solid #1D334A;
}

section[data-testid="stSidebar"] * {
    color: #F8FAFC !important;
}

section[data-testid="stSidebar"] [data-testid="stRadio"] label {
    border-radius: 10px;
    padding: 8px 10px;
}

section[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: rgba(34, 211, 238, .10);
}

/* Hero */
.hero {
    position: relative;
    overflow: hidden;
    background:
        radial-gradient(circle at 90% 15%, rgba(103,232,249,.18), transparent 26%),
        linear-gradient(135deg, #0D2137 0%, #124B65 52%, #176B87 100%);
    border: 1px solid #285D75;
    border-radius: 24px;
    padding: 30px 32px;
    margin-bottom: 24px;
    box-shadow: 0 18px 45px rgba(0,0,0,.28);
}

.hero:after {
    content: "";
    position: absolute;
    width: 180px;
    height: 180px;
    right: -60px;
    bottom: -90px;
    border-radius: 50%;
    border: 1px solid rgba(255,255,255,.12);
}

.hero h1 {
    margin: 0;
    color: #FFFFFF !important;
    font-size: 31px;
    font-weight: 800;
}

.hero p {
    margin: 8px 0 0;
    color: #D7EEF7 !important;
    font-size: 14px;
}

.hero-badge {
    display: inline-block;
    margin-top: 15px;
    padding: 6px 11px;
    border-radius: 999px;
    background: rgba(255,255,255,.10);
    border: 1px solid rgba(255,255,255,.16);
    color: #DFF8FF !important;
    font-size: 11px;
    font-weight: 750;
    letter-spacing: .4px;
}

/* KPI cards */
.kpi-card {
    background: linear-gradient(145deg, #111D2F, #0D1727);
    border: 1px solid #253A52;
    border-radius: 18px;
    padding: 18px 19px;
    min-height: 128px;
    box-shadow: 0 9px 24px rgba(0,0,0,.20);
    transition: transform .18s ease, border-color .18s ease;
}

.kpi-card:hover {
    transform: translateY(-2px);
    border-color: #2E607B;
}

.kpi-label {
    color: #8EA1B7 !important;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: .65px;
}

.kpi-value {
    color: #F8FAFC !important;
    font-size: 25px;
    font-weight: 800;
    margin-top: 9px;
}

.kpi-note {
    color: #71839A !important;
    font-size: 11px;
    margin-top: 7px;
}

.green { color: #34D399 !important; }
.red { color: #FB7185 !important; }
.cyan { color: #67E8F9 !important; }
.yellow { color: #FBBF24 !important; }

/* Content cards */
.ui-card {
    background: rgba(15, 27, 44, .92);
    border: 1px solid #253A52;
    border-radius: 19px;
    padding: 20px;
    margin-bottom: 18px;
    box-shadow: 0 9px 24px rgba(0,0,0,.17);
}

.ui-card-title {
    color: #F8FAFC !important;
    font-size: 16px;
    font-weight: 780;
    margin-bottom: 4px;
}

.ui-card-subtitle {
    color: #7F92A8 !important;
    font-size: 12px;
    margin-bottom: 14px;
}

/* Mini insight cards */
.insight-card {
    background: #0D1929;
    border: 1px solid #23384F;
    border-radius: 15px;
    padding: 15px;
    min-height: 105px;
}

.insight-icon {
    font-size: 20px;
}

.insight-title {
    color: #F1F5F9 !important;
    font-size: 13px;
    font-weight: 750;
    margin-top: 5px;
}

.insight-text {
    color: #91A2B5 !important;
    font-size: 11px;
    margin-top: 4px;
}

/* Section heading */
.section-head {
    display: flex;
    align-items: center;
    gap: 9px;
    color: #F8FAFC !important;
    font-size: 17px;
    font-weight: 780;
    margin: 7px 0 4px;
}

.section-caption {
    color: #788BA1 !important;
    font-size: 12px;
    margin-bottom: 12px;
}

/* Progress */
.budget-label {
    display: flex;
    justify-content: space-between;
    color: #D8E2EC !important;
    font-size: 12px;
    font-weight: 650;
    margin-top: 9px;
}

/* Buttons */
.stButton > button {
    border-radius: 10px !important;
    font-weight: 700 !important;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #0E7490, #0891B2) !important;
    border: 1px solid #22A9C5 !important;
    color: white !important;
}

/* Metrics */
[data-testid="stMetric"] {
    background: #111D2F;
    border: 1px solid #253A52;
    border-radius: 14px;
    padding: 14px;
}

[data-testid="stMetricLabel"] {
    color: #8EA1B7 !important;
}

[data-testid="stMetricValue"] {
    color: #F8FAFC !important;
}

/* STAGE 2 UX POLISH */
.page-kicker { display:inline-flex; align-items:center; gap:7px; color:#8EA1B7 !important; font-size:11px; font-weight:800; letter-spacing:.8px; text-transform:uppercase; margin-bottom:7px; }
.section-caption { color:#7F92A8 !important; font-size:12px; margin:0 0 14px; }
.health-score { border-radius:16px; padding:18px; background:linear-gradient(135deg,#10283A,#0D1929); border:1px solid #27516A; }
.health-score-value { font-size:34px; font-weight:850; color:#67E8F9 !important; }
.health-score-label { color:#AFC0D1 !important; font-size:12px; }
.status-pill { display:inline-block; padding:5px 10px; border-radius:999px; font-size:11px; font-weight:800; margin-top:7px; }
.status-good { background:rgba(52,211,153,.12); color:#34D399 !important; border:1px solid rgba(52,211,153,.25); }
.status-warn { background:rgba(251,191,36,.12); color:#FBBF24 !important; border:1px solid rgba(251,191,36,.25); }
.status-bad { background:rgba(251,113,133,.12); color:#FB7185 !important; border:1px solid rgba(251,113,133,.25); }
.insight-card { transition: transform .18s ease, border-color .18s ease, background .18s ease; }
.insight-card:hover { transform:translateY(-2px); border-color:#2E607B; background:#102034; }
div.stButton > button { border-radius:10px; border:1px solid #2B4962; background:#102236; color:#EAF4FB; font-weight:700; }
div.stButton > button:hover { border-color:#38BDF8; color:#FFFFFF; background:#12304A; }
button[kind="primary"] { background:linear-gradient(135deg,#0EA5E9,#14B8A6) !important; border:0 !important; }
[data-testid="stExpander"] { background:#0E1929; border:1px solid #253A52; border-radius:14px; }
/* Inputs */
.stTextInput input, .stNumberInput input, .stDateInput input {
    background: #0E1929 !important;
    color: #F8FAFC !important;
    border: 1px solid #31465D !important;
}

div[data-baseweb="select"] > div {
    background: #0E1929 !important;
    color: #F8FAFC !important;
    border-color: #31465D !important;
}

/* Tables and chat */
[data-testid="stDataFrame"] {
    border: 1px solid #253A52;
    border-radius: 13px;
    overflow: hidden;
}

[data-testid="stChatMessage"] {
    background: #101C2D;
    border: 1px solid #253A52;
    border-radius: 14px;
    margin-bottom: 10px;
}

hr {
    border-color: #253A52 !important;
}

#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ============================================================
# DATABASE FUNCTIONS
# ============================================================

def get_transactions():
    """Get all transactions from the database."""

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

    df = pd.read_sql_query(query, connection)

    connection.close()

    return df


def get_budgets():
    """Get budget information from the database."""

    connection = get_connection()

    query = """
        SELECT
            category,
            budget
        FROM budgets
    """

    df = pd.read_sql_query(query, connection)

    connection.close()

    return df


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
        "🚨 Anomaly Detection"
    ]
)


# ============================================================
# DASHBOARD
# ============================================================

if page == "🏠 Dashboard":

    if transactions_df.empty:
        st.markdown("""
        <div class="hero">
            <h1>Welcome to FinanceAI 👋</h1>
            <p>Your personal finance command center.</p>
            <span class="hero-badge">● READY FOR YOUR FINANCIAL DATA</span>
        </div>
        """, unsafe_allow_html=True)
        st.warning("No financial data available.")
    else:

        income = transactions_df[
            transactions_df["type"].astype(str).str.lower() == "income"
        ]["amount"].sum()

        expenses = transactions_df[
            transactions_df["type"].astype(str).str.lower() == "expense"
        ]["amount"].sum()

        savings = income - expenses
        savings_rate = (savings / income * 100) if income > 0 else 0

        expense_data = transactions_df[
            transactions_df["type"].astype(str).str.lower() == "expense"
        ]

        category_expenses = (
            expense_data.groupby("category")["amount"]
            .sum()
            .sort_values(ascending=False)
            if not expense_data.empty
            else pd.Series(dtype=float)
        )

        # HERO
        st.markdown("""
        <div class="hero">
            <h1>Good to see you 👋</h1>
            <p>One clear view of your income, spending, savings and financial health.</p>
            <span class="hero-badge">● PERSONAL FINANCE OVERVIEW</span>
        </div>
        """, unsafe_allow_html=True)

        # KPI ROW
        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">💵 TOTAL INCOME</div>
                <div class="kpi-value">₹{income:,.2f}</div>
                <div class="kpi-note">Total money received</div>
            </div>
            """, unsafe_allow_html=True)

        with c2:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">💸 TOTAL EXPENSES</div>
                <div class="kpi-value red">₹{expenses:,.2f}</div>
                <div class="kpi-note">Total money spent</div>
            </div>
            """, unsafe_allow_html=True)

        with c3:
            saving_class = "green" if savings >= 0 else "red"
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">🏦 NET SAVINGS</div>
                <div class="kpi-value {saving_class}">₹{savings:,.2f}</div>
                <div class="kpi-note">Income minus expenses</div>
            </div>
            """, unsafe_allow_html=True)

        with c4:
            rate_class = "green" if savings_rate >= 20 else "yellow"
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">📈 SAVINGS RATE</div>
                <div class="kpi-value {rate_class}">{savings_rate:.1f}%</div>
                <div class="kpi-note">Percentage of income saved</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # MAIN ANALYTICS GRID
        left, right = st.columns([1.15, .85], gap="large")

        with left:
            with st.container(border=True):
                st.markdown('<div class="ui-card-title">📊 Spending by Category</div>', unsafe_allow_html=True)
                st.markdown('<div class="ui-card-subtitle">Where your money is going</div>', unsafe_allow_html=True)
                if not category_expenses.empty:
                    st.bar_chart(category_expenses, color="#22B8CF", height=300)
                else:
                    st.info("No expense data available.")

        with right:
            with st.container(border=True):
                st.markdown('<div class="ui-card-title">💵 Money Flow</div>', unsafe_allow_html=True)
                st.markdown('<div class="ui-card-subtitle">Income versus total spending</div>', unsafe_allow_html=True)
                flow = pd.DataFrame({"Amount": [income, expenses]}, index=["Income", "Expenses"])
                st.bar_chart(flow, color="#34D399", height=300)

        # HEALTH + TOP SPENDING
        h1, h2 = st.columns([1, 1], gap="large")

        with h1:
            with st.container(border=True):
                st.markdown('<div class="ui-card-title">❤️ Financial Health</div>', unsafe_allow_html=True)
                st.markdown('<div class="ui-card-subtitle">A simple score based on your current savings rate</div>', unsafe_allow_html=True)
                score = int(max(0, min(100, savings_rate * 2)))
                if savings_rate >= 30:
                    status, cls, msg = "Excellent", "status-good", "Strong savings behaviour."
                elif savings_rate >= 20:
                    status, cls, msg = "Healthy", "status-good", "Good savings discipline."
                elif savings_rate >= 10:
                    status, cls, msg = "Moderate", "status-warn", "There is room to improve savings."
                else:
                    status, cls, msg = "Needs Attention", "status-bad", "Expenses are putting pressure on savings."
                health_html = f'<div class="health-score"><div class="health-score-label">FINANCIAL HEALTH SCORE</div><div class="health-score-value">{score}/100</div><span class="status-pill {cls}">{status}</span><div style="color:#91A2B5;font-size:11px;margin-top:8px;">{msg}</div></div>'
                st.markdown(health_html, unsafe_allow_html=True)
                st.progress(min(max(score / 100, 0), 1))

        with h2:
            with st.container(border=True):
                st.markdown('<div class="ui-card-title">🏆 Biggest Spending Area</div>', unsafe_allow_html=True)
                st.markdown('<div class="ui-card-subtitle">The category taking the largest share of expenses</div>', unsafe_allow_html=True)
                if not category_expenses.empty:
                    top_category = category_expenses.index[0]
                    top_amount = float(category_expenses.iloc[0])
                    top_pct = top_amount / expenses * 100 if expenses > 0 else 0
                    st.metric("Top Category", str(top_category), f"{top_pct:.1f}% of expenses")
                    st.progress(min(top_pct / 100, 1))
                    st.caption(f"₹{top_amount:,.2f} spent in this category.")
                else:
                    st.info("No expense categories available.")

        # QUICK INSIGHTS
        st.markdown("""
        <div class="section-head">⚡ Quick Insights</div>
        <div class="section-caption">Small signals that help you understand your finances faster.</div>
        """, unsafe_allow_html=True)

        q1, q2, q3, q4 = st.columns(4)

        with q1:
            st.markdown(f"""
            <div class="insight-card">
                <div class="insight-icon">🧾</div>
                <div class="insight-title">{len(transactions_df)} Transactions</div>
                <div class="insight-text">Records currently stored in your finance database.</div>
            </div>
            """, unsafe_allow_html=True)

        with q2:
            category_count = len(category_expenses)
            st.markdown(f"""
            <div class="insight-card">
                <div class="insight-icon">🗂️</div>
                <div class="insight-title">{category_count} Expense Categories</div>
                <div class="insight-text">Categories currently contributing to your spending.</div>
            </div>
            """, unsafe_allow_html=True)

        with q3:
            if savings >= 0:
                insight_title = "Positive Cash Flow"
                insight_text = "Your income is currently higher than your expenses."
            else:
                insight_title = "Negative Cash Flow"
                insight_text = "Your expenses are currently higher than your income."

            st.markdown(f"""
            <div class="insight-card">
                <div class="insight-icon">{"🟢" if savings >= 0 else "🔴"}</div>
                <div class="insight-title">{insight_title}</div>
                <div class="insight-text">{insight_text}</div>
            </div>
            """, unsafe_allow_html=True)

        with q4:
            st.markdown(f"""
            <div class="insight-card">
                <div class="insight-icon">🚨</div>
                <div class="insight-title">Anomaly Monitor</div>
                <div class="insight-text">Isolation Forest module is ready for anomaly review.</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # SMART TAKEAWAY
        if not category_expenses.empty:
            top_category = category_expenses.index[0]
            top_amount = float(category_expenses.iloc[0])
            top_pct = top_amount / expenses * 100 if expenses > 0 else 0

            if top_pct > 40:
                takeaway = (
                    f"Your biggest focus area is **{top_category}**. "
                    f"It accounts for **{top_pct:.1f}%** of total expenses."
                )
            elif savings_rate >= 20:
                takeaway = (
                    f"Your finances look healthy at a **{savings_rate:.1f}% savings rate**. "
                    "Keep monitoring your largest expense categories."
                )
            else:
                takeaway = (
                    "Your next improvement opportunity is to increase your savings rate "
                    "by controlling discretionary spending."
                )

            st.markdown(f"""
            <div class="ui-card">
                <div class="ui-card-title">💡 Today's Financial Takeaway</div>
                <div class="ui-card-subtitle">A quick interpretation of your current numbers</div>
                <div style="color:#D7E2ED;font-size:14px;line-height:1.7;">{takeaway}</div>
            </div>
            """, unsafe_allow_html=True)


# ============================================================
# TRANSACTIONS
# ============================================================

elif page == "💳 Transactions":

    st.markdown('<div class="hero"><h1>💳 Transactions</h1><p>Review and explore your stored financial transactions.</p></div>', unsafe_allow_html=True)

    if transactions_df.empty:

        st.warning("No transactions available.")

    else:

        f1, f2, f3 = st.columns([1, 1, 1.5])
        with f1:
            type_filter = st.selectbox("Transaction Type", ["All", "Income", "Expense"])
        with f2:
            categories = sorted(transactions_df["category"].dropna().astype(str).unique().tolist())
            category_filter = st.selectbox("Category", ["All"] + categories)
        with f3:
            search = st.text_input("Search description", placeholder="e.g. food, salary, shopping")

        filtered = transactions_df.copy()
        if type_filter != "All":
            filtered = filtered[filtered["type"].astype(str).str.lower() == type_filter.lower()]
        if category_filter != "All":
            filtered = filtered[filtered["category"].astype(str) == category_filter]
        if search.strip():
            filtered = filtered[filtered["description"].astype(str).str.contains(search.strip(), case=False, na=False)]

        st.caption(f"Showing {len(filtered)} of {len(transactions_df)} transactions")
        st.dataframe(filtered, use_container_width=True, hide_index=True)

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
            st.metric(
                "Total Income",
                f"₹{income:,.2f}"
            )

        with col2:
            st.metric(
                "Total Expenses",
                f"₹{expenses:,.2f}"
            )


# ============================================================
# ANALYSIS
# ============================================================

elif page == "📊 Analysis":

    st.markdown('<div class="hero"><h1>📊 Financial Analytics</h1><p>Understand your spending patterns and financial performance.</p></div>', unsafe_allow_html=True)

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

        # ----------------------------------------------------
        # SUMMARY
        # ----------------------------------------------------

        st.subheader("📌 Financial Summary")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Income",
                f"₹{income:,.2f}"
            )

        with col2:
            st.metric(
                "Expenses",
                f"₹{expenses:,.2f}"
            )

        with col3:
            st.metric(
                "Savings",
                f"₹{savings:,.2f}"
            )

        st.markdown("---")

        # ----------------------------------------------------
        # CATEGORY ANALYSIS
        # ----------------------------------------------------

        if not expenses_df.empty:
            category_data = (
                expenses_df.groupby("category")["amount"]
                .sum().sort_values(ascending=False)
            )
            with st.container(border=True):
                st.markdown('<div class="ui-card-title">📊 Spending by Category</div>', unsafe_allow_html=True)
                st.markdown('<div class="ui-card-subtitle">Compare where your expenses are concentrated</div>', unsafe_allow_html=True)
                st.bar_chart(category_data, color="#22B8CF", height=330)

            highest_category = category_data.index[0]
            highest_amount = float(category_data.iloc[0])
            highest_pct = highest_amount / expenses * 100 if expenses else 0
            with st.container(border=True):
                st.markdown('<div class="ui-card-title">🏆 Highest Spending Category</div>', unsafe_allow_html=True)
                st.success(f"Your highest spending category is **{highest_category}** with **₹{highest_amount:,.2f}** ({highest_pct:.1f}% of expenses).")


# ============================================================
# BUDGET
# ============================================================

elif page == "💰 Budget":

    st.markdown('<div class="hero"><h1>💰 Budget Health</h1><p>Compare planned budgets with actual spending.</p></div>', unsafe_allow_html=True)

    try:

        budgets_df = get_budgets()

        if budgets_df.empty:

            st.warning("No budget data available.")

        else:

            expenses_df = transactions_df[
                transactions_df["type"] == "Expense"
            ]

            # ------------------------------------------------
            # CALCULATE ACTUAL SPENDING
            # ------------------------------------------------

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

            # ------------------------------------------------
            # MERGE BUDGET + SPENDING
            # ------------------------------------------------

            budget_df = budgets_df.merge(
                spent_df,
                on="category",
                how="left"
            )

            budget_df["amount"] = (
                budget_df["amount"]
                .fillna(0)
            )

            budget_df["remaining"] = (
                budget_df["budget"]
                - budget_df["amount"]
            )

            # ------------------------------------------------
            # STATUS
            # ------------------------------------------------

            def get_status(row):

                budget = row["budget"]
                spent = row["amount"]

                if budget <= 0:
                    return "⚪ No Budget"

                percentage = (
                    spent / budget
                ) * 100

                if percentage >= 100:
                    return "🔴 Over Budget"

                elif percentage >= 80:
                    return "🟡 Near Limit"

                else:
                    return "🟢 Within Budget"

            budget_df["status"] = budget_df.apply(
                get_status,
                axis=1
            )

            # ------------------------------------------------
            # DISPLAY TABLE
            # ------------------------------------------------

            st.subheader("📊 Budget Overview")

            display_df = budget_df[
                [
                    "category",
                    "budget",
                    "amount",
                    "remaining",
                    "status"
                ]
            ].copy()

            display_df.columns = [
                "Category",
                "Budget",
                "Spent",
                "Remaining",
                "Status"
            ]

            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True
            )

            st.markdown("---")

            # ------------------------------------------------
            # BUDGET VS ACTUAL
            # ------------------------------------------------

            st.subheader(
                "📈 Budget vs Actual Spending"
            )

            chart_df = budget_df[
                ["category", "budget", "amount"]
            ].copy()

            chart_df = chart_df.set_index(
                "category"
            )

            chart_df.columns = [
                "Budget",
                "Actual Spending"
            ]

            st.bar_chart(chart_df)

    except Exception as e:

        st.error(
            f"Budget analysis could not be loaded: {e}"
        )


# ============================================================
# AI FINANCIAL ADVISOR
# ============================================================

elif page == "🤖 AI Advisor":

    st.markdown('<div class="hero"><h1>🤖 Financial Advisor</h1><p>Get explainable financial recommendations based on your current data.</p></div>', unsafe_allow_html=True)

    st.write(
        "Get personalized financial recommendations "
        "based on your income and spending."
    )

    st.markdown("---")

    if st.button(
        "🧠 Generate Financial Advice",
        type="primary"
    ):

        try:

            # Generate existing Python-based advice
            generate_advice()

            # Also calculate information for display
            if not transactions_df.empty:

                income = transactions_df[
                    transactions_df["type"] == "Income"
                ]["amount"].sum()

                expenses_df = transactions_df[
                    transactions_df["type"] == "Expense"
                ]

                expenses = expenses_df["amount"].sum()

                savings = income - expenses

                if income > 0:
                    savings_rate = (
                        savings / income
                    ) * 100
                else:
                    savings_rate = 0

                st.subheader(
                    "💡 Your Financial Overview"
                )

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Income",
                        f"₹{income:,.2f}"
                    )

                with col2:
                    st.metric(
                        "Expenses",
                        f"₹{expenses:,.2f}"
                    )

                with col3:
                    st.metric(
                        "Savings Rate",
                        f"{savings_rate:.2f}%"
                    )

                st.markdown("---")

                # Savings advice
                if savings_rate >= 30:

                    st.success(
                        "✅ Excellent savings rate! "
                        "You are saving a healthy portion "
                        "of your income."
                    )

                elif savings_rate >= 20:

                    st.info(
                        "🟢 Good savings rate. "
                        "Try to maintain it consistently."
                    )

                elif savings_rate >= 10:

                    st.warning(
                        "🟡 Your savings rate is moderate. "
                        "Consider reducing unnecessary expenses."
                    )

                else:

                    st.error(
                        "🔴 Your savings rate is low. "
                        "Review your spending."
                    )

                # Highest spending category
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

                    highest_amount = (
                        category_spending.iloc[0]
                    )

                    percentage = (
                        highest_amount
                        / expenses
                        * 100
                    )

                    st.markdown("---")

                    st.subheader(
                        "📌 Spending Recommendation"
                    )

                    st.write(
                        f"Your highest spending category "
                        f"is **{highest_category}** "
                        f"with spending of "
                        f"**₹{highest_amount:,.2f}**."
                    )

                    if percentage > 40:

                        st.warning(
                            f"⚠️ {highest_category} represents "
                            f"{percentage:.1f}% of your total "
                            f"expenses. Consider reviewing "
                            f"this category."
                        )

                    else:

                        st.info(
                            f"👍 {highest_category} represents "
                            f"{percentage:.1f}% of your total "
                            f"expenses."
                        )

        except Exception as e:

            st.error(
                f"Unable to generate financial advice: {e}"
            )


# ============================================================
# FINANCE CHAT
# ============================================================

elif page == "💬 Finance Chat":

    st.markdown('<div class="hero"><h1>💬 Finance Chat</h1><p>Ask questions about your stored financial information.</p></div>', unsafe_allow_html=True)

    st.write(
        "Ask questions about your financial transactions."
    )

    st.markdown("---")

    # --------------------------------------------------------
    # CHAT HISTORY
    # --------------------------------------------------------

    if "chat_history" not in st.session_state:

        st.session_state.chat_history = []

    # --------------------------------------------------------
    # DISPLAY CHAT HISTORY
    # --------------------------------------------------------

    for message in st.session_state.chat_history:

        with st.chat_message(
            message["role"]
        ):

            st.write(
                message["content"]
            )

    # --------------------------------------------------------
    # CHAT INPUT
    # --------------------------------------------------------

    question = st.chat_input(
        "Ask something about your finances..."
    )

    if question:

        # Add user message
        st.session_state.chat_history.append(
            {
                "role": "user",
                "content": question
            }
        )

        # Display user message immediately
        with st.chat_message("user"):

            st.write(question)

        # Generate answer
        try:

            response = answer_question(
                question
            )

        except Exception as e:

            response = (
                f"Sorry, I couldn't process that "
                f"question. Error: {e}"
            )

        # Add assistant message
        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "content": response
            }
        )

        # Display assistant response
        with st.chat_message("assistant"):

            st.write(response)

    # --------------------------------------------------------
    # CLEAR CHAT
    # --------------------------------------------------------

    if st.session_state.chat_history:

        if st.button("🗑️ Clear Chat"):

            st.session_state.chat_history = []

            st.rerun()

# ============================================================
# ANOMALY DETECTION UI
# ============================================================
elif page == "🚨 Anomaly Detection":

    st.markdown("""
    <div class="hero">
        <h1>🚨 Spending Anomaly Detection</h1>
        <p>Review unusual spending patterns detected by your ML module.</p>
    </div>
    """, unsafe_allow_html=True)

    st.info("Isolation Forest anomaly detection is implemented and tested. The next integration is to connect the existing detector directly to this dashboard page.")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Expense Transactions", len(transactions_df[transactions_df["type"] == "Expense"]) if not transactions_df.empty else 0)
    with c2:
        st.metric("Detection Method", "Isolation Forest")
    with c3:
        st.metric("Status", "Model Ready")

    st.markdown("### 🔍 What this module does")
    st.write("The anomaly detector identifies transactions that differ significantly from normal spending patterns without requiring manually labelled anomaly data.")
    st.warning("The detector itself remains in src/anomaly_detection.py. This UI page does not duplicate or change its ML logic.")

