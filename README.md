# 💰 FinanceAI — AI Personal Finance Assistant

> A portfolio-ready personal finance management application built with Python, Streamlit, SQLite, Pandas, Machine Learning, Anomaly Detection, Rule-Based AI, and an LLM integration layer.

## 🚀 Live Demo

https://ai-personal-finance-assistantt.streamlit.app/

## 💻 GitHub Repository

`https://github.com/arka829636/ai-personal-finance-assistant`

---

## 📌 Project Overview

FinanceAI is an AI-assisted personal finance management application designed to help users understand, monitor, and analyze their financial activity.

The application combines traditional financial analytics with machine learning, anomaly detection, rule-based recommendations, conversational finance features, and an LLM integration layer.

### Main Objectives

- Record income and expenses
- Add, edit, and delete transactions
- Analyze spending patterns
- Track budgets
- Calculate savings
- Identify unusual spending
- Predict the next expense
- Generate rule-based financial recommendations
- Answer financial questions through Finance Chat
- Provide an LLM integration layer
- Present financial information through an interactive FinTech dashboard

---

# ✨ Features

## 1. 📊 Dashboard

The Dashboard provides a high-level financial overview:

- Total income
- Total expenses
- Net savings
- Savings rate
- Total transactions
- Expense transactions
- Average expense
- Top spending category
- Monthly income
- Category-wise expenses
- Income vs expense trends

### Example Demo Metrics

| Metric | Value |
|---|---:|
| Total Income | ₹130,000 |
| Total Expenses | ₹102,714.10 |
| Net Savings | ₹27,285.90 |
| Savings Rate | 21.0% |
| Total Transactions | 197 |
| Expense Transactions | 192 |
| Average Expense | ₹534.97 |
| Top Category | Shopping |

---

## 2. 💳 Transactions — Full CRUD

The Transactions page supports:

- Create/add transaction
- Read/view transactions
- Update/edit transaction
- Delete transaction
- Income/expense type
- Category
- Description
- Amount
- Payment method
- Transaction date

### CRUD Flow

```text
CREATE → INSERT into SQLite
READ   → SELECT from SQLite
UPDATE → UPDATE selected transaction
DELETE → DELETE selected transaction
```

Database operations use parameterized SQL queries.

---

## 3. 📈 Financial Analysis

The Analysis page provides:

- Income analysis
- Expense analysis
- Net savings
- Savings rate
- Category-wise spending
- Expense distribution
- Income vs expense comparison
- Financial trend visualization

Pandas is used for analysis and Plotly for interactive visualization.

---

## 4. 💰 Budget Management

The Budget page compares planned spending against actual spending.

### Budget Metrics

- Total budget
- Actual spending
- Remaining budget
- Usage percentage
- Category-wise utilization
- Budget status

Possible statuses:

```text
Within Budget
Near Limit
Over Budget
```

### Demo Scenarios

#### May 2026 — Shopping

```text
Period: May 1–31, 2026
Budget: ₹7,284.19
Actual: ₹8,093.54
Over by: ₹809.35
Usage: 111%
Status: Over Budget
```

#### July 2026 — Education

```text
Period: July 1–31, 2026
Budget: ₹8,195.08
Actual: ₹9,105.65
Over by: ₹910.57
Usage: 111%
Status: Over Budget
```

These are intentional presentation scenarios and do not modify underlying aggregate transaction totals.

---

## 5. 🤖 AI Financial Advisor

The AI Advisor is a rule-based recommendation system.

It analyzes:

- Income
- Expenses
- Savings
- Savings rate
- Average expense
- Category spending
- Budget utilization

Because the recommendations are rule-based, the behavior is deterministic and explainable.

---

# 6. 📊 Machine Learning — Expense Prediction

The project uses a **Random Forest Regressor** to predict the next expense.

### Features

- Day of week
- Day of month
- Month
- Previous day expense
- Previous 7-transaction expense
- Rolling 7-transaction average

> The seven-transaction feature represents a historical transaction window, not seven calendar days.

### Model Configuration

```text
Algorithm: RandomForestRegressor
Estimators: 200
Max Depth: 8
Random State: 42
Train/Test Split: 80/20 chronological split
```

### Evaluation Metrics

- MAE
- RMSE
- R²

### Prediction Pipeline

```text
Historical Transactions
        ↓
Data Preparation
        ↓
Feature Engineering
        ↓
Random Forest
        ↓
Prediction
        ↓
Predicted Next Expense
```

The deployed demo has been tested with a prediction of approximately **₹386.46**.

---

# 7. 🚨 Anomaly Detection

The project uses **Isolation Forest** for unsupervised expense anomaly detection.

### Configuration

```text
Algorithm: Isolation Forest
Contamination: 0.05
Random State: 42
Input: Expense Amount
```

The model does not require labeled anomalies.

### Current Demo Result

```text
Expense Transactions: 192
Anomalies: 10
Normal Transactions: 182
Anomaly Rate: 5.2%
```

Flagged demo categories include:

- Bills
- Shopping
- Food

### Detection Pipeline

```text
Expense Transactions
        ↓
Expense Amount
        ↓
Isolation Forest
        ↓
Normal / Anomaly
        ↓
Visualization
```

---

# 8. 💬 Finance Chat

Finance Chat provides a conversational interface for financial questions.

The system combines:

1. Rule-based intent detection
2. Deterministic financial calculations
3. Retrieved financial context
4. LLM fallback for unsupported/general questions

### Supported Intents

```text
Income
Expenses
Savings
Category
Prediction
Anomaly
Comparison
General
```

### Example Questions

```text
How much income do I have?
How much did I spend?
How much am I saving?
What is my biggest expense category?
Predict my next expense.
Show me unusual transactions.
Compare my income and expenses.
```

---

# 9. 🧠 Rule-Based Intent Detection

Structured financial questions are answered deterministically before using the LLM.

Example:

```text
User:
How much income do I have?

Response:
Your total income is ₹130,000.00.

Detected Intent:
Income
```

Example:

```text
User:
Predict my next expense.

Response:
Your predicted next expense is approximately ₹386.46.

Detected Intent:
Expense Prediction
```

This reduces unnecessary LLM calls and keeps structured financial answers consistent.

---

# 10. 🧩 LLM Integration Layer

The project contains a dedicated LLM abstraction layer supporting:

```text
Mock LLM
    OR
Live OpenAI API
```

The application can run in local/demo mode without an API key.

### Configuration Example

```env
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-5.6
MOCK_LLM=true
```

For development without API credits:

```env
MOCK_LLM=true
```

API keys should never be committed to GitHub.

### Interview Explanation

> I implemented an LLM integration layer with secure API-key configuration and a local mock mode for development. The application can switch to live LLM calls when API access is available.

---

# 🏗️ System Architecture

```text
                         ┌─────────────────────┐
                         │        User         │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   Streamlit UI      │
                         │      app.py         │
                         └──────────┬──────────┘
                                    │
             ┌──────────────────────┼──────────────────────┐
             │                      │                      │
             ▼                      ▼                      ▼
      ┌────────────┐         ┌────────────┐        ┌──────────────┐
      │Transactions│         │  Analysis  │        │    Budget    │
      └─────┬──────┘         └──────┬─────┘        └──────┬───────┘
            │                       │                     │
            └───────────────────────┼─────────────────────┘
                                    ▼
                         ┌─────────────────────┐
                         │   SQLite Database   │
                         └──────────┬──────────┘
                                    │
                    ┌───────────────┼────────────────┐
                    │               │                │
                    ▼               ▼                ▼
              ┌──────────┐   ┌────────────┐   ┌──────────────┐
              │  Pandas  │   │ Rule-Based │   │    Budget    │
              │ Analysis │   │ AI Advisor │   │   Analysis   │
              └────┬─────┘   └────────────┘   └──────────────┘
                   │
          ┌────────┴─────────┐
          │                  │
          ▼                  ▼
 ┌─────────────────┐  ┌──────────────────┐
 │ Random Forest   │  │ Isolation Forest │
 │ Expense         │  │ Anomaly          │
 │ Prediction      │  │ Detection        │
 └────────┬────────┘  └────────┬─────────┘
          │                    │
          └──────────┬─────────┘
                     ▼
             ┌───────────────┐
             │ Finance Chat  │
             └───────┬───────┘
                     │
                     ▼
             ┌───────────────┐
             │ LLM Layer     │
             │ Mock / OpenAI │
             └───────────────┘
```

---

# 🔄 Finance Chat Data Flow

```text
User Question
      ↓
Intent Detection
      ↓
Structured Query?
      │
      ├── YES → Database / Analysis / ML
      │                    ↓
      │             Deterministic Answer
      │
      └── NO  → Financial Context
                         ↓
                    LLM Layer
                         ↓
                    AI Response
```

---

# 🗄️ Database

The project uses SQLite.

## Transactions Schema

```sql
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    type TEXT NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    amount REAL NOT NULL,
    payment_method TEXT
);
```

### Fields

| Field | Description |
|---|---|
| `id` | Unique transaction ID |
| `date` | Transaction date |
| `type` | Income or Expense |
| `category` | Transaction category |
| `description` | Transaction description |
| `amount` | Transaction amount |
| `payment_method` | Payment method |

### Database Safety

Parameterized SQL is used for CRUD operations.

```python
connection.execute(
    "DELETE FROM transactions WHERE id = ?",
    (int(transaction_id),),
)
```

Transactions are committed after successful operations and rolled back on exceptions.

---

# 📂 Project Structure

```text
ai-personal-finance-assistant/
│
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── transactions.csv
│   ├── budgets.csv
│   └── finance.db
│
├── src/
│   ├── database.py
│   ├── analysis.py
│   ├── budget.py
│   ├── recommendations.py
│   ├── ai_advisor.py
│   ├── finance_chat.py
│   ├── llm_client.py
│   ├── config.py
│   ├── ml_expense_prediction.py
│   ├── anomaly_detection.py
│   ├── transactions.py
│   ├── utils.py
│   └── main.py
│
└── tests/
    └── test_core.py
```

> `finance.db` is a runtime database. Fresh environments can initialize the database from the CSV dataset.

---

# 🧩 Module Responsibilities

| File | Responsibility |
|---|---|
| `app.py` | Streamlit UI and application flow |
| `database.py` | SQLite connection, initialization and DB operations |
| `analysis.py` | Financial calculations and analysis |
| `budget.py` | Budget calculations |
| `recommendations.py` | Recommendation rules |
| `ai_advisor.py` | AI Advisor |
| `finance_chat.py` | Finance Chat and intent detection |
| `llm_client.py` | Mock/OpenAI LLM layer |
| `config.py` | Environment configuration |
| `ml_expense_prediction.py` | Random Forest prediction |
| `anomaly_detection.py` | Isolation Forest |
| `transactions.py` | Transaction operations |
| `utils.py` | Utility functions |
| `main.py` | Application/module support |

---

# 🛠️ Technology Stack

| Area | Technology |
|---|---|
| Language | Python |
| Web UI | Streamlit |
| Data Analysis | Pandas, NumPy |
| Visualization | Plotly |
| Database | SQLite, SQL |
| ML | Scikit-learn |
| Regression | Random Forest |
| Anomaly Detection | Isolation Forest |
| AI | Rule-based AI |
| LLM | OpenAI API + Mock LLM |
| Configuration | python-dotenv |
| Version Control | Git, GitHub |
| Deployment | Streamlit Community Cloud |

---

# 📊 Demo Dataset

```text
Total Transactions: 197
Expense Transactions: 192
Income Transactions: 5
Total Income: ₹130,000
Total Expenses: ₹102,714.10
Savings: ₹27,285.90
Savings Rate: 21.0%
```

## Monthly Income

| Month | Income |
|---|---:|
| May 2026 | ₹20,000 |
| June 2026 | ₹23,000 |
| July 2026 | ₹25,000 |
| August 2026 | ₹32,000 |
| September 2026 | ₹30,000 |
| **Total** | **₹130,000** |

## Expense Categories

| Category | Amount |
|---|---:|
| Shopping | ₹21,274.29 |
| Bills | ₹20,408.83 |
| Education | ₹19,900.85 |
| Healthcare | ₹13,814.35 |
| Entertainment | ₹12,521.87 |
| Food | ₹10,325.04 |
| Transport | ₹4,468.87 |
| **Total** | **₹102,714.10** |

---

# 📦 Budget Demo Data

```text
Total Budget: ₹106,186.99
Actual Spending: ₹68,490.92
Remaining: ₹37,696.07
Usage: 64.5%
```

| Category | Budget | Actual | Remaining | Usage |
|---|---:|---:|---:|---:|
| Education | ₹22,855.61 | ₹19,900.85 | ₹2,954.76 | 87% |
| Entertainment | ₹20,133.31 | ₹12,521.87 | ₹7,611.44 | 62% |
| Food | ₹18,972.90 | ₹10,325.04 | ₹8,647.86 | 54% |
| Shopping | ₹39,092.77 | ₹21,274.29 | ₹17,818.48 | 54% |
| Transport | ₹5,132.40 | ₹4,468.87 | ₹663.53 | 87% |

The budget demonstration covers selected categories; other expense categories account for the difference between budget actuals and total expenses.

---

# 🧪 Testing

The project includes automated tests covering:

- Anomaly detection
- ML dataset preparation
- ML training
- Financial summary
- Finance Chat intent detection
- Mock LLM financial context

Current test result:

```text
6 tests passed
```

Run:

```bash
pytest
```

---

# 🔧 Installation

## 1. Clone

```bash
git clone https://github.com/arka829636/ai-personal-finance-assistant.git
cd ai-personal-finance-assistant
```

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure Environment

Optional `.env`:

```env
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-5.6
MOCK_LLM=true
```

For development without API credits:

```env
MOCK_LLM=true
```

## 5. Run

```bash
streamlit run app.py
```

Local application:

```text
http://localhost:8501
```

---

# ☁️ Streamlit Deployment

The deployed application uses:

