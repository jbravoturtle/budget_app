import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QComboBox, QTabWidget, QMessageBox,
                             QInputDialog, QLineEdit, QPushButton)
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt
from styles import stylesheet  # Ensure this file has the correct stylesheet string
from database import initialize_db, User, Budget, Expense
from visualize import visualize_daily_expenses_by_user, visualize_monthly_expenses_by_user, visualize_yearly_expenses_by_user
from datetime import datetime

class ProfilesTab(QWidget):
    def __init__(self, user_combo):
        super().__init__()
        self.user_combo = user_combo  # Pass the shared user_combo
        self.initUI()

    def initUI(self):
        self.load_button = QPushButton('Load Profile', self)
        self.load_button.clicked.connect(self.load_profile)

        self.add_user_button = QPushButton('Add New User', self)
        self.add_user_button.clicked.connect(self.add_new_user)

        self.remove_user_button = QPushButton('Remove User', self)
        self.remove_user_button.clicked.connect(self.remove_user)

        self.update_button = QPushButton('Update Profile', self)
        self.update_button.clicked.connect(self.update_profile)

        # Create and center align the welcome label
        welcome_label = QLabel(
            "Welcome to the Budget Management System!\n\n"
            "Prepare for a reality check.\n"
            "This isn’t just an app; it’s a harsh spotlight on your spending habits.\n"
            "Create or select an account and face the financial truth!"
        )
        welcome_label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.addWidget(welcome_label)
        layout.addWidget(self.user_combo)
        layout.addWidget(self.load_button)
        layout.addWidget(self.add_user_button)
        layout.addWidget(self.remove_user_button)
        layout.addWidget(self.update_button)

        self.setLayout(layout)

    def load_users(self):
        self.user_combo.clear()
        users = User.select()
        for user in users:
            self.user_combo.addItem(user.name, user.id)

    def load_profile(self):
        user_id = self.user_combo.currentData()
        if user_id:
            user = User.get_by_id(user_id)
            QMessageBox.information(self, 'Profile Loaded', f'Profile for {user.name} loaded.')

    def add_new_user(self):
        name, ok = QInputDialog.getText(self, 'Add New User', 'Enter the name of the new user:')
        if ok and name:
            monthly_income, ok = QInputDialog.getInt(self, 'Add New User', 'Enter the monthly income:')
            if ok:
                User.create(name=name, monthly_income=monthly_income)
                self.load_users()
                self.user_combo.addItem(name, User.get(User.name == name).id)  # Add new user to the combo box
                QMessageBox.information(self, 'Success', f'New user {name} added successfully.')

    def remove_user(self):
        user_id = self.user_combo.currentData()
        if user_id:
            user = User.get_by_id(user_id)
            user.delete_instance()
            self.load_users()
            self.user_combo.removeItem(self.user_combo.currentIndex())  # Remove the user from the combo box
            QMessageBox.information(self, 'Success', f'User {user.name} removed successfully.')

    def update_profile(self):
        user_id = self.user_combo.currentData()
        if user_id:
            user = User.get_by_id(user_id)
            new_name, ok = QInputDialog.getText(self, 'Update Profile', 'Enter new name:')
            if ok and new_name:
                user.name = new_name
            new_income, ok = QInputDialog.getInt(self, 'Update Profile', 'Enter new monthly income:')
            if ok:
                user.monthly_income = new_income
            user.save()
            self.load_users()
            self.user_combo.setItemText(self.user_combo.currentIndex(), new_name)  # Update name in the combo box
            QMessageBox.information(self, 'Success', f'Profile updated successfully.')

class ExpenseTab(QWidget):
    def __init__(self, user_combo):
        super().__init__()
        self.user_combo = user_combo  # Pass the shared user_combo
        self.initUI()

    def initUI(self):
        self.category_label = QLabel('Expense Category:', self)
        self.category_combo = QComboBox(self)
        self.category_combo.addItems([
            'Food',
            'Bills',
            'Construction Materials',
            'Apartment Maintenance',
            'Travel',
            'Entertainment',
            'Transportation',
            'Health & Fitness',
            'Personal Care',
            'Education',
            'Gifts & Donations',
            'Household Supplies',
            'Other'
        ])

        self.expense_label = QLabel('Expense Amount:', self)
        self.expense_edit = QLineEdit(self)

        self.add_expense_button = QPushButton('Add Expense', self)
        self.add_expense_button.clicked.connect(self.add_expense)

        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.addWidget(QLabel('Select the appropriate expense type & amount!'))
        layout.addWidget(self.user_combo)
        layout.addWidget(self.category_label)
        layout.addWidget(self.category_combo)
        layout.addWidget(self.expense_label)
        layout.addWidget(self.expense_edit)
        layout.addWidget(self.add_expense_button)

        self.setLayout(layout)

    def add_expense(self):
        user_id = self.user_combo.currentData()
        if user_id is None:
            QMessageBox.warning(self, 'Error', 'Please select a user.')
            return

        category = self.category_combo.currentText()
        try:
            amount = int(self.expense_edit.text())
        except ValueError:
            QMessageBox.warning(self, 'Error', 'Invalid amount. Please enter a number.')
            return

        expense_date = datetime.now().date()

        today = datetime.today()
        month = today.strftime('%B')
        year = today.year

        try:
            budget = Budget.get(Budget.user == user_id, Budget.month == month, Budget.year == year)
        except Budget.DoesNotExist:
            budget = Budget.create(user=user_id, month=month, year=year, total_days=today.day,
                                   monthly_budget=User.get_by_id(user_id).monthly_income)

        Expense.create(budget=budget, date=expense_date, category=category, amount=amount)

        QMessageBox.information(self, 'Success',
                                f'Expense of {amount} in {category} on {expense_date} has been successfully recorded.')
        self.expense_edit.clear()

class ReportsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.daily_button = QPushButton('Visualize Daily Expenses by User', self)
        self.daily_button.clicked.connect(self.visualize_daily_expenses_by_user)

        self.monthly_button = QPushButton('Visualize Monthly Expenses by User', self)
        self.monthly_button.clicked.connect(self.visualize_monthly_expenses_by_user)

        self.yearly_button = QPushButton('Visualize Yearly Expenses by User', self)
        self.yearly_button.clicked.connect(self.visualize_yearly_expenses_by_user)

        layout = QVBoxLayout()
        layout.addWidget(QLabel('Pick a report, and let\'s find out just how bad things really are :('))
        layout.setSpacing(10)
        layout.addWidget(self.daily_button)
        layout.addWidget(self.monthly_button)
        layout.addWidget(self.yearly_button)

        self.setLayout(layout)

    def visualize_daily_expenses_by_user(self):
        visualize_daily_expenses_by_user()

    def visualize_monthly_expenses_by_user(self):
        visualize_monthly_expenses_by_user()

    def visualize_yearly_expenses_by_user(self):
        visualize_yearly_expenses_by_user()

class LogoLabel(QLabel):
    def __init__(self, image_path, parent=None):
        super().__init__(parent)
        self.image_path = image_path

    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap(self.image_path).scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        painter.drawPixmap(0, 0, pixmap)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Budget Management System')

        # Create a logo label without circular styling
        logo_label = LogoLabel('logo.png', self)
        logo_label.setFixedSize(150, 150)  # Set a fixed size for the logo

        # Create a shared QComboBox for user selection
        self.user_combo = QComboBox(self)
        self.load_users()

        # Create and center align the "Select Profile" label
        select_profile_label = QLabel('Select Profile:')
        select_profile_label.setAlignment(Qt.AlignCenter)

        # Create tabs
        self.tabs = QTabWidget()

        self.profiles_tab = ProfilesTab(self.user_combo)
        self.expense_tab = ExpenseTab(self.user_combo)
        self.reports_tab = ReportsTab()

        self.tabs.addTab(self.profiles_tab, 'Profiles')
        self.tabs.addTab(self.expense_tab, 'Add Expense')
        self.tabs.addTab(self.reports_tab, 'Reports')

        # Create a layout for the logo and tabs
        logo_layout = QHBoxLayout()
        logo_layout.addStretch(1)
        logo_layout.addWidget(logo_label)
        logo_layout.addStretch(1)

        main_layout = QVBoxLayout()
        main_layout.addLayout(logo_layout)
        main_layout.addWidget(select_profile_label)
        main_layout.addWidget(self.user_combo)
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)

    def load_users(self):
        self.user_combo.clear()
        users = User.select()
        for user in users:
            self.user_combo.addItem(user.name, user.id)

def main():
    initialize_db()
    app = QApplication(sys.argv)

    # Apply the stylesheet from styles.py
    app.setStyleSheet(stylesheet)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
