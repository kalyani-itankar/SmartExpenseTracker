import pandas as pd
import matplotlib.pyplot as plt

from database import get_expenses


def get_expense_dataframe():
    expenses = get_expenses()

    if not expenses:
        return None

    df = pd.DataFrame(
        expenses,
        columns=[
            "id",
            "amount",
            "category",
            "description",
            "date"
        ]
    )

    return df


def show_total_expense():
    df = get_expense_dataframe()

    if df is None:
        print("\n❌ No expenses found.")
        return

    total = df["amount"].sum()

    print("\n========== TOTAL EXPENSE ==========")
    print(f"💸 Total spent: ₹{total:.2f}")


def show_category_analysis():
    df = get_expense_dataframe()

    if df is None:
        print("\n❌ No expenses found.")
        return

    category_total = (
        df.groupby("category")["amount"]
        .sum()
        .sort_values(ascending=False)
    )

    print("\n========== CATEGORY ANALYSIS ==========")

    for category, amount in category_total.items():
        print(f"📌 {category}: ₹{amount:.2f}")


def show_highest_category():
    df = get_expense_dataframe()

    if df is None:
        print("\n❌ No expenses found.")
        return

    category_total = (
        df.groupby("category")["amount"]
        .sum()
    )

    highest_category = category_total.idxmax()
    highest_amount = category_total.max()

    print("\n========== TOP SPENDING CATEGORY ==========")

    print(
        f"🔥 You spend the most on "
        f"{highest_category}: ₹{highest_amount:.2f}"
    )


def show_average_expense():
    df = get_expense_dataframe()

    if df is None:
        print("\n❌ No expenses found.")
        return

    average = df["amount"].mean()

    print("\n========== AVERAGE EXPENSE ==========")
    print(f"📊 Average expense: ₹{average:.2f}")


def show_expense_count():
    df = get_expense_dataframe()

    if df is None:
        print("\n❌ No expenses found.")
        return

    count = len(df)

    print("\n========== EXPENSE COUNT ==========")
    print(f"🧾 Number of expenses: {count}")


def show_bar_chart():
    df = get_expense_dataframe()

    if df is None:
        print("\n❌ No expenses found.")
        return

    category_total = (
        df.groupby("category")["amount"]
        .sum()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(9, 5))

    category_total.plot(kind="bar")

    plt.title("💰 Spending by Category")
    plt.xlabel("Category")
    plt.ylabel("Amount (₹)")

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.show()


def show_pie_chart():
    df = get_expense_dataframe()

    if df is None:
        print("\n❌ No expenses found.")
        return

    category_total = (
        df.groupby("category")["amount"]
        .sum()
    )

    plt.figure(figsize=(7, 7))

    category_total.plot(
        kind="pie",
        autopct="%1.1f%%"
    )

    plt.title("🥧 Expense Distribution")

    plt.ylabel("")

    plt.tight_layout()

    plt.show()
