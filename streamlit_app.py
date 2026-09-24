import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, date

from database import (
    create_database,
    add_expense,
    get_expenses,
    get_current_month_expenses,
    get_current_month_expense_total,
    update_expense,
    delete_expense,
    add_income,
    get_current_month_income,
    set_budget,
    get_budget
)


# ==========================================
# DATABASE
# ==========================================

create_database()


# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Smart Expense Tracker",
    page_icon="💰",
    layout="wide"
)


# ==========================================
# TITLE
# ==========================================

st.title("💰 Smart Expense Tracker")

st.caption(
    "Track your money • Understand your spending • "
    "Control your budget"
)


# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("📌 Navigation")

menu = st.sidebar.radio(
    "Go to",
    [
        "📊 Dashboard",
        "📅 Date Analytics",
        "➕ Add Expense",
        "💰 Add Income",
        "🎯 Set Budget",
        "🧾 Manage Expenses"
    ]
)


# ==========================================
# FINANCIAL DATA
# ==========================================

all_expenses = get_expenses()

current_month_expenses = get_current_month_expenses()

monthly_expense = get_current_month_expense_total()

monthly_income = get_current_month_income()

monthly_balance = monthly_income - monthly_expense

budget = get_budget()


if budget > 0:

    budget_used = (
        monthly_expense / budget
    ) * 100

else:

    budget_used = 0


current_month = datetime.now().strftime(
    "%B %Y"
)


# ============================================================
# DASHBOARD
# ============================================================

