# 💰 AI Personal Finance Assistant

A **FinTech-focused personal finance analytics application** built with Python, SQLite, Pandas, Machine Learning, and Streamlit.

The project helps users understand their **income, expenses, savings, budgets, spending patterns, financial recommendations, expense predictions, and unusual spending behavior** through an interactive dashboard.

---

## 📌 Project Status

### Current Stage: Portfolio-Ready MVP + Enhanced UI/UX

The project currently includes:

- ✅ SQLite financial database
- ✅ Transaction management
- ✅ Budget management
- ✅ Financial analysis
- ✅ Income & expense summaries
- ✅ Savings calculation
- ✅ Savings-rate analysis
- ✅ Spending-by-category analysis
- ✅ Rule-based financial recommendation engine
- ✅ AI Financial Advisor module
- ✅ Finance Chat Assistant
- ✅ Machine Learning expense prediction
- ✅ Spending anomaly detection
- ✅ Interactive Streamlit dashboard
- ✅ Premium FinTech-style UI/UX
- ✅ Sidebar navigation
- ✅ KPI cards
- ✅ Financial insights
- ✅ Interactive transaction filtering
- ✅ Improved chart/card layout
- ✅ README and project documentation

The project is intentionally stopped at the **anomaly detection stage** for the current version.

---

# 🎯 Objectives

The main objectives of this project are to:

1. Store financial transactions in a structured database.
2. Analyze income and expenses.
3. Calculate savings and savings rate.
4. Track spending by category.
5. Compare budgets with actual spending.
6. Generate personalized financial recommendations.
7. Provide an AI-style financial advisor.
8. Allow users to ask questions about their transactions.
9. Predict future expense behavior using Machine Learning.
10. Detect unusual spending patterns using anomaly detection.
11. Present financial information through a professional dashboard.

---

# 🏗️ Project Architecture

```text
                         ┌──────────────────────────┐
                         │        User              │
                         └────────────┬─────────────┘
                                      │
                                      ▼
                    ┌───────────────────────────────┐
                    │       Streamlit UI            │
                    │           app.py               │
                    │                               │
                    │ Dashboard                     │
                    │ Transactions                  │
                    │ Analysis                      │
                    │ Budget                        │
                    │ AI Advisor                    │
                    │ Finance Chat                  │
                    │ Anomaly Detection             │
                    └───────────────┬───────────────┘
                                    │
                ┌───────────────────┼───────────────────┐
                │                   │                   │
                ▼                   ▼                   ▼
       ┌────────────────┐  ┌────────────────┐  ┌────────────────┐
       │ SQLite Database│  │ Pandas         │  │ ML / Analytics │
       │ finance.db     │  │ Data Analysis  │  │ Modules        │
       └───────┬────────┘  └────────────────┘  └───────┬────────┘
               │                                        │
               ▼                                        ▼
       ┌────────────────┐                     ┌──────────────────┐
       │ Transactions   │                     │ Expense          │
       │ Budgets        │                     │ Prediction       │
       └────────────────┘                     │ Anomaly Detection│
                                              └──────────────────┘
                                                        │
                                                        ▼
                                           ┌─────────────────────┐
                                           │ Financial Insights  │
                                           │ Recommendations     │
                                           └─────────────────────┘
```

---

# 🧩 Main Application Modules

## 1. Dashboard

The main dashboard provides a quick overview of the user's financial condition.

### Features

- Total income
- Total expenses
- Net savings
- Savings rate
- Spending by category
- Money flow visualization
- Highest spending category
- Financial insights
- Financial health indicators
- Premium FinTech dashboard layout

The dashboard was upgraded with a **dark FinTech visual theme, gradient hero section, KPI cards, content cards, improved spacing, hover effects, and better visual hierarchy**.

---

## 2. Transactions

The Transactions section displays stored financial transactions.

### Information includes

- Transaction ID
- Type
- Category
- Description
- Amount
- Date/payment information where available

### UI improvements

The upgraded interface supports easier exploration using filters and search-oriented controls.

---

## 3. Financial Analysis

The Analysis section is used to understand spending behavior.

Examples of analysis include:

- Category-wise expenses
- Total income
- Total expenses
- Savings
- Spending distribution
- Financial summaries
- Visual charts

Pandas is used to process and aggregate financial data.

---

## 4. Budget Analysis

The Budget module compares:

```text
Budget Amount
      ↓
Actual Spending
      ↓
Remaining Amount
      ↓
Budget Status
```

The system can identify categories that are:

- 🟢 Within Budget
- 🟡 Near Limit
- 🔴 Over Budget

This gives the user a practical way to monitor spending against planned budgets.

---

# 🤖 5. AI Financial Advisor

The AI Financial Advisor analyzes financial information and provides recommendations.

It considers information such as:

- Income
- Expenses
- Savings
- Savings rate
- Highest spending category
- Spending percentage

The current recommendation logic is primarily **rule-based financial analysis**, making it transparent and easy to explain during an interview.

Example logic:

```text
Savings Rate >= 30%
        ↓
Excellent Savings Rate

Savings Rate >= 20%
        ↓
Good Savings Rate

Savings Rate >= 10%
        ↓
Moderate Savings Rate

Savings Rate < 10%
        ↓
Review Spending
```

---

# 💬 6. Finance Chat Assistant

The project includes a Finance Chat component that works with stored financial transaction data.

Users can ask questions related to their financial transactions.

Example questions:

```text
How much did I spend?

What is my highest spending category?

How much did I earn?

How much did I save?
```

This module demonstrates the foundation for future **Natural Language → Financial Data Querying** capabilities.

---

# 📈 7. Machine Learning Expense Prediction

The project includes an ML-based expense prediction module.

The dataset contains engineered features such as:

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

These features are created from historical expense data.

### Feature Engineering

Historical transactions are transformed into useful predictive features such as:

- Previous day's expense
- Previous 7-day expense
- Rolling 7-day average
- Day of week
- Day of month
- Month

This provides a foundation for predicting future expense behavior.

---

# 🚨 8. Spending Anomaly Detection

The project includes a spending anomaly detection module.

Its purpose is to identify transactions that significantly differ from normal spending behavior.

The output classifies transactions into categories such as:

```text
✅ Normal
🚨 Anomaly
```

Example:

```text
Date        Category       Amount       Status
------------------------------------------------
2026-05-11  Food           ₹268.33      ✅ Normal
2026-05-13  Bills          ₹2961.59     🚨 Anomaly
```

The system also reports:

- Total expense transactions
- Number of anomalies
- All analyzed transactions
- Category
- Amount
- Anomaly status

This is an important FinTech feature because unusual transactions can be flagged for further review.

---

# 🗄️ Database

The project uses **SQLite** as the local relational database.

Main database:

```text
data/finance.db
```

The database stores financial information such as:

### Transactions

```text
id
date
type
category
description
amount
payment_method
```

### Budgets

```text
id
category
budget
```

SQLite is useful for this project because it is:

- Lightweight
- Serverless
- Easy to develop with
- SQL-based
- Suitable for a local MVP

---

# 🛠️ Technologies Used

## Programming Language

- **Python**

## Frontend / UI

- **Streamlit**
- HTML/CSS styling through Streamlit components

## Database

- **SQLite**
- SQL

## Data Analysis

- **Pandas**

## Machine Learning

- Python ML/data-processing ecosystem
- Feature engineering for expense prediction
- Anomaly detection

## Visualization

- Streamlit charting / data visualization
- Pandas-based analysis

## Development Tools

- Visual Studio Code
- Python Virtual Environment (`venv`)
- PowerShell / Terminal
- Git/GitHub can be used for version control

---

# 📦 Python Libraries

The project uses libraries such as:

```text
streamlit
pandas
numpy
scikit-learn
```

Additional packages may be present in `requirements.txt` depending on the installed version of the project.

Install dependencies using:

```bash
pip install -r requirements.txt
```

---

# 📁 Project Structure

```text
AI Personal Finance Assistant/
│
├── app.py
├── README.md
├── requirements.txt
├── .env
│
├── data/
│   ├── finance.db
│   ├── transactions.csv
│   └── budgets.csv
│
├── src/
│   ├── __init__.py
│   ├── database.py
│   ├── analysis.py
│   ├── budget.py
│   ├── recommendations.py
│   ├── ai_advisor.py
│   ├── finance_chat.py
│   ├── ml_expense_prediction.py
│   ├── anomaly_detection.py
│   ├── transactions.py
│   ├── utils.py
│   └── main.py
│
└── venv/
```

---

# ▶️ How to Run

## 1. Open the project folder

```bash
cd "AI Personal Finance Assistant"
```

## 2. Activate virtual environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell execution policy causes an issue:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then:

```powershell
.\venv\Scripts\Activate.ps1
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Run database check

```bash
python src/check_database.py
```

## 5. Run ML expense prediction

```bash
python src/ml_expense_prediction.py
```

## 6. Run anomaly detection

```bash
python src/anomaly_detection.py
```

## 7. Start Streamlit

```bash
streamlit run app.py
```

The application will open in the browser.

---

# 🔐 Security Note

The project is currently designed as a local portfolio/MVP application.

For production deployment, additional security would be required, including:

- Authentication
- User authorization
- Secure secret management
- Input validation
- Database access controls
- Encryption
- API security
- Logging and monitoring
- Secure handling of financial data

Do **not** commit real credentials or secrets to GitHub.

---

# 🧪 Testing Performed

The project has been tested through:

- Database inspection
- Transaction data verification
- Budget data verification
- Streamlit application execution
- Financial analysis verification
- ML dataset generation
- Expense prediction execution
- Anomaly detection execution
- UI/UX testing

Example database verification:

```bash
python src/check_database.py
```

Example anomaly detection:

```bash
python src/anomaly_detection.py
```

---

# 💼 Why This Project Is Relevant to FinTech

This project demonstrates several concepts commonly relevant to FinTech applications:

### Data Management

```text
SQLite + SQL
```

### Financial Analytics

```text
Income
Expenses
Savings
Budgets
Spending Categories
```

### Machine Learning

```text
Expense Prediction
Anomaly Detection
Feature Engineering
```

### Intelligent Systems

```text
Financial Recommendations
Finance Chat
AI Advisor
```

### Product Development

```text
Interactive Dashboard
Data Visualization
Filtering
User Experience
```

Therefore, this is more than a simple CRUD project. It combines:

**Database + Data Analytics + Machine Learning + AI-style Recommendations + FinTech UI/UX.**

---

# 🧠 Key Concepts Demonstrated

Through this project, the following concepts are demonstrated:

- Python programming
- SQL
- SQLite
- Database connectivity
- CRUD/data retrieval
- Pandas
- Data cleaning
- Data aggregation
- Feature engineering
- Financial metrics
- Data visualization
- Machine Learning
- Anomaly detection
- Rule-based recommendation systems
- Streamlit
- UI/UX design
- Modular Python architecture

---

# 📊 Current Architecture Flow

```text
                    USER
                     │
                     ▼
              STREAMLIT APP
                  app.py
                     │
       ┌─────────────┼─────────────┐
       │             │             │
       ▼             ▼             ▼
   Dashboard    Transactions    Analysis
       │             │             │
       └─────────────┼─────────────┘
                     │
                     ▼
                DATABASE
               SQLite DB
                     │
          ┌──────────┼──────────┐
          │          │          │
          ▼          ▼          ▼
       Budget    AI Advisor   Finance Chat
          │          │          │
          └──────────┼──────────┘
                     │
                     ▼
             DATA PROCESSING
                  Pandas
                     │
            ┌────────┴────────┐
            ▼                 ▼
     ML Prediction      Anomaly Detection
            │                 │
            └────────┬────────┘
                     ▼
              FINANCIAL INSIGHTS
```

---

# 🚀 Future Improvements

The current project stops at the anomaly detection stage.

Possible next stages include:

## Stage 4 — Advanced AI

- LLM integration
- Natural-language financial analysis
- Better Finance Chat
- AI-generated explanations
- Personalized financial planning

## Stage 5 — Database-Safe AI

```text
User Question
      ↓
Intent Detection
      ↓
Safe Query Generation
      ↓
SQL Validation
      ↓
Database
      ↓
Result
      ↓
Natural Language Response
```

## Stage 6 — Production Features

- User authentication
- Multiple user accounts
- Personal financial profiles
- Secure database architecture
- Cloud deployment
- API layer
- Automated testing

## Stage 7 — Advanced FinTech Features

- Recurring expense detection
- Subscription detection
- Cash-flow forecasting
- Financial goal tracking
- Monthly financial reports
- Spending alerts
- Advanced anomaly detection
- Explainable AI
- Personalized budget suggestions

---

# 🎓 Interview Explanation

### Short Answer

> "I developed an AI-powered personal finance assistant using Python, SQLite, Pandas, Machine Learning and Streamlit. The application stores and analyzes financial transactions, tracks budgets, calculates savings, generates financial recommendations, provides a finance chat interface, predicts expense behavior using engineered time-series features, and detects unusual spending patterns. I also designed a modern FinTech-style Streamlit dashboard for visualization and user interaction."

### If asked about the architecture

> "The Streamlit application acts as the presentation layer. The application communicates with modular Python components for database operations, analysis, budgeting, recommendations, AI advisory, chat, prediction and anomaly detection. SQLite is used as the persistence layer, while Pandas handles data processing and the ML modules perform prediction and anomaly detection."

---

# ⭐ Project Highlights

```text
💰 Personal Finance Management
📊 Financial Analytics
💳 Transaction Tracking
🎯 Budget Monitoring
🤖 AI Financial Advisor
💬 Finance Chat
📈 ML Expense Prediction
🚨 Anomaly Detection
🎨 FinTech Dashboard UI/UX
🗄️ SQLite Database
🐍 Python
```

---

# 👨‍💻 Project Development Journey

The project evolved progressively:

```text
Database
   ↓
Transaction Management
   ↓
Financial Analysis
   ↓
Budget Analysis
   ↓
Recommendation Engine
   ↓
AI Financial Advisor
   ↓
Finance Chat
   ↓
ML Expense Prediction
   ↓
Spending Anomaly Detection
   ↓
Streamlit Dashboard
   ↓
UI/UX Upgrade — Stage 1
   ↓
UI/UX Upgrade — Stage 2
```

---

# 📌 Current Stopping Point

The current version intentionally stops after:

**Spending Anomaly Detection + UI/UX Stage 2**

This provides a strong foundation for the next development phase without unnecessarily increasing project complexity.

---

## 📄 License

This project is intended for educational, portfolio, and interview purposes.
