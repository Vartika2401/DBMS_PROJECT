import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QStackedWidget
from main_menu import main_menu
from customer import customer
from admin import admin
from add_product import add_product
import functions
import mysql.connector

class MainWindow(QMainWindow):
#     online retail store
    def __init__(self):
        super().__init__()


        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)

        #create the screens
        self.main_menu = main_menu()
        self.customer_menu = customer()
        self.admin_menu = admin()
        self.add_product = add_product()
        #add them to the QStackedWidget
        self.stacked_widget.addWidget(self.main_menu)
        self.stacked_widget.addWidget(self.customer_menu)
        self.stacked_widget.addWidget(self.admin_menu)
        self.stacked_widget.addWidget(self.add_product)


        # Connect the button signals to the slot that changes the current widget
        self.main_menu.customer_menu_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.customer_menu))
        self.customer_menu.back_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.main_menu))
        self.main_menu.admin_menu_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.admin_menu))
        self.admin_menu.back_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.main_menu))
        self.admin_menu.view_products_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(functions.view_products(self).show()))
        self.admin_menu.view_categories_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(functions.view_categories(self).show()))
        self.admin_menu.add_product_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(functions.add_product_func(self)))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