if menu == "📊 Dashboard":

    st.header(
        f"📊 Financial Dashboard — {current_month}"
    )


    # ==========================================
    # SUMMARY CARDS
    # ==========================================

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "💰 Monthly Income",
            f"₹{monthly_income:,.2f}"
        )


    with col2:

        st.metric(
            "💸 Monthly Expense",
            f"₹{monthly_expense:,.2f}"
        )


    with col3:

        st.metric(
            "💵 Balance",
            f"₹{monthly_balance:,.2f}"
        )


    with col4:

        st.metric(
            "🎯 Budget Used",
            f"{budget_used:.1f}%"
        )


    st.divider()


    # ==========================================
    # CSV EXPORT
    # ==========================================

    st.subheader(
        "📥 Export Your Data"
    )


    export_col1, export_col2 = st.columns(2)


    with export_col1:

        if current_month_expenses:

            current_df = pd.DataFrame(
                current_month_expenses,
                columns=[
                    "ID",
                    "Amount",
                    "Category",
                    "Description",
                    "Date"
                ]
            )


            current_csv = (
                current_df
                .to_csv(index=False)
                .encode("utf-8")
            )


            st.download_button(
                label="📥 Download Current Month CSV",
                data=current_csv,
                file_name=(
                    f"expenses_"
                    f"{datetime.now().strftime('%Y_%m')}.csv"
                ),
                mime="text/csv",
                width="stretch"
            )


        else:

            st.info(
                "No current-month expenses to export."
            )


    with export_col2:

        if all_expenses:

            all_df = pd.DataFrame(
                all_expenses,
                columns=[
                    "ID",
                    "Amount",
                    "Category",
                    "Description",
                    "Date"
                ]
            )


            all_csv = (
                all_df
                .to_csv(index=False)
                .encode("utf-8")
            )


            st.download_button(
                label="📥 Download All Expenses CSV",
                data=all_csv,
                file_name="all_expenses.csv",
                mime="text/csv",
                width="stretch"
            )


        else:

            st.info(
                "No expenses available to export."
            )


    st.divider()


    # ========================================================
    # MONTHLY ANALYTICS
    # ========================================================

    if current_month_expenses:

        df = pd.DataFrame(
            current_month_expenses,
            columns=[
                "ID",
                "Amount",
                "Category",
                "Description",
                "Date"
            ]
        )


        average_expense = df["Amount"].mean()

        highest_expense = df["Amount"].max()

        transaction_count = len(df)

        highest_expense_row = df.loc[
            df["Amount"].idxmax()
        ]


        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "📊 Average Expense",
                f"₹{average_expense:,.2f}"
            )


        with col2:

            st.metric(
                "🔥 Highest Expense",
                f"₹{highest_expense:,.2f}"
            )


        with col3:

            st.metric(
                "🧾 Transactions",
                transaction_count
            )


        st.divider()


        # ======================================
        # CATEGORY ANALYSIS
        # ======================================

        category_total = (
            df.groupby("Category")["Amount"]
            .sum()
            .sort_values(ascending=False)
        )


        # ====================================================
        # SMART SPENDING INSIGHTS
        # ====================================================

        st.subheader(
            "🧠 Smart Spending Insights"
        )


        highest_category = (
            category_total.idxmax()
        )


        highest_category_amount = (
            category_total.max()
        )


        total_spending = (
            category_total.sum()
        )


        if total_spending > 0:

            highest_category_percentage = (
                highest_category_amount
                / total_spending
            ) * 100

        else:

            highest_category_percentage = 0


        st.info(
            f"🔥 **Top spending category:** "
            f"{highest_category} — "
            f"₹{highest_category_amount:,.2f} "
            f"({highest_category_percentage:.1f}% of spending)"
        )


        if budget > 0:

            remaining = (
                budget - monthly_expense
            )


            if monthly_expense >= budget:

                st.error(
                    f"🚨 **Budget Alert:** "
                    f"You have exceeded your monthly budget "
                    f"by ₹{abs(remaining):,.2f}."
                )


            elif monthly_expense >= budget * 0.8:

                st.warning(
                    f"⚠️ **Budget Alert:** "
                    f"You have used {budget_used:.1f}% "
                    f"of your budget. "
                    f"Only ₹{remaining:,.2f} remains."
                )


            else:

                st.success(
                    f"✅ **Budget Status:** "
                    f"You are within your budget. "
                    f"₹{remaining:,.2f} remains."
                )


        else:

            st.warning(
                "💡 **Tip:** Set a monthly budget to "
                "receive personalized budget alerts."
            )


        st.write(
            f"📊 Your average transaction is "
            f"**₹{average_expense:,.2f}**."
        )


        if highest_expense > average_expense * 2:

            st.warning(
                f"💸 Your largest transaction was "
                f"₹{highest_expense:,.2f}, which is "
                f"more than twice your average expense."
            )


        st.divider()


        # ======================================
        # CHARTS
        # ======================================

        chart_col1, chart_col2 = st.columns(2)


        with chart_col1:

            st.subheader(
                "🥧 Spending Distribution"
            )


            fig, ax = plt.subplots(
                figsize=(7, 7)
            )


            ax.pie(
                category_total.values,
                labels=category_total.index,
                autopct="%1.1f%%",
                startangle=90
            )


            ax.set_title(
                "Expense by Category"
            )


            st.pyplot(
                fig,
                width="stretch"
            )


            plt.close(fig)


        with chart_col2:

            st.subheader(
                "📊 Spending by Category"
            )


            st.bar_chart(
                category_total,
                width="stretch"
            )


        st.divider()


        # ======================================
        # DAILY SPENDING TREND
        # ======================================

        st.subheader(
            "📈 Daily Spending Trend"
        )


        daily_expense = (
            df.groupby("Date")["Amount"]
            .sum()
        )


        st.line_chart(
            daily_expense,
            width="stretch"
        )


        st.divider()


        # ======================================
        # LARGEST TRANSACTION
        # ======================================

        st.subheader(
            "💸 Largest Transaction"
        )


        st.warning(
            f"₹{highest_expense:,.2f} "
            f"spent on **{highest_expense_row['Description']}** "
            f"under **{highest_expense_row['Category']}** "
            f"on **{highest_expense_row['Date']}**."
        )


        st.divider()


        # ======================================
        # TRANSACTION TABLE
        # ======================================

        st.subheader(
            "🧾 This Month's Transactions"
        )


        st.dataframe(
            df,
            width="stretch",
            hide_index=True
        )


    else:

        st.info(
            "📭 No expenses recorded this month yet."
        )


        st.write(
            "Add your first expense to start "
            "seeing analytics and smart insights!"
        )


    # ====================================================
    # MONTHLY BUDGET
    # ====================================================

    st.divider()


    st.subheader(
        "🎯 Monthly Budget"
    )


    if budget > 0:

        remaining = (
            budget - monthly_expense
        )


        budget_col1, budget_col2 = st.columns(2)


        with budget_col1:

            st.write(
                f"**Budget:** ₹{budget:,.2f}"
            )


            st.write(
                f"**Spent:** ₹{monthly_expense:,.2f}"
            )


            st.write(
                f"**Remaining:** ₹{remaining:,.2f}"
            )


        with budget_col2:

            progress = min(
                monthly_expense / budget,
                1.0
            )


            st.progress(
                progress
            )


            st.write(
                f"{budget_used:.1f}% of your "
                f"budget has been used."
            )


        if monthly_expense >= budget:

            st.error(
                "🚨 Budget exceeded!"
            )


        elif monthly_expense >= budget * 0.8:

            st.warning(
                "⚠️ You have used more than "
                "80% of your budget."
            )


        else:

            st.success(
                "✅ You are within your budget."
            )


    else:

        st.warning(
            "⚠️ No monthly budget has been set."
        )


# ============================================================
# DATE ANALYTICS
# ============================================================

elif menu == "📅 Date Analytics":

    st.header(
        "📅 Date & Month Analytics"
    )


    st.write(
        "Analyze your spending for a specific month "
        "or choose a custom date range."
    )


    # ==========================================
    # CHECK EXPENSE DATA
    # ==========================================

    if not all_expenses:

        st.info(
            "📭 No expense data available yet."
        )

        st.write(
            "Add some expenses first to use "
            "Date Analytics."
        )


    else:

        analytics_df = pd.DataFrame(
            all_expenses,
            columns=[
                "ID",
                "Amount",
                "Category",
                "Description",
                "Date"
            ]
        )


        analytics_df["Date"] = pd.to_datetime(
            analytics_df["Date"]
        )


        # ======================================
        # FILTER TYPE
        # ======================================

        filter_type = st.radio(
            "Choose analysis type",
            [
                "📅 Select Month",
                "🔍 Custom Date Range"
            ],
            horizontal=True
        )


        # ====================================================
        # MONTH FILTER
        # ====================================================

        if filter_type == "📅 Select Month":

            analytics_df["Month"] = (
                analytics_df["Date"]
                .dt.to_period("M")
            )


            available_months = sorted(
                analytics_df["Month"]
                .unique(),
                reverse=True
            )


            month_options = [
                month.strftime("%B %Y")
                for month in available_months
            ]


            selected_month_label = st.selectbox(
                "Select Month",
                month_options
            )


            selected_index = month_options.index(
                selected_month_label
            )


            selected_month = (
                available_months[selected_index]
            )


            filtered_df = analytics_df[
                analytics_df["Month"]
                == selected_month
            ].copy()


            period_name = selected_month_label


        # ====================================================
        # CUSTOM DATE RANGE
        # ====================================================

        else:

            min_date = (
                analytics_df["Date"]
                .min()
                .date()
            )


            max_date = (
                analytics_df["Date"]
                .max()
                .date()
            )


            date_col1, date_col2 = st.columns(2)


            with date_col1:

                start_date = st.date_input(
                    "Start Date",
                    value=min_date,
                    min_value=min_date,
                    max_value=max_date
                )


            with date_col2:

                end_date = st.date_input(
                    "End Date",
                    value=max_date,
                    min_value=min_date,
                    max_value=max_date
                )


            if start_date > end_date:

                st.error(
                    "❌ Start date cannot be after end date."
                )

                filtered_df = pd.DataFrame()

            else:

                filtered_df = analytics_df[
                    (
                        analytics_df["Date"].dt.date
                        >= start_date
                    )
                    &
                    (
                        analytics_df["Date"].dt.date
                        <= end_date
                    )
                ].copy()


            period_name = (
                f"{start_date.strftime('%d %b %Y')} "
                f"to "
                f"{end_date.strftime('%d %b %Y')}"
            )


        # ====================================================
        # RESULTS
        # ====================================================

        if not filtered_df.empty:

            total_spending = (
                filtered_df["Amount"].sum()
            )


            average_expense = (
                filtered_df["Amount"].mean()
            )


            highest_expense = (
                filtered_df["Amount"].max()
            )


            transaction_count = (
                len(filtered_df)
            )


            # ======================================
            # SUMMARY
            # ======================================

            st.divider()


            st.subheader(
                f"📊 Analysis — {period_name}"
            )


            col1, col2, col3, col4 = st.columns(4)


            with col1:

                st.metric(
                    "💸 Total Spending",
                    f"₹{total_spending:,.2f}"
                )


            with col2:

                st.metric(
                    "📊 Average Expense",
                    f"₹{average_expense:,.2f}"
                )


            with col3:

                st.metric(
                    "🔥 Highest Expense",
                    f"₹{highest_expense:,.2f}"
                )


            with col4:

                st.metric(
                    "🧾 Transactions",
                    transaction_count
                )


            st.divider()


            # ======================================
            # CATEGORY ANALYSIS
            # ======================================

            category_total = (
                filtered_df
                .groupby("Category")["Amount"]
                .sum()
                .sort_values(
                    ascending=False
                )
            )


            st.subheader(
                "🏷️ Category Analysis"
            )


            category_col1, category_col2 = (
                st.columns(2)
            )


            with category_col1:

                st.bar_chart(
                    category_total,
                    width="stretch"
                )


            with category_col2:

                fig, ax = plt.subplots(
                    figsize=(7, 7)
                )


                ax.pie(
                    category_total.values,
                    labels=category_total.index,
                    autopct="%1.1f%%",
                    startangle=90
                )


                ax.set_title(
                    "Spending Distribution"
                )


                st.pyplot(
                    fig,
                    width="stretch"
                )


                plt.close(fig)


            st.divider()


            # ======================================
            # SPENDING TREND
            # ======================================

            st.subheader(
                "📈 Spending Trend"
            )


            daily_spending = (
                filtered_df
                .groupby("Date")["Amount"]
                .sum()
                .sort_index()
            )


            st.line_chart(
                daily_spending,
                width="stretch"
            )


            st.divider()


            # ======================================
            # SMART INSIGHTS
            # ======================================

            st.subheader(
                "🧠 Smart Insights"
            )


            top_category = (
                category_total.idxmax()
            )


            top_category_amount = (
                category_total.max()
            )


            top_category_percentage = (
                top_category_amount
                / total_spending
            ) * 100


            st.info(
                f"🔥 You spent the most on "
                f"**{top_category}**: "
                f"₹{top_category_amount:,.2f} "
                f"({top_category_percentage:.1f}% "
                f"of this period's spending)."
            )


            if highest_expense > average_expense * 2:

                st.warning(
                    f"⚠️ Your largest transaction "
                    f"of ₹{highest_expense:,.2f} "
                    f"is more than twice your "
                    f"average transaction."
                )


            else:

                st.success(
                    "✅ Your largest transaction "
                    "is within a reasonable range "
                    "of your average transaction."
                )


            # ======================================
            # HIGHEST SPENDING TRANSACTION
            # ======================================

            highest_row = filtered_df.loc[
                filtered_df["Amount"].idxmax()
            ]


            st.warning(
                f"💸 Largest transaction: "
                f"₹{highest_row['Amount']:,.2f} "
                f"for **{highest_row['Description']}** "
                f"on **"
                f"{highest_row['Date'].strftime('%d %b %Y')}"
                f"**."
            )


            st.divider()


            # ======================================
            # CSV EXPORT
            # ======================================

            st.subheader(
                "📥 Export Analysis"
            )


            export_df = filtered_df.copy()


            export_df["Date"] = (
                export_df["Date"]
                .dt.strftime("%Y-%m-%d")
            )


            export_df = export_df[
                [
                    "ID",
                    "Amount",
                    "Category",
                    "Description",
                    "Date"
                ]
            ]


            filtered_csv = (
                export_df
                .to_csv(index=False)
                .encode("utf-8")
            )


            st.download_button(
                label="📥 Download Selected Period CSV",
                data=filtered_csv,
                file_name="filtered_expenses.csv",
                mime="text/csv",
                width="stretch"
            )


            st.divider()


            # ======================================
            # DATA TABLE
            # ======================================

            st.subheader(
                "🧾 Transactions in Selected Period"
            )


            display_df = filtered_df.copy()


            display_df["Date"] = (
                display_df["Date"]
                .dt.strftime("%Y-%m-%d")
            )


            display_df = display_df[
                [
                    "ID",
                    "Amount",
                    "Category",
                    "Description",
                    "Date"
                ]
            ]


            st.dataframe(
                display_df,
                width="stretch",
                hide_index=True
            )


        else:

            st.info(
                "📭 No expenses found for the "
                "selected period."
            )


# ============================================================
# ADD EXPENSE
# ============================================================

elif menu == "➕ Add Expense":

    st.header(
        "➕ Add New Expense"
    )


    with st.form("expense_form"):

        amount = st.number_input(
            "Expense Amount (₹)",
            min_value=0.01,
            step=10.0
        )


        category = st.selectbox(
            "Category",
            [
                "Food",
                "Travel",
                "Shopping",
                "Education",
                "Entertainment",
                "Bills",
                "Health",
                "Other"
            ]
        )


        description = st.text_input(
            "Description",
            placeholder="Example: Lunch at college"
        )


        submitted = st.form_submit_button(
            "💾 Save Expense"
        )


        if submitted:

            if not description.strip():

                st.error(
                    "❌ Please enter a description."
                )

            else:

                expense_date = datetime.now().strftime(
                    "%Y-%m-%d"
                )


                add_expense(
                    amount,
                    category,
                    description,
                    expense_date
                )


                st.success(
                    "✅ Expense saved successfully!"
                )


                st.rerun()


# ============================================================
# ADD INCOME
# ============================================================

elif menu == "💰 Add Income":

    st.header(
        "💰 Add Income"
    )


    with st.form("income_form"):

        amount = st.number_input(
            "Income Amount (₹)",
            min_value=0.01,
            step=100.0
        )


        submitted = st.form_submit_button(
            "💾 Save Income"
        )


        if submitted:

            income_date = datetime.now().strftime(
                "%Y-%m-%d"
            )


            add_income(
                amount,
                income_date
            )


            st.success(
                "✅ Income saved successfully!"
            )


            st.rerun()