```text
Repository: arka829636/ai-personal-finance-assistant
Branch: main
Entrypoint: app.py
```

The repository contains the CSV demo dataset used to initialize fresh runtime database state.

---

# 🔒 Security

- API keys are stored in environment variables or Streamlit secrets.
- `.env` and `.streamlit/secrets.toml` are excluded from Git.
- Runtime SQLite data is excluded from version control where appropriate.
- SQL operations use parameterized queries.
- LLM configuration is separated from application logic.

Never commit:

```text
.env
.streamlit/secrets.toml
API keys
private credentials
```

---

# 📚 Learning Outcomes

### Python

- Functions
- Modules
- Exception handling
- Environment configuration

### SQL

- SELECT
- INSERT
- UPDATE
- DELETE
- Parameterized queries
- Transactions

### Data Science

- Data cleaning
- Aggregation
- Feature engineering
- Visualization
- Financial analytics

### Machine Learning

- Regression
- Feature engineering
- Train/test splitting
- Model evaluation
- Unsupervised anomaly detection

### AI

- Rule-based systems
- Intent detection
- LLM integration
- Context construction

### Software Development

- Modular architecture
- CRUD
- Testing
- Git/GitHub
- Cloud deployment

---

# 🧠 Why Rule-Based AI + ML + LLM?

Different tasks are handled by the most appropriate component.

```text
Exact Financial Calculation
        ↓
Database + Rule-Based Logic

Prediction
        ↓
Machine Learning

Anomaly Detection
        ↓
Isolation Forest

Natural-Language Interaction
        ↓
LLM
```

Structured financial calculations remain deterministic instead of asking an LLM to calculate values that can be obtained directly from the database.

---

# ⚠️ Current Limitations

This version is primarily a portfolio/demo application.

- SQLite is intended for local/demo use.
- Authentication is not yet implemented.
- The current architecture is primarily single-user/demo oriented.
- Live LLM functionality requires API access.
- Expense prediction depends on historical data availability.
- Current anomaly detection focuses on expense amounts.
- Budget scenarios include intentional demonstration cases.
- Financial recommendations are informational and are not professional financial advice.

---

# 🔮 Future AI Improvements

## RAG

```text
User Question
      ↓
Retriever
      ↓
Trusted Financial Knowledge
      ↓
Relevant Context
      ↓
LLM
      ↓
Answer
```

## Advanced Expense Prediction

Potential improvements:

- More historical features
- Category-specific models
- Time-series models
- Seasonal patterns
- Recurring expense detection

## Better Anomaly Detection

Future features:

- Amount
- Category
- Frequency
- Merchant
- Payment method
- Time
- User-specific behavior

## Personalized AI

Future versions can provide personalized financial explanations and recommendations while maintaining appropriate privacy and authorization controls.

---

# 📝 Disclaimer

FinanceAI is an educational and portfolio project.

Financial information, recommendations, predictions, and AI-generated responses are for demonstration and informational purposes only and should not be treated as professional financial, investment, tax, or legal advice.

---

# 👨‍💻 Author

**Arka Mondal**

MCA Student

Interests:

- Data Analytics
- Data Science
- Machine Learning
- Backend Development
- AI / GenAI
- RAG
- FinTech

GitHub:

`https://github.com/arka829636`

---

# 📌 Project Summary

```text
FinanceAI
│
├── Transaction Management
│   ├── Add
│   ├── Read
│   ├── Update
│   └── Delete
│
├── Financial Analytics
│   ├── Income
│   ├── Expenses
│   ├── Savings
│   └── Category Analysis
│
├── Budget Management
│
├── Rule-Based AI Advisor
│
├── Machine Learning
│   └── Random Forest Expense Prediction
│
├── Anomaly Detection
│   └── Isolation Forest
│
├── Finance Chat
│   └── Intent Detection
│
├── LLM Integration
│   ├── Mock LLM
│   └── OpenAI API
│
├── Database
│   └── SQLite
│
├── Testing
│
└── Deployment
    └── Streamlit Community Cloud
```

---

## 🚀 Current Status

```text
Dashboard                 ✅
Transactions CRUD         ✅
Financial Analysis        ✅
Budget Management         ✅
AI Advisor                ✅
Random Forest ML          ✅
Anomaly Detection         ✅
Finance Chat              ✅
Intent Detection          ✅
LLM Integration Layer     ✅
Mock LLM                  ✅
Automated Tests           ✅
GitHub                    ✅
Streamlit Deployment     ✅
Authentication            🔜
FastAPI                   🔜
PostgreSQL                🔜
Flutter Mobile/Desktop    🔜
RAG                       🔜
```

---

⭐ **FinanceAI — turning personal financial data into understandable insights using analytics, machine learning, anomaly detection, and AI.**
