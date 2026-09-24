from datetime import datetime

from database import (
    create_database,
    add_expense,
    get_expenses,
    add_income,
    get_total_income,
    set_budget,
    get_budget
)

from analytics import (
    show_total_expense,
    show_category_analysis,
    show_highest_category,
    show_average_expense,
    show_expense_count,
    show_bar_chart,
    show_pie_chart
)


# ==========================================
# ADD EXPENSE
# ==========================================

def add_new_expense():

    print("\n========== ADD EXPENSE ==========")

    try:
        amount = float(input("Enter expense amount: ₹"))

        if amount <= 0:
            print("❌ Amount must be greater than 0.")
            return

        category = input("Enter category: ").strip()

        if not category:
            print("❌ Category cannot be empty.")
            return

        description = input("Enter description: ").strip()

        if not description:
            print("❌ Description cannot be empty.")
            return

        date = datetime.now().strftime("%Y-%m-%d")

        add_expense(
            amount,
            category,
            description,
            date
        )

        print("\n✅ Expense saved successfully!")

    except ValueError:
        print("\n❌ Please enter a valid number.")


# ==========================================
# VIEW EXPENSES
# ==========================================

def view_expenses():

    expenses = get_expenses()

    if not expenses:
        print("\n❌ No expenses found.")
        return

    print("\n========== YOUR EXPENSES ==========")

    for expense in expenses:

        expense_id = expense[0]
        amount = expense[1]
        category = expense[2]
        description = expense[3]
        date = expense[4]

        print(
            f"{expense_id}. "
            f"₹{amount:.2f} | "
            f"{category} | "
            f"{description} | "
            f"{date}"
        )


# ==========================================
# ADD INCOME
# ==========================================

def add_new_income():

    print("\n========== ADD INCOME ==========")

    try:

        amount = float(input("Enter income amount: ₹"))

        if amount <= 0:
            print("❌ Amount must be greater than 0.")
            return

        date = datetime.now().strftime("%Y-%m-%d")

        add_income(
            amount,
            date
        )

        print("\n✅ Income saved successfully!")

    except ValueError:

        print("\n❌ Please enter a valid number.")


# ==========================================
# SET MONTHLY BUDGET
# ==========================================

def set_monthly_budget():

    print("\n========== SET MONTHLY BUDGET ==========")

    try:

        amount = float(
            input("Enter your monthly budget: ₹")
        )

        if amount <= 0:
            print("❌ Budget must be greater than 0.")
            return

        set_budget(amount)

        print(
            f"\n✅ Monthly budget set to ₹{amount:.2f}"
        )

    except ValueError:

        print("\n❌ Please enter a valid number.")


# ==========================================
# SHOW BALANCE
# ==========================================

def show_balance():

    expenses = get_expenses()

    total_expense = sum(
        expense[1]
        for expense in expenses
    )

    total_income = get_total_income()

    balance = total_income - total_expense

    print("\n========== FINANCIAL SUMMARY ==========")

    print(
        f"💰 Total Income:  ₹{total_income:.2f}"
    )

    print(
        f"💸 Total Expense: ₹{total_expense:.2f}"
    )

    print(
        f"💵 Balance:       ₹{balance:.2f}"
    )


# ==========================================
# SHOW BUDGET
# ==========================================

def show_budget():

    expenses = get_expenses()

    total_expense = sum(
        expense[1]
        for expense in expenses
    )

    budget = get_budget()

    print("\n========== BUDGET STATUS ==========")

    if budget == 0:

        print(
            "⚠️ No monthly budget has been set."
        )

        return

    remaining = budget - total_expense

    percentage = (
        total_expense / budget
    ) * 100

    print(
        f"💰 Budget:       ₹{budget:.2f}"
    )

    print(
        f"💸 Spent:        ₹{total_expense:.2f}"
    )

    print(
        f"💵 Remaining:    ₹{remaining:.2f}"
    )

    print(
        f"📊 Used:         {percentage:.1f}%"
    )

    if percentage >= 100:

        print(
            "\n🚨 ALERT: You have exceeded your budget!"
        )

    elif percentage >= 80:

        print(
            "\n⚠️ WARNING: You have used more than "
            "80% of your budget!"
        )

    else:

        print(
            "\n✅ You are within your budget!"
        )


# ==========================================
# ANALYTICS MENU
# ==========================================

def analytics_menu():

    while True:

        print("\n========== 📊 ANALYTICS ==========")

        print("1. Total Expense")
        print("2. Category Analysis")
        print("3. Highest Spending Category")
        print("4. Average Expense")
        print("5. Number of Expenses")
        print("6. 📊 Bar Chart")
        print("7. 🥧 Pie Chart")
        print("8. Back to Main Menu")

        choice = input("\nEnter your choice: ")

        if choice == "1":

            show_total_expense()

        elif choice == "2":

            show_category_analysis()

        elif choice == "3":

            show_highest_category()

        elif choice == "4":

            show_average_expense()

        elif choice == "5":

            show_expense_count()

        elif choice == "6":

            show_bar_chart()

        elif choice == "7":

            show_pie_chart()

        elif choice == "8":

            break

        else:

            print("\n❌ Invalid choice.")


# ==========================================
# MAIN PROGRAM
# ==========================================

def main():

    create_database()

    while True:

        print("\n==============================")
        print("     💰 SMART EXPENSE TRACKER")
        print("==============================")

        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Add Income")
        print("4. Show Balance")
        print("5. Set Monthly Budget")
        print("6. Show Budget Status")
        print("7. 📊 Expense Analytics")
        print("8. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":

            add_new_expense()

        elif choice == "2":

            view_expenses()

        elif choice == "3":

            add_new_income()

        elif choice == "4":

            show_balance()

        elif choice == "5":

            set_monthly_budget()

        elif choice == "6":

            show_budget()

        elif choice == "7":

            analytics_menu()

        elif choice == "8":

            print(
                "\nThank you for using "
                "Smart Expense Tracker! 👋"
            )

            break

        else:

            print(
                "\n❌ Invalid choice. "
                "Please select 1-8."
            )


# ==========================================
# START PROGRAM
# ==========================================

if __name__ == "__main__":
    main()
