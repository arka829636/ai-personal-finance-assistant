# 💰 FinanceAI — AI Personal Finance Assistant

FinanceAI is a personal finance analytics application built with **Python and Streamlit**. It combines transaction management, financial analytics, budgeting, machine learning, anomaly detection, rule-based intent detection, and an LLM integration layer into a single interactive application.

The project is designed as a practical **FinTech / Data Analytics / AI portfolio project**.

---

## 🚀 Live Demo

🌐 **Streamlit App:**  
https://https://ai-personal-finance-assistantt.streamlit.app//

📂 **GitHub Repository:**  
https://github.com/arka829636/ai-personal-finance-assistant

---

## 📌 Project Overview

FinanceAI helps users understand their financial activity through:

- Income and expense tracking
- Interactive financial dashboards
- Category-wise spending analysis
- Budget monitoring
- Financial recommendations
- Expense prediction using Machine Learning
- Unusual transaction detection
- Natural-language Finance Chat
- LLM integration for general financial questions
- SQLite-based transaction storage

The application uses a layered architecture where the Streamlit interface communicates with analytics, database, machine learning, and AI components.

---

# ✨ Features

## 🏠 Dashboard

The dashboard provides a quick overview of the user's financial position.

### Key Metrics

- Total Income
- Total Expenses
- Savings
- Savings Rate
- Number of Transactions
- Average Expense
- Top Spending Category

### Visualizations

- Monthly income
- Category-wise expenses
- Spending distribution
- Financial KPI cards

---

## 💳 Transaction Management

FinanceAI provides complete CRUD functionality for financial transactions.

### Supported Operations

- Add transaction
- View transactions
- Edit transaction
- Delete transaction

### Transaction Fields

- Date
- Type
- Category
- Description
- Amount
- Payment Method

All transaction data is stored in a SQLite database.

---

## 📊 Financial Analysis

The Analysis module provides deeper insights into spending behavior.

### Metrics

- Total income
- Total expenses
- Net savings
- Savings rate
- Category-wise spending

### Analysis

- Expense distribution
- Monthly income vs expense
- Spending categories
- Highest spending category

---

## 💰 Budget Management

The Budget module compares planned budgets with actual spending.

### Features

- Category-wise budget
- Actual spending
- Remaining budget
- Budget utilization
- Budget status

### Budget Status

Transactions can be classified as:

- Within Budget
- Near Limit
- Over Budget

The project also includes intentional monthly demo scenarios to demonstrate budget-overrun handling.

---

## 🤖 AI Advisor

The AI Advisor provides rule-based financial recommendations using the user's stored financial data.

Examples include:

- High spending categories
- Budget utilization
- Savings performance
- Average expense
- Areas where spending can be reviewed

The recommendations are generated from actual application data rather than hard-coded financial advice.

---

# 🧠 Machine Learning

FinanceAI contains two machine learning components.

## 1. Expense Prediction

A **Random Forest Regressor** is used to estimate the next day's expense.

### Features

The model uses:

- Day of week
- Day of month
- Month
- Previous day's expense
- Previous seven-transaction expense total
- Rolling seven-transaction average

### Model

```text
RandomForestRegressor
├── n_estimators = 200
├── max_depth = 8
└── random_state = 42
