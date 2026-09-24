# 💰 AI Personal Finance Assistant

An AI-powered personal finance analytics platform built with Python and Streamlit that helps users track transactions, analyze spending, manage budgets, predict future expenses, detect unusual spending patterns, and interact with their financial data through a natural-language Finance Chat interface.

The project combines:

- Financial analytics
- SQL and database management
- Machine Learning
- Anomaly Detection
- Rule-based financial intelligence
- Natural Language Processing
- LLM integration
- Interactive data visualization
- Streamlit deployment

It is designed as a practical **AI / Machine Learning / FinTech portfolio project**.

---

## 🚀 Live Demo

🌐 **Live Application**

https://ai-personal-finance-assistantt.streamlit.app/

> Replace `YOUR_NEW_STREAMLIT_URL` with the exact Streamlit URL of the current deployment.

📂 **GitHub Repository**

https://github.com/arka829636/ai-personal-finance-assistant

---

# 📌 Project Overview

The AI Personal Finance Assistant provides a unified platform for personal financial management.

Instead of maintaining separate applications for transactions, analysis, budgets, and financial insights, this project combines them into one interactive system.

The application allows users to:

- Track income and expenses
- Add, edit, and delete transactions
- Analyze spending patterns
- Monitor budgets
- Receive rule-based financial recommendations
- Predict future expenses using Machine Learning
- Detect unusual spending using Anomaly Detection
- Ask financial questions using natural language
- Use an LLM integration layer for general financial questions
- Visualize financial information through interactive charts

---

# 🎯 Project Objectives

The main objectives of the project are:

1. Build a practical personal finance management application.
2. Apply SQL and database concepts to real-world financial data.
3. Use Pandas for financial data analysis.
4. Apply Machine Learning for expense prediction.
5. Apply unsupervised learning for anomaly detection.
6. Implement natural-language intent detection.
7. Integrate an LLM layer into a financial application.
8. Build an interactive FinTech-style user interface.
9. Deploy the application using Streamlit Community Cloud.
10. Create a project suitable for AI/ML/Data Analytics interviews.

---

# ✨ Key Features

## 🏠 1. Dashboard

The Dashboard provides a high-level overview of the user's financial condition.

### Key Performance Indicators

- Total Income
- Total Expenses
- Savings
- Savings Rate
- Number of Transactions
- Number of Expense Transactions
- Average Expense
- Top Spending Category

### Visualizations

- Monthly income
- Category-wise expenses
- Spending distribution
- Financial KPI cards
- Expense trends

---

# 💳 2. Transaction Management

The Transactions module provides complete CRUD functionality.

## CRUD Operations

### Create
Add a new financial transaction.

### Read
View and filter existing transactions.

### Update
Edit an existing transaction.

### Delete
Remove a transaction.

### Transaction Fields

| Field | Description |
|---|---|
| ID | Unique transaction identifier |
| Date | Transaction date |
| Type | Income / Expense |
| Category | Food, Shopping, Education, etc. |
| Description | Transaction description |
| Amount | Transaction amount |
| Payment Method | UPI, Cash, Bank Transfer, etc. |

The transaction data is stored in SQLite.

---

# 🗄️ 3. Database Layer

The project uses **SQLite** as the relational database.

## Database Table

```sql
transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    type TEXT NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    amount REAL NOT NULL,
    payment_method TEXT
)
