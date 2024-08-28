import matplotlib.pyplot as plt
from peewee import fn
from datetime import datetime
from database import Expense, Budget, User

# Visualize daily expenses by user and category
def visualize_daily_expenses_by_user():
    today = datetime.today()
    daily_expenses = (Expense
                      .select(User.name, Expense.category, fn.SUM(Expense.amount).alias('total'))
                      .join(Budget)
                      .join(User)
                      .where(Expense.date == today.date())
                      .group_by(User.name, Expense.category)
                      .dicts())

    users = {}

    for entry in daily_expenses:
        user = entry['name']
        if user not in users:
            users[user] = {}
        users[user][entry['category']] = entry['total']

    plt.figure(figsize=(10, 6))

    for user, categories in users.items():
        plt.bar([f"{user} - {cat}" for cat in categories.keys()], categories.values(), label=user)

    plt.title("Daily Expenses by User and Category")
    plt.xlabel("User and Category")
    plt.ylabel("Total Expenses")
    plt.xticks(rotation=45, ha='right')
    plt.legend()
    plt.tight_layout()
    plt.show()

# Visualize monthly expenses by user and category, including total income
def visualize_monthly_expenses_by_user():
    today = datetime.today()
    month = today.strftime('%B')
    year = today.year

    # Calculate total income for the month
    total_income = User.select(fn.SUM(User.monthly_income)).scalar()

    monthly_expenses = (Expense
                        .select(User.name, Expense.category, fn.SUM(Expense.amount).alias('total'))
                        .join(Budget)
                        .join(User)
                        .where((Budget.month == month) & (Budget.year == year))
                        .group_by(User.name, Expense.category)
                        .dicts())

    users = {}
    total_expenses = 0

    for entry in monthly_expenses:
        user = entry['name']
        if user not in users:
            users[user] = {}
        users[user][entry['category']] = entry['total']
        total_expenses += entry['total']

    plt.figure(figsize=(12, 8))

    plt.subplot(211)
    plt.bar(['Total Income', 'Total Expenses'], [total_income, total_expenses], color=['green', 'red'])
    plt.title(f"Total Income vs. Total Expenses for {month} {year}")
    plt.ylabel("Amount")

    plt.subplot(212)
    for user, categories in users.items():
        plt.bar([user], [sum(categories.values())], label=user)

    plt.title(f"Monthly Expenses by User for {month} {year}")
    plt.xlabel("User")
    plt.ylabel("Total Expenses")
    plt.xticks(rotation=45, ha='right')
    plt.legend()
    plt.tight_layout()
    plt.show()

# Visualize yearly expenses by user, combined for each month
def visualize_yearly_expenses_by_user():
    today = datetime.today()
    year = today.year

    months = [datetime(year, month, 1).strftime('%B') for month in range(1, 13)]
    monthly_totals = {month: {} for month in months}

    for month in months:
        monthly_expenses = (Expense
                            .select(User.name, fn.SUM(Expense.amount).alias('total'))
                            .join(Budget)
                            .join(User)
                            .where((Budget.month == month) & (Budget.year == year))
                            .group_by(User.name)
                            .dicts())

        for entry in monthly_expenses:
            user = entry['name']
            if user not in monthly_totals[month]:
                monthly_totals[month][user] = entry['total']
            else:
                monthly_totals[month][user] += entry['total']

    plt.figure(figsize=(14, 10))

    for month, users in monthly_totals.items():
        for user, total in users.items():
            plt.bar([f"{month} - {user}"], [total], label=f"{user} - {month}")

    plt.title(f"Yearly Expenses by User for {year}")
    plt.xlabel("Month and User")
    plt.ylabel("Total Expenses")
    plt.xticks(rotation=90)
    plt.legend()
    plt.tight_layout()
    plt.show()
