stylesheet = """
    QWidget {
        background-color: #ffffff;  # White background
        color: #333333;  # Dark gray text
        font-family: Arial, sans-serif;
        font-size: 14px;
    }

    QLabel {
        font-weight: bold;
        color: #333333;
    }

    QLineEdit {
        background-color: #ffffff;
        border: 1px solid #c0c0c0;
        padding: 5px;
        border-radius: 3px;
        color: #333333;
    }

    QComboBox {
        background-color: #ffffff;
        border: 1px solid #c0c0c0;
        padding: 5px;
        border-radius: 3px;
        color: #333333;
    }

    QPushButton {
        background-color: #007BFF;  # Blue button color
        color: white;
        padding: 8px 15px;
        border: none;
        border-radius: 5px;
        font-weight: bold;
    }

    QPushButton:hover {
        background-color: #0056b3;
    }

    QPushButton:pressed {
        background-color: #003d7a;
    }

    QTabWidget::pane {
        border: 1px solid #c0c0c0;
    }

    QTabBar::tab {
        background: #f0f0f0;  # Light gray background for inactive tabs
        border: 1px solid #c0c0c0;
        padding: 15px 20px;  # Padding for tab button text space
        margin-right: 15px;  # Space between tabs
        font-weight: bold;
        color: #333333;  # Dark gray text color for tabs
    }

    QTabBar::tab:selected {
        background: #ffffff;  # White background for the active tab
        border-bottom-color: #ffffff;
        color: #000000;  # Black text for the active tab
    }

    #logoLabel {
        min-width: 150px;
        min-height: 150px;
        max-width: 150px;
        max-height: 150px;
        background-color: #ffffff;  # White background for the logo
        padding: 10px;
        margin-left: 10px;  # Adjust positioning within the layout
    }
"""
