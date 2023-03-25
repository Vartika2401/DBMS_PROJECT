import mysql.connector
from mysql.connector import errorcode
#connecting to the database
db = mysql.connector.connect(host="localhost", user="prakhar", passwd="prakhar", database="test")
cursor = db.cursor()
def starting_menu():
    print("Hello! Welcome to the retail store database management system.")
    print("Please select an option from the following:")
    print("1. Customer")
    print("2. Delivery Man")
    print("3. Admin")
    print("4. Exit")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        id = customer_verification()
        if (id!=-1):
            customer_menu(id)
        else:
            starting_menu()
    elif choice == 2:
        id = delivery_man_verification()    
        if (id!=-1):
            delivery_man_menu(id)
        else:
            starting_menu()
    elif choice == 3:
        id = admin_verification()
        if (id!=-1):   
            admin_menu(id)
        else:
            starting_menu()
    elif choice == 4:
        exit()
    else:
        print("Invalid choice. Please try again.")
        starting_menu()
def customer_verification():
    print("Please enter your customer ID: ")
    id = int(input())
    cursor.execute("SELECT * FROM CUSTOMER WHERE CUSTOMER_ID = %s", (id,))
    res = cursor.fetchall()
    if len(res) == 0:
        print("Invalid customer ID. Please try again.")
        return -1
    else:
        return id
def delivery_man_verification():
    print("Please enter your delivery ID:")
    id = int(input())
    cursor.execute("Select * from delivery_man where delivery_id = %s", (id,))
    res = cursor.fetchall()
    if len(res) == 0:
        print("Invalid delivery ID. Please try again.")
        return -1
    else:
        return id
def admin_verification():
    print("please enter your admin ID:")
    id = int(input())
    cursor.execute("Select * from admin where admin_id = %s", (id,))
    res = cursor.fetchall()
    if len(res) == 0:
        print("Invalid admin ID. Please try again.")
        return -1
    else:
        return id
def view_products():
    print("Please select an option from the following: ")
    print("1. View all products")
    print("2. View products by category")
    print("3. View products by price range")
    print("4. Exit")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        cursor.execute("SELECT * FROM PRODUCT")
        res = cursor.fetchall()
        for i in res:
            print("Product ID: " + str(i[0]) + " Product name: " + str(i[1]) + " Product price: " + str(i[2]) + " Product quantity: " + str(i[3]))
    elif choice == 2:
        category_id = int(input("Enter category ID: "))
        cursor.execute("SELECT * FROM PRODUCT WHERE CATEGORY_ID = %s", (category_id,))
        res = cursor.fetchall()
        for i in res:
            print("Product ID: " + str(i[0]) + " Product name: " + str(i[1]) + " Product price: " + str(i[2]) + " Product quantity: " + str(i[3]))
    elif choice == 3:
        min_price = int(input("Enter minimum price: "))
        max_price = int(input("Enter maximum price: "))
        cursor.execute("SELECT * FROM PRODUCT WHERE PRODUCT_PRICE BETWEEN %s AND %s", (min_price, max_price))
        res = cursor.fetchall()
        for i in res:
            print("Product ID: " + str(i[0]) + " Product name: " + str(i[1]) + " Product price: " + str(i[2]) + " Product quantity: " + str(i[3]))
    elif choice == 4:
        customer_menu()
    else:
        print("Invalid choice. Please try again.")
        view_products()
def view_categories():
    cursor.execute("SELECT * FROM CATEGORY")
    res = cursor.fetchall()
    for i in res:
        print("Category ID: " + str(i[0]) + " Category name: " + str(i[1]))
    customer_menu()
def view_cart(id):
    cursor.execute("SELECT * FROM CART WHERE CUSTOMER_ID = %s", (id,))
    res = cursor.fetchall()
    total_price = 0
    total_quantity = 0
    for i in res:
        print("Product ID: " + str(i[1]) + " Product name: " + str(i[2]) + " Product price: " + str(i[3]) + " Product quantity: " + str(i[4]))
        total_price += i[3]*i[4]
        total_quantity += i[4]
    print("Total price: " + str(total_price))
    print("Total quantity: " + str(total_quantity))
    customer_menu(id)
