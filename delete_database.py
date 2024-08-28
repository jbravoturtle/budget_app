import os

if os.path.exists("budget_data.db"):
    os.remove("budget_data.db")
    print("Database deleted successfully.")
else:
    print("Database file does not exist.")
