from peewee import SqliteDatabase, Model, IntegerField, CharField, ForeignKeyField, DateField
from datetime import date

# Define the database connection
db = SqliteDatabase('budget_data.db')

# Define the User model
class User(Model):
    name = CharField()
    monthly_income = IntegerField()

    class Meta:
        database = db

# Define the Budget model
class Budget(Model):
    user = ForeignKeyField(User, backref='budgets')
    month = CharField()
    year = IntegerField()
    total_days = IntegerField()
    monthly_budget = IntegerField()

    class Meta:
        database = db

# Define the Expense model
class Expense(Model):
    budget = ForeignKeyField(Budget, backref='expenses')
    date = DateField(default=date.today)
    category = CharField()
    amount = IntegerField()

    class Meta:
        database = db

# Initialize the database
def initialize_db():
    db.connect(reuse_if_open=True)
    db.create_tables([User, Budget, Expense], safe=True)
    db.close()
