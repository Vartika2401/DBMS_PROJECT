import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QStackedWidget, \
    QLineEdit, QMessageBox
import functions
class add_to_cart(QWidget):
    print("add to cart")
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.tci = take_cus_input()
        self.back_button = QPushButton("Back")
        self.back_button.move(50, 200)
        layout.addWidget(self.back_button)
        self.add_to_cart_button = QPushButton("Add to cart")
        self.add_to_cart_button.move(150, 200)
        layout.addWidget(self.add_to_cart_button)
        self.quantity_label = QLabel("Quantity")
        self.quantity_label.move(450, 200)
        layout.addWidget(self.quantity_label)
        self.quantity_label = QLineEdit()
        self.quantity_label.move(550, 200)
        layout.addWidget(self.quantity_label)
        self.id_label = QLabel("ID")
        self.id_label.move(450, 200)
        layout.addWidget(self.id_label)
        self.id = QLineEdit()
        self.id.move(550, 200)
        layout.addWidget(self.id)


    def save_Details(self,customer_id):
        print("save details")
        print(customer_id)
        self.quantity = self.quantity_label.text()
        self.id = self.id.text()
        print(self.quantity_label)
        print(self.id)
        customer_id = customer_id
        if self.quantity == "" or self.id == "":
            self.error = QLabel("Please fill all the fields")
        else:
            functions.add_to_cart_func(self, self.quantity, self.id,customer_id)
            QMessageBox.information(self, "Success", "Product added to cart successfully")
        return self.quantity, self.id, customer_id


class take_cus_input(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        self.customer_id_label = QLabel("Customer ID")
        self.customer_id_label.move(50, 200)
        layout.addWidget(self.customer_id_label)
        self.customer_id = QLineEdit()
        self.customer_id.move(150, 200)
        layout.addWidget(self.customer_id)
        self.customer_id_button = QPushButton("Enter")
        self.customer_id_button.move(250, 200)
        layout.addWidget(self.customer_id_button)
        self.customer_id_button.clicked.connect(self.save_customer_id)
    def save_customer_id(self):
        self.customer_id_save = self.customer_id.text()
        QMessageBox.information(self, "Success", "Customer ID saved successfully")

        # return self.customer_id_save
    def forget_customer_id(self):
        self.customer_id = ""

class place_order(QWidget):
    def __init__(self):
        




