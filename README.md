# 💰 AI Personal Finance Assistant

A FinTech-focused personal finance analytics application built with **Python, SQLite, Pandas, Machine Learning, Streamlit, and an LLM-ready Finance Chat architecture**.

The application helps users understand income, expenses, savings, budgets, spending patterns, financial recommendations, expense prediction, and unusual spending behavior through an interactive dashboard.

## 📌 Project Status

**Current Stage: Portfolio-Ready FinTech MVP + LLM-Ready Finance Chat**

### Implemented

- ✅ SQLite financial database
- ✅ Transaction management
- ✅ Budget management
- ✅ Financial analysis
- ✅ Income and expense summaries
- ✅ Savings and savings-rate calculation
- ✅ Spending-by-category analysis
- ✅ Rule-based financial recommendation engine
- ✅ AI Financial Advisor
- ✅ Finance Chat Assistant
- ✅ Machine Learning expense prediction
- ✅ Spending anomaly detection
- ✅ Interactive Streamlit dashboard
- ✅ FinTech-style dark UI/UX
- ✅ Sidebar navigation
- ✅ KPI cards and financial charts
- ✅ Interactive transaction/budget views
- ✅ Finance Chat interface
- ✅ Secure `.env` configuration
- ✅ LLM client architecture with local Mock LLM mode

### Current LLM Mode

The project is **LLM-ready** and currently uses:

```env
MOCK_LLM=true
```

This allows development and demonstration without API credits. When live API access is available, the same architecture can switch to live LLM calls through environment configuration.

## 🎯 Objectives

1. Store financial transactions in a structured relational database.
2. Analyze income and expenses.
3. Calculate savings and savings rate.
4. Track spending by category.
5. Compare budgets with actual spending.
6. Generate explainable financial recommendations.
7. Provide an AI-style financial advisor.
8. Allow users to ask questions about their financial data.
9. Predict future expense behavior using Machine Learning.
10. Detect unusual spending patterns.
11. Present financial information through a professional dashboard.
12. Provide an extensible LLM integration layer for natural-language financial assistance.

## 🏗️ Project Architecture

```text
                         ┌──────────────┐
                         │     User     │
                         └──────┬───────┘
                                │
                                ▼
                    ┌──────────────────────┐
                    │    Streamlit UI      │
                    │       app.py         │
                    └──────────┬───────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
       ┌────────────┐   ┌──────────────┐  ┌───────────────┐
       │ Dashboard  │   │ Transactions │  │    Budget     │
       └─────┬──────┘   └──────┬───────┘  └──────┬────────┘
             │                 │                 │
             └─────────────────┼─────────────────┘
                               ▼
                    ┌──────────────────────┐
                    │   SQLite Database    │
                    │    data/finance.db   │
                    └──────────┬───────────┘
                               │
                ┌──────────────┼─────────────────┐
                │              │                 │
                ▼              ▼                 ▼
        ┌─────────────┐ ┌──────────────┐ ┌──────────────────┐
        │   Pandas    │ │ Rule-Based   │ │ ML / Analytics   │
        │ Data Analysis│ │ AI Advisor   │ │ Modules          │
        └──────┬──────┘ └──────┬───────┘ └────────┬─────────┘
               │               │                  │
               │               │          ┌───────┴────────┐
               │               │          ▼                ▼
               │               │   Expense Prediction  Anomaly Detection
               │               │
               └───────────────┼──────────────────────────┐
                               ▼                          │
                    ┌──────────────────────┐              │
                    │    Finance Chat      │◄─────────────┘
                    │ finance_chat.py      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Financial Summary    │
                    │ + User Question      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │     LLM Layer        │
                    │   llm_client.py      │
                    ├──────────────────────┤
                    │ Mock LLM             │
                    │        OR            │
                    │ Live OpenAI API      │
                    └──────────┬───────────┘
                               │
                               ▼
                    Natural-Language Answer
```

## 🧩 Main Modules

### 1. 🏠 Dashboard

Provides a quick overview of the user's financial condition:

- Total income
- Total expenses
- Net savings
- Savings rate
- Expenses by category
- Income vs expenses
- Highest spending category
- Financial health indicators
- KPI cards and FinTech-style layout

### 2. 💳 Transactions

Displays stored financial transactions including:

- Transaction ID
- Type
- Category
- Description
- Amount

### 3. 📊 Financial Analysis

Used to understand spending behavior through:

- Category-wise expenses
- Total income
- Total expenses
- Savings
- Spending distribution
- Highest spending category
- Financial summaries
- Visual charts

### 4. 💰 Budget Management

Compares planned spending with actual spending.

Budget status:

```text
🟢 Within Budget
🟡 Near Limit
🔴 Over Budget
⚪ No Budget
```

The module calculates:

```text
Remaining = Budget - Actual Spending
```

### 5. 🤖 AI Financial Advisor

Provides explainable recommendations based on:

- Income
- Expenses
- Savings
- Savings rate
- Highest spending category
- Spending percentage

Example rule-based logic:

```text
Savings Rate >= 30% → Excellent
Savings Rate >= 20% → Good
Savings Rate >= 10% → Moderate
Savings Rate < 10%  → Low
```

The rule-based approach is transparent and easy to explain in an interview.

### 6. 💬 Finance Chat Assistant

Users can ask questions such as:

```text
How much did I spend?
How much did I earn?
What is my highest spending category?
What is my savings rate?
Give me a short summary of my financial situation.
```

Flow:

```text
User Question
      ↓
finance_chat.py
      ↓
SQLite Financial Data
      ↓
Financial Summary
      ↓
Rule-Based Answer
      │
      └── Unsupported question
                  ↓
             LLM Layer
                  ↓
          Mock / Live LLM
                  ↓
          Natural-Language Answer
```

Known financial questions are answered deterministically. Broader questions use an aggregated financial summary as LLM context.

### 7. 🧠 LLM Integration Layer

Dedicated files:

```text
src/llm_client.py
src/config.py
```

Environment configuration:

```env
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-5.6
MOCK_LLM=true
```

`MOCK_LLM=true` enables local development without making an external API request.

When live API access is available:

```env
MOCK_LLM=false
```

The source code does not contain the API key.

### 8. 📈 Machine Learning Expense Prediction

The project contains an ML expense prediction module using engineered historical features such as:

```text
date
amount
day_of_week
day_of_month
month
previous_day_expense
previous_7_day_expense
rolling_7_day_avg
```

Feature engineering includes previous-day expense, previous-7-day expense, rolling 7-day average, day of week, day of month, and month.

### 9. 🚨 Spending Anomaly Detection

The project contains an **Isolation Forest** anomaly detection module.

It identifies transactions that differ significantly from normal spending behavior and can classify transactions as:

```text
✅ Normal
🚨 Anomaly
```

The ML logic is kept separately in:

```text
src/anomaly_detection.py
```

## 🗄️ Database

The application uses SQLite:

```text
data/finance.db
```

Transactions contain fields such as:

```text
id
date
type
category
description
amount
payment_method
```

Budgets contain:

```text
id
category
budget
```

SQLite is lightweight, serverless, SQL-based, and suitable for a local portfolio/MVP application.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| SQLite | Financial data storage |
| SQL | Database querying |
| Pandas | Data processing and analysis |
| Scikit-learn | Machine Learning / anomaly detection |
| Streamlit | Interactive web dashboard |
| OpenAI SDK | LLM integration layer |
| python-dotenv | Environment variable management |
| Git & GitHub | Version control and hosting |

## 📁 Project Structure

```text
AI Personal Finance Assistant/
│
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── finance.db
│   ├── transactions.csv
│   └── budgets.csv
│
└── src/
    ├── __init__.py
    ├── database.py
    ├── analysis.py
    ├── budget.py
    ├── recommendations.py
    ├── ai_advisor.py
    ├── finance_chat.py
    ├── ml_expense_prediction.py
    ├── anomaly_detection.py
    ├── transactions.py
    ├── utils.py
    ├── main.py
    ├── config.py
    └── llm_client.py
```

`.env` remains local and is excluded from Git.

## ▶️ How to Run

```powershell
git clone https://github.com/arka829636/ai-personal-finance-assistant.git
cd ai-personal-finance-assistant
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create a local `.env`:

```env
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-5.6
MOCK_LLM=true
```

Run:

```powershell
streamlit run app.py
```

## 🔐 Security

- API keys are loaded through environment variables.
- `.env` is excluded from Git.
- API keys are not hard-coded in source files.
- Production deployment would additionally require authentication, authorization, secure secret management, input validation, database access controls, encryption, API security, logging, and secure financial-data handling.

## 🧪 Testing Performed

- Database inspection
- Transaction data verification
- Budget data verification
- Dashboard execution
- Financial calculation verification
- Finance Chat testing
- Rule-based question testing
- Mock LLM integration testing
- Streamlit UI testing
- Git/GitHub verification
- `.env` ignore verification

## ⚠️ Current Limitations

This is a portfolio/MVP application, not a production banking system.

- Local SQLite database
- No user authentication
- No multi-user account management
- Live LLM usage requires API access/credits
- Mock LLM is used during no-credit development
- Anomaly detection is implemented as a separate ML module
- Additional production security would be required
- Financial recommendations are informational and not professional financial advice

## 🚀 Future Improvements

1. Enable live LLM access when API credits are available.
2. Improve natural-language financial querying.
3. Add authentication and user accounts.
4. Move to PostgreSQL for production use.
5. Add recurring transaction detection.
6. Add monthly financial reports.
7. Add automated budget alerts.
8. Add richer anomaly explanations.
9. Add model evaluation for expense prediction.
10. Add cloud deployment.
11. Add automated tests and CI/CD.
12. Add encrypted financial-data storage.

## 💼 Resume Description

**AI Personal Finance Assistant | Python, SQLite, Pandas, ML, Streamlit**

- Built a FinTech-focused personal finance application using Python, SQLite, Pandas and Streamlit to analyze income, expenses, savings, budgets and spending patterns through an interactive dashboard.
- Implemented ML-based expense prediction, Isolation Forest spending anomaly detection, rule-based financial recommendations and an LLM-ready Finance Chat architecture with secure environment-based API configuration.

## 🎤 Interview Summary

> I built an AI-powered personal finance assistant that stores financial transactions in SQLite, processes them using Pandas, provides financial analytics and recommendations through Streamlit, predicts expense behavior using Machine Learning, detects unusual spending using Isolation Forest, and includes an LLM-ready Finance Chat architecture for natural-language financial queries.

## 📌 Important Note

The project currently uses a **local Mock LLM mode** for development because live API access is optional. The architecture is designed so live LLM access can be enabled through environment configuration without changing the core financial-data pipeline.