# ============================================================
# SET BUDGET
# ============================================================

elif menu == "🎯 Set Budget":

    st.header(
        "🎯 Set Monthly Budget"
    )


    current_budget = get_budget()


    if current_budget > 0:

        st.info(
            f"Current Budget: "
            f"₹{current_budget:,.2f}"
        )


    with st.form("budget_form"):

        amount = st.number_input(
            "Monthly Budget (₹)",
            min_value=1.0,
            step=100.0
        )


        submitted = st.form_submit_button(
            "💾 Save Budget"
        )


        if submitted:

            set_budget(
                amount
            )


            st.success(
                f"✅ Budget set to "
                f"₹{amount:,.2f}"
            )


            st.rerun()


# ============================================================
# MANAGE EXPENSES
# ============================================================

elif menu == "🧾 Manage Expenses":

    st.header(
        "🧾 Manage Expenses"
    )


    expenses = get_expenses()


    if not expenses:

        st.info(
            "📭 No expenses available."
        )


    else:

        df = pd.DataFrame(
            expenses,
            columns=[
                "ID",
                "Amount",
                "Category",
                "Description",
                "Date"
            ]
        )


        # ======================================
        # SEARCH
        # ======================================

        search = st.text_input(
            "🔎 Search",
            placeholder=(
                "Search category or description..."
            )
        )


        # ======================================
        # CATEGORY FILTER
        # ======================================

        categories = [
            "All"
        ] + sorted(
            df["Category"].unique().tolist()
        )


        selected_category = st.selectbox(
            "🏷️ Category",
            categories
        )


        # ======================================
        # FILTER DATA
        # ======================================

        filtered_df = df.copy()


        if search:

            filtered_df = filtered_df[
                filtered_df["Category"]
                .str.contains(
                    search,
                    case=False,
                    na=False
                )
                |
                filtered_df["Description"]
                .str.contains(
                    search,
                    case=False,
                    na=False
                )
            ]


        if selected_category != "All":

            filtered_df = filtered_df[
                filtered_df["Category"]
                == selected_category
            ]


        st.write(
            f"Showing **{len(filtered_df)}** expense(s)"
        )


        categories_list = [
            "Food",
            "Travel",
            "Shopping",
            "Education",
            "Entertainment",
            "Bills",
            "Health",
            "Other"
        ]


        # ======================================
        # EXPENSE MANAGEMENT
        # ======================================

        for _, row in filtered_df.iterrows():

            expense_id = int(
                row["ID"]
            )


            with st.expander(
                f"💸 ₹{row['Amount']:,.2f} | "
                f"{row['Category']} | "
                f"{row['Description']}"
            ):


                col1, col2 = st.columns(2)


                # ==================================
                # EDIT
                # ==================================

                with col1:

                    st.subheader(
                        "✏️ Edit Expense"
                    )


                    edit_amount = st.number_input(
                        "Amount",
                        min_value=0.01,
                        value=float(
                            row["Amount"]
                        ),
                        step=10.0,
                        key=f"amount_{expense_id}"
                    )


                    if row["Category"] in categories_list:

                        category_index = (
                            categories_list.index(
                                row["Category"]
                            )
                        )

                    else:

                        category_index = 0


                    edit_category = st.selectbox(
                        "Category",
                        categories_list,
                        index=category_index,
                        key=f"category_{expense_id}"
                    )


                    edit_description = st.text_input(
                        "Description",
                        value=row["Description"],
                        key=f"description_{expense_id}"
                    )


                    edit_date = st.date_input(
                        "Date",
                        value=pd.to_datetime(
                            row["Date"]
                        ).date(),
                        key=f"date_{expense_id}"
                    )


                    if st.button(
                        "💾 Update Expense",
                        key=f"update_{expense_id}"
                    ):

                        if not edit_description.strip():

                            st.error(
                                "Description cannot be empty."
                            )

                        else:

                            update_expense(
                                expense_id,
                                edit_amount,
                                edit_category,
                                edit_description,
                                edit_date.strftime(
                                    "%Y-%m-%d"
                                )
                            )


                            st.success(
                                "✅ Expense updated!"
                            )


                            st.rerun()


                # ==================================
                # DELETE
                # ==================================

                with col2:

                    st.subheader(
                        "🗑️ Delete Expense"
                    )


                    st.write(
                        "Permanently remove this expense."
                    )


                    if st.button(
                        "🗑️ Delete Expense",
                        key=f"delete_{expense_id}"
                    ):

                        delete_expense(
                            expense_id
                        )


                        st.success(
                            "✅ Expense deleted."
                        )


                        st.rerun()