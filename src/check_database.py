import sqlite3


connection = sqlite3.connect(
    "data/finance.db"
)

cursor = connection.cursor()


print("\n===== TRANSACTIONS =====")

cursor.execute(
    "SELECT * FROM transactions"
)

rows = cursor.fetchall()

for row in rows:

    print(row)


print("\n===== BUDGETS =====")

cursor.execute(
    "SELECT * FROM budgets"
)

rows = cursor.fetchall()

for row in rows:

    print(row)


connection.close()