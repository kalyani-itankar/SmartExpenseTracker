import sqlite3


# ==========================================
# CREATE DATABASE
# ==========================================

def create_database():

    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    # Expenses table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            date TEXT NOT NULL
        )
    """)

    # Income table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS income (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            date TEXT NOT NULL
        )
    """)

    # Budget table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budget (
            id INTEGER PRIMARY KEY,
            amount REAL NOT NULL
        )
    """)

    connection.commit()
    connection.close()


# ==========================================
# ADD EXPENSE
# ==========================================

def add_expense(amount, category, description, date):

    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO expenses
        (amount, category, description, date)
        VALUES (?, ?, ?, ?)
    """, (
        amount,
        category,
        description,
        date
    ))

    connection.commit()
    connection.close()


# ==========================================
# GET ALL EXPENSES
# ==========================================

def get_expenses():

    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM expenses
        ORDER BY date DESC, id DESC
    """)

    expenses = cursor.fetchall()

    connection.close()

    return expenses


# ==========================================
# GET CURRENT MONTH EXPENSES
# ==========================================

def get_current_month_expenses():

    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM expenses
        WHERE strftime('%Y-%m', date) = strftime('%Y-%m', 'now')
        ORDER BY date DESC, id DESC
    """)

    expenses = cursor.fetchall()

    connection.close()

    return expenses


# ==========================================
# GET TOTAL CURRENT MONTH EXPENSE
# ==========================================

def get_current_month_expense_total():

    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT SUM(amount)
        FROM expenses
        WHERE strftime('%Y-%m', date) = strftime('%Y-%m', 'now')
    """)

    result = cursor.fetchone()[0]

    connection.close()

    return result if result else 0


# ==========================================
# UPDATE EXPENSE
# ==========================================

def update_expense(
    expense_id,
    amount,
    category,
    description,
    date
):

    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE expenses
        SET
            amount = ?,
            category = ?,
            description = ?,
            date = ?
        WHERE id = ?
    """, (
        amount,
        category,
        description,
        date,
        expense_id
    ))

    connection.commit()
    connection.close()


# ==========================================
# DELETE EXPENSE
# ==========================================

def delete_expense(expense_id):

    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM expenses
        WHERE id = ?
    """, (expense_id,))

    connection.commit()
    connection.close()


# ==========================================
# ADD INCOME
# ==========================================

def add_income(amount, date):

    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO income
        (amount, date)
        VALUES (?, ?)
    """, (
        amount,
        date
    ))

    connection.commit()
    connection.close()


# ==========================================
# GET TOTAL INCOME
# ==========================================

def get_total_income():

    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT SUM(amount)
        FROM income
    """)

    result = cursor.fetchone()[0]

    connection.close()

    return result if result else 0


# ==========================================
# GET CURRENT MONTH INCOME
# ==========================================

def get_current_month_income():

    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT SUM(amount)
        FROM income
        WHERE strftime('%Y-%m', date) = strftime('%Y-%m', 'now')
    """)

    result = cursor.fetchone()[0]

    connection.close()

    return result if result else 0


# ==========================================
# SET BUDGET
# ==========================================

def set_budget(amount):

    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO budget
        (id, amount)
        VALUES (1, ?)
    """, (amount,))

    connection.commit()
    connection.close()


# ==========================================
# GET BUDGET
# ==========================================

def get_budget():

    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT amount
        FROM budget
        WHERE id = 1
    """)

    result = cursor.fetchone()

    connection.close()

    if result:
        return result[0]

    return 0