def add_to_cart(id):
    print("Please enter the product ID: ")
    product_id = int(input())
    print("Please enter the quantity: ")
    quantity = int(input())
    cursor.execute("INSERT INTO CART VALUES (%s, %s, %s, %s, %s)", (id, product_id, quantity, 0, 0))
    db.commit()  
def remove_from_cart(id):
    print("Please enter the product ID: ")
    product_id = int(input())
    cursor.execute("DELETE FROM CART WHERE CUSTOMER_ID = %s AND PRODUCT_ID = %s", (id, product_id))
    db.commit()
def order_history(id):
    #count the number of orders placed by the customer
    cursor.execute("select count(*) from all_orders where customer_id = %s group by order_id", (id,))
    res = cursor.fetchall()
    print("Number of orders placed: " + str(len(res)))
    #display the order history
    cursor.execute("select order_id from all_orders where customer_id = %s group by order_id", (id,))
    res = cursor.fetchall()
    for i in res:
        print("Order ID: " + str(i[0]))
        cursor.execute("select product_quantity, product_price from all_orders where order_id = %s and customer_id = %s", (i[0], id))
        res1 = cursor.fetchall()
        total_price = 0
        total_quantity = 0
        for j in res1:
            print("Product quantity: " + str(j[0]) + " Product price: " + str(j[1]))
            total_price += j[0]*j[1]
            total_quantity += j[0]
        print("Total price: " + str(total_price))
        print("Total quantity: " + str(total_quantity))
def place_order(id):
    cursor.execute("Insert into orders(customer_id, order_datetime) values (%s, now())", (id,))
    db.commit()
    print("Order placed successfully!")
def change_password(id):
    password = input("Enter new password: ")
    cursor.execute("update customer set customer_password=" + password + " where customer_id=" + id)
    db.commit()
def change_wallet_balance(id):
    wallet_balance = int(input("Enter new wallet balance: "))
    cursor.execute("update customer set wallet_balance=" + wallet_balance + " where customer_id=" + id)
    db.commit()
def delivery_man_details(id):
    # check whether the customer has placed an order
    cursor.execute("select count(*) from orders where customer_id = %s", (id,))
    res = cursor.fetchall()
    if res[0][0] == 0:
        print("You have not placed any orders yet.")
    else:
        #fetch the details of the delivery man for the respective order and customer ID
        cursor.execute("select order_id from orders where customer_id = %s", (id,))
        res = cursor.fetchall()
        customer_order_id = res[0][0]
        cursor.execute("select delivery_man_id from order_delivery_man where order_id = %s", (customer_order_id,))
        res = cursor.fetchall()
        delivery_man_id = res[0][0]
        cursor.execute("select man_name, man_contact, man_email, man_pass from delivery_man where delivery_man_id = %s", (delivery_man_id,))
def customer_menu(id):
    print("Hello! Welcome to the customer menu.")
    print("Please select an option from the following:")
    print("1. View products")
    print("2. View categories")
    print("3. View cart")
    print("4. Add to cart")
    print("5. Remove from cart")
    print("6. Place order")
    print("7. Change password")
    print("8. Change wallet balance")
    print("9. Order history")
    print("10. Check the details of the assigned delivery man")
    print("11. Exit")
    print("12. Go Back")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        view_products()
    elif choice == 2:
        view_categories()
    elif choice == 3:  
        view_cart(id)
    elif choice == 4:
        add_to_cart(id)
    elif choice == 5:
        remove_from_cart(id)
    elif choice == 6:
        place_order(id)
    elif choice == 7:
        change_password(id)
    elif choice == 8:
        change_wallet_balance(id)
    elif choice == 9:
        order_history(id)
    elif choice == 10:
        delivery_man_details(id)
    elif choice == 11:
        exit()
    elif choice == 12:
        starting_menu()
    else:
        print("Invalid choice. Please try again.")
        customer_menu()
def view_orders_to_be_delivered(id):
    cursor.execute("select order_id from order_delivery_man where delivery_man_id = %s", (id,))
    res = cursor.fetchall()
    for i in res:
        cursor.execute("select order_id, order_datetime, order_amount, customer_id from orders where order_id = %s", (i[0],))
        res1 = cursor.fetchall()
        print("Order ID: " + str(res1[0][0]))
        print("Order date and time: " + str(res1[0][1]))
        print("Order amount: " + str(res1[0][2]))
        print("Customer ID: " + str(res1[0][3]))
def view_customer_details_for_order(id):
    print("Enter the order ID for which you want to view the customer details: ")
    order_id = int(input())
    cursor.execute("select customer_id from orders where order_id = %s", (order_id,))
    res = cursor.fetchall()
    customer_id = res[0][0]
    cursor.execute("select customer_fname, customer_lname, customer_contact_number, customer_address_buildingno, customer_address_street, customer_address_city, customer_address_state, customer_address_pincode from customer where customer_id = %s", (customer_id,))
    res = cursor.fetchall()
    print("Customer first name: " + str(res[0][0]))
    print("Customer last name: " + str(res[0][1]))
    print("Customer contact number: " + str(res[0][2]))
    print("Customer address building number: " + str(res[0][3]))
    print("Customer address street: " + str(res[0][4]))
    print("Customer address city: " + str(res[0][5]))
    print("Customer address state: " + str(res[0][6]))
    print("Customer address pincode: " + str(res[0][7]))
def change_delivery_man_password(id):
    password = input("Enter new password: ")
    cursor.execute("update delivery_man set man_pass = %s where delivery_man_id = %s", (password, id))
    db.commit()
def delivery_man_menu(id):
    print("Hello! Welcome to the delivery man menu")
    print("Please select an option from the following:")
    print("1. View orders")
    print("2. View customer details")
    print("3. Change password")
    print("4. Exit")
    print("5. Go Back")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        view_orders_to_be_delivered(id)
    elif choice == 2:
        view_customer_details_for_order(id)
    elif choice == 3:
        change_delivery_man_password(id)
    elif choice == 4:   
        exit()
    elif choice == 5:
        starting_menu()
    else:
        print("Invalid choice. Please try again.")
        delivery_man_menu(id)
def add_product():
    product_name = input("Enter product name: ")
    product_price = int(input("Enter product price: "))
    product_quantity = int(input("Enter product quantity: "))
    product_category = input("Enter product category: ")
    cursor.execute("insert into product (product_name, product_price, product_quantity, product_category) values (%s, %s, %s, %s)", (product_name, product_price, product_quantity, product_category))
    db.commit()
def add_category():
    category_name = input("Enter category name: ")
    cursor.execute("insert into category (category_name) values (%s)", (category_name,))
    db.commit()
def remove_product():
    product_id = int(input("Enter product ID: "))
    cursor.execute("delete from product where product_id = %s", (product_id,))
    db.commit()
def remove_category():
    category_name = input("Enter category name: ")
    cursor.execute("delete from category where category_name = %s", (category_name,))
    db.commit()
def change_product_price():
    product_id = int(input("Enter product ID: "))
    product_price = int(input("Enter new product price: "))
    if (product_price < 0):
        print("Invalid price. Please try again.")
        change_product_price()
    else:
        cursor.execute("update product set product_price = %s where product_id = %s", (product_price, product_id))
        db.commit()
def change_product_quantity():
    product_id = int(input("Enter product ID: "))
    product_quantity = int(input("Enter new product quantity: "))
    if (product_quantity < 0):
        print("Invalid quantity. Please try again.")
        change_product_quantity()
    else:
        cursor.execute("update product set product_quantity = %s where product_id = %s", (product_quantity, product_id))
        db.commit()
def change_admin_password(id):
    password = input("Enter new password: ")
    cursor.execute("update admin_shop set admin_password = %s where admin_id = %s", (password, id))
def admin_menu(id):
    print("Hello! Welcome to the admin menu")
    print("Please select an option from the following:")
    print("1. View products")
    print("2. View categories")
    print("3. Add product")
    print("4. Add category")
    print("5. Remove product")
    print("6. Remove category")
    print("7. Change product price")
    print("8. Change product quantity")
    print("9. Change password")
    print("10. Exit")
    print("11. Go Back")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        view_products()
    elif choice == 2:
        view_categories()
    elif choice == 3:
        add_product()
    elif choice == 4:
        add_category()
    elif choice == 5:
        remove_product()
    elif choice == 6:
        remove_category()
    elif choice == 7:
        change_product_price()
    elif choice == 8:
        change_product_quantity()
    elif choice == 9:
        change_password(id)
    elif choice == 10:
        exit()
    elif choice == 11:
        starting_menu()
    else:
        print("Invalid choice. Please try again.")
        admin_menu(id)   
starting_menu()