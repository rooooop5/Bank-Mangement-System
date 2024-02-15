import mysql.connector as sql

obj = sql.connect(host="localhost", user="akash", passwd="akash")
cursor = obj.cursor()
import random


def create_db_and_tables():
    cursor.execute("CREATE DATABASE IF NOT EXISTS ProjBank")
    cursor.execute("USE ProjBank")
    cursor.execute("create table if not exists Branch(branch_no int primary key)")
    # creating customer table
    cursor.execute(
        """create table if not exists Customer(customer_id bigint primary key,name varchar(100) not null,
               address varchar(200) not null unique,ph_no bigint not null unique,branch_no int,
               foreign key(branch_no) references Branch(branch_no) on delete cascade)"""
    )
    # creating Employee table
    cursor.execute(
        """create table if not exists Employee(emp_id bigint primary key,name varchar(200) not null,
               post varchar(200) not null,salary int not null,
               ph_no bigint not null unique,branch_no int references Branch(branch_no) on delete cascade on update cascade)"""
    )
    # creating Account table
    cursor.execute(
        """create table if not exists Account(acc_no bigint primary key,customer_id bigint not null,
               balance int default 0,type varchar(200),                           
               foreign key(customer_id) references Customer(customer_id) on delete cascade on update cascade)"""
    )
    # creating Transactions table
    cursor.execute(
        """create table if not exists Transactions(type varchar(200) not null,amt int,acc_no bigint not null,
               constraint acc_fkey  foreign key(acc_no) references Account(acc_no))"""
    )
    # insert branch numbers into branch table because branch number is present as foreign key in rest of the tables
    cursor.execute("SELECT COUNT(*) FROM Branch")
    chk = cursor.fetchone()[0]
    if chk == 0:
        for i in range(1, 11):
            query = "INSERT INTO Branch VALUES({})".format(
                i,
            )
            cursor.execute(query)
            obj.commit()


create_db_and_tables()


# function for creating customer record
def create_customer():
    print("\nRequest received for customer record creation.")
    customer_id = random.randint(1, 900000000001)
    name = input("Enter customer name.")
    address = input("Enter present address of customer.")
    ph_no = int(input("Enter 10 digit phone number."))
    branch_no = int(input("Enter branch number within 1-10."))
    query = "INSERT INTO Customer VALUES({},'{}','{}',{},{})".format(
        customer_id, name, address, ph_no, branch_no
    )
    cursor.execute(query)
    obj.commit()
    print("\tCustomer id of this customer is ", customer_id)
    print("\tSuccesfully created record.Exiting request.")


# function for viewing a particular customer record
def view_customer():
    print("\nRequest received for viewing customer record.")
    id = int(input("Enter your customer id."))
    found = False
    check = "SELECT customer_id FROM Customer"
    cursor.execute(check)
    for row in cursor.fetchall():
        if id in row:
            found = True
            query = "SELECT * FROM Customer WHERE customer_id={}".format(
                id,
            )
            cursor.execute(query)
            for row in cursor.fetchall():
                print(row)
            print(
                "\tRecord shown successfully in the order(Customer ID,Name,Address,Phone Number,Branch Number).Exiting request."
            )
            break
    if found == False:
        print("\tSaid customer does not exist.Exiting request.")


# function for viewing all bank accounts associated with a customer
def view_customer_acc():
    print("\nRequest received for viewing customer accounts.")
    id = int(input("Enter your customer id."))
    found = False
    check = "SELECT customer_id FROM Customer"
    cursor.execute(check)
    for row in cursor.fetchall():
        if id in row:
            found = True
            query = "SELECT * FROM Account WHERE customer_id={}".format(
                id,
            )
            cursor.execute(query)
            data = cursor.fetchall()
            if data != []:
                for row in data:
                    print(row)
                print(
                    "\tAccount shown successfully in the order(Account Number,Customer ID,Balance,Address,Type of account).Exiting request."
                )
            else:
                print("\tNo accounts are realated to this customer.")
            break
    if found == False:
        print("\tSaid account does not exist.Exiting request.")


# function for editing customer record
def edit_customer():
    print("\nRequest received for editing customer record.")
    id = int(input("Enter your customer id."))
    found = False
    check = "SELECT customer_id FROM Customer"
    cursor.execute(check)
    for row in cursor.fetchall():
        if id in row:
            found = True
            print("Customer id is okay.")
            choice = int(
                input(
                    """What do want to format?
                                For changing customer name > Enter 1
                                For changing customer address > Enter 2
                                For changing customer phone number > Enter 3
                                For changing branch number of customer > Enter 4. 
                                Input - """
                )
            )
            if choice == 1:
                new = input("\tEnter new name of customer.")
                query = "UPDATE Customer SET name='{}' WHERE customer_id={}".format(
                    new, id
                )
                cursor.execute(query)
                obj.commit()
                print("\t\tSuccessfully changed customer record.Exiting request.")
            elif choice == 2:
                new = input("\tEnter new address of customer.")
                query = "UPDATE Customer SET address='{}' WHERE customer_id={}".format(
                    new, id
                )
                cursor.execute(query)
                obj.commit()
                print("\t\tSuccessfully changed customer record.Exiting request.")
            elif choice == 3:
                new = int(input("\tEnter new phone number of customer."))
                query = "UPDATE Customer SET ph_no={} WHERE customer_id={}".format(
                    new, id
                )
                cursor.execute(query)
                obj.commit()
                print("\t\tSuccessfully changed customer record.Exiting request.")
            elif choice == 4:
                new = int(input("\tEnter new brach number of customer."))
                query = "UPDATE Customer SET branch_no={} WHERE customer_id={}".format(
                    new, id
                )
                cursor.execute(query)
                obj.commit()
                print("\t\tSuccessfully changed customer record.Exiting request.")
            else:
                print("\t\tIncorrect choice.Exiting request.")
            break
    if found == False:
        print("\tSaid customer does not exist.Exiting request.")


# function for deleting customer record
def delete_customer():
    print("\nRequest received for deleting customer record.")
    id = int(input("Enter your customer id."))
    found = False
    check = "SELECT customer_id FROM Customer"
    cursor.execute(check)
    for row in cursor.fetchall():
        if id in row:
            found = True
            print("\tCustomer id is okay.")
            choice = input(
                "\tAre you sure you want to delete your customer record?(Yes/No)"
            )
            if choice == "Yes":
                query = "DELETE FROM Customer where customer_id={}".format(id)
                cursor.execute(query)
                obj.commit()
                print("\t\tSuccessfully deleted customer record.Exiting request.")
            else:
                print("\t\tExiting request.")
            break
    if found == False:
        print("\tSuch a customer does not exist.Exiting request.")


# function for creating bank account associated with a customer
def create_acc():
    print("\nRequest received for creating account.")
    id = int(input("Enter customer id of customer who wants to create account."))
    no = random.randint(1, 900000000001)
    type = input("Enter account type.")
    query = "INSERT INTO Account(acc_no,customer_id,type) VALUES({},{},'{}')".format(
        no, id, type
    )
    cursor.execute(query)
    print("\tThe account number of this account is ", no)
    print("\tSuccessfully created account.Exiting request.")
    obj.commit()


# function for viewing a particular account
def view_account():
    print("\nRequest received for viewing bank account.")
    id = int(input("Enter your account number."))
    found = False
    check = "SELECT acc_no FROM Account"
    cursor.execute(check)
    for row in cursor.fetchall():
        if id in row:
            found = True
            query = "SELECT * FROM Account WHERE acc_no={}".format(
                id,
            )
            cursor.execute(query)
            for row in cursor.fetchall():
                print(row)
            print(
                "\tAccount shown successfully in the order(Account Number,Customer ID,Balance,Address,Type of account).Exiting request."
            )
            break
    if found == False:
        print("\tSaid account does not exist.Exiting request.")


# function for deleting bank account
def delete_acc():
    print("\nRequest received for deleting account.")
    id = int(input("Enter account number of account to be deleted."))
    found = False
    check = "SELECT acc_no FROM Account"
    cursor.execute(check)
    for row in cursor.fetchall():
        if id in row:
            found = True
            print("\tAccount number is okay.")
            choice = input("\tAre you sure you want to delete your account?(Yes/No)")
            if choice == "Yes":
                query = "DELETE FROM Account where acc_no={}".format(id)
                cursor.execute(query)
                obj.commit()
                print("\t\tSuccessfully deleted account.Exiting request.")
            else:
                print("\t\tExiting request.")
            break
    if found == False:
        print("\tSaid account does not exist.Exiting request.")


# function for editing a bank account type
def edit_acc():
    print("\nRequest received for editing account.")
    print("Only account type can be changed.")
    id = int(input("Enter account number of account to edited."))
    found = False
    check = "SELECT acc_no FROM Account"
    cursor.execute(check)
    for row in cursor.fetchall():
        if id in row:
            found = True
            print("\tAccount number is okay.")
            new = input("\tEnter new type of bank account.")
            query = "UPDATE Account SET type='{}' WHERE acc_no={}".format(new, id)
            cursor.execute(query)
            obj.commit()
            print("\t\tSuccessfully changed account type.Exiting request.")
            break
    if found == False:
        print("\tSaid account does not exist.Exiting request.")


# function for depositing money in an account
def deposit():
    print("\nRequest received for depositing funds.")
    id = int(input("Enter account number."))
    found = False
    check = "SELECT acc_no FROM Account"
    cursor.execute(check)
    for row in cursor.fetchall():
        if id in row:
            found = True
            print("\tAccount number is okay.")
            new = int(input("\tEnter sum to deposited."))
            query1 = "UPDATE Account SET balance=balance+{} WHERE acc_no={}".format(
                new, id
            )
            cursor.execute(query1)
            obj.commit()
            query2 = "INSERT INTO Transactions(type,amt,acc_no) VALUES('Deposition',{},{})".format(
                new, id
            )
            cursor.execute(query2)
            obj.commit()
            print("\t\tSuccessfully deposited in account.Exiting request.")
            break
    if found == False:
        print("\tSaid account does not exist.Exiting request.")


# function for withdrawing money from an account
def withdraw():
    print("\nRequest received for withdrawing funds.")
    id = int(input("Enter account number."))
    found = False
    check = "SELECT acc_no FROM Account"
    cursor.execute(check)
    for row in cursor.fetchall():
        if id in row:
            found = True
            print("\tAccount number is okay.")
            new = int(input("\tEnter sum to withdrawed."))
            condtn = "SELECT balance FROM Account WHERE acc_no={}".format(
                id,
            )
            cursor.execute(condtn)
            for bal in cursor.fetchall():
                if (bal[0] - new) >= 0:
                    query1 = (
                        "UPDATE Account SET balance=balance-{} WHERE acc_no={}".format(
                            new, id
                        )
                    )
                    cursor.execute(query1)
                    obj.commit()
                    query2 = "INSERT INTO Transactions(type,amt,acc_no) VALUES('Withdrawal',{},{})".format(
                        new, id
                    )
                    cursor.execute(query2)
                    obj.commit()
                    print("\t\tSuccessfully withdrawed from account.Exiting request.")
                else:
                    print(
                        "\t\tSaid amount cannot be withdrawn since balance is too low."
                    )
            break
    if found == False:
        print("\tSaid account does not exist.Exiting request.")


# function for transferring money between accounts
def fund_transfer():
    print("\nRequest received for transferring funds.")
    from_acc = int(input("FROM(provide account number) - "))
    to_acc = int(input("TO(provide account number) - "))
    check = "SELECT acc_no FROM Account"
    cursor.execute(check)
    ok1 = False
    ok2 = False
    for row in cursor.fetchall():
        if from_acc in row:
            ok1 = True
        if to_acc in row:
            ok2 = True
    if ok1 == True and ok2 == True:
        print("\tBoth accounts are valid and exist.")
        amt = int(input("\tEnter amount to be transferred."))
        condtn = "SELECT balance FROM Account WHERE acc_no={}".format(
            from_acc,
        )
        cursor.execute(condtn)
        for bal in cursor.fetchall():
            if (bal[0] - amt) >= 0:
                query1 = "UPDATE Account SET balance=balance-{} WHERE acc_no={}".format(
                    amt, from_acc
                )
                query2 = "UPDATE Account SET balance=balance+{} WHERE acc_no={}".format(
                    amt, to_acc
                )
                cursor.execute(query1)
                cursor.execute(query2)
                print("\t\tFund successfully transferred.Exiting request.")
                obj.commit()
                query3 = "INSERT INTO Transactions(type,amt,acc_no) VALUES('Credit',{},{})".format(
                    amt, to_acc
                )
                query4 = "INSERT INTO Transactions(type,amt,acc_no) VALUES('Debit',{},{})".format(
                    amt, from_acc
                )
                cursor.execute(query3)
                cursor.execute(query4)
                obj.commit()
            else:
                print("\t\tSaid amount cannot be transferred since balance is too low.")
            break
    else:
        print("\tBoth accounts are not valid.")


# function for viewing all transactions associated with an account
def view_transactions():
    print("\nRequest received for viewing transaction records.")
    id = int(input("Enter your account number."))
    found = False
    check = "SELECT acc_no FROM Account"
    cursor.execute(check)
    for row in cursor.fetchall():
        if id in row:
            found = True
            query = "SELECT * FROM Transactions WHERE acc_no={}".format(
                id,
            )
            cursor.execute(query)
            data = cursor.fetchall()
            if data != []:
                for row in data:
                    print(row)
                print("\tTransactions shown successfully.Exiting request.")
            else:
                print("\tNo transactions related to this account have occured.")
            break
    if found == False:
        print("Said account does not exist.Exiting request.")


# function for creating employee record
def create_emp():
    print("\nRequest received for employee record creation.")
    emp_id = random.randint(1, 900000000001)
    name = input("Enter employee name.")
    post = input("Enter current post of employee.")
    ph_no = int(input("Enter 10 digit phone number."))
    salary = int(input("Enter salary of employee."))
    branch_no = int(input("Enter branch number within 1-10."))
    query = "INSERT INTO Employee VALUES({},'{}','{}',{},{},{})".format(
        emp_id, name, post, salary, ph_no, branch_no
    )
    cursor.execute(query)
    obj.commit()
    print("\tEmployee ID of this employee is ", emp_id)
    print("\tSuccesfully created record.Exiting request.")


# function for editing employee record
def edit_emp():
    print("\nRequest received for editing employee record.")
    id = int(input("Enter your employee id."))
    found = False
    check = "SELECT emp_id FROM Employee"
    cursor.execute(check)
    for row in cursor.fetchall():
        if id in row:
            found = True
            print("Employee id is okay.")
            choice = int(
                input(
                    """What do want to format?
                                For changing employee name > Enter 1
                                For changing employee post > Enter 2
                                For changing employee phone number > Enter 3
                                For changing employee salary > Enter 4
                                For changing branch number of employee > Enter 5. 
                                Input - """
                )
            )
            if choice == 1:
                new = input("\tEnter new name of employee.")
                query = "UPDATE Employee SET name='{}' WHERE emp_id={}".format(new, id)
                cursor.execute(query)
                obj.commit()
                print("\t\tSuccessfully changed employee record.Exiting request.")
            elif choice == 2:
                new = input("\tEnter new post of employee.")
                query = "UPDATE Employee SET post='{}' WHERE emp_id={}".format(new, id)
                cursor.execute(query)
                obj.commit()
                print("\t\tSuccessfully changed employee record.Exiting request.")
            elif choice == 3:
                new = int(input("\tEnter new phone number of employee."))
                query = "UPDATE Employee SET ph_no={} WHERE emp_id={}".format(new, id)
                cursor.execute(query)
                obj.commit()
                print("\t\tSuccessfully changed employee record.Exiting request.")
            elif choice == 4:
                new = int(input("\tEnter new salary of employee."))
                query = "UPDATE Employee SET salary={} WHERE emp_id={}".format(new, id)
                cursor.execute(query)
                obj.commit()
                print("\t\tSuccessfully changed employee record.Exiting request.")

            elif choice == 5:
                new = int(input("\tEnter new brach number of employee."))
                query = "UPDATE Employee SET branch_no={} WHERE emp_id={}".format(
                    new, id
                )
                cursor.execute(query)
                obj.commit()
                print("\t\tSuccessfully changed employee record.Exiting request.")
            else:
                print("\t\tIncorrect choice.Exiting request.")
            break
    if found == False:
        print("\tSaid employee does not exist.Exiting request.")


# function for deleting employee record
def delete_emp():
    print("\nRequest received for deleting employee record.")
    id = int(input("Enter your employee id."))
    found = False
    check = "SELECT emp_id FROM Employee"
    cursor.execute(check)
    for row in cursor.fetchall():
        if id in row:
            found = True
            print("\tEmployee id is okay.")
            choice = input(
                "\tAre you sure you want to delete your employee record?(Yes/No)-"
            )
            if choice == "Yes":
                query = "DELETE FROM Employee where emp_id={}".format(id)
                cursor.execute(query)
                obj.commit()
                print("\t\tSuccessfully deleted employee record.Exiting request.")
            else:
                print("\t\tExiting request.")
            break
    if found == False:
        print("\tSuch a employee does not exist.Exiting request.")


# function for viewing employee record
def view_emp():
    print("\nRequest received for viewing employee record.")
    id = int(input("Enter your employee id."))
    found = False
    check = "SELECT emp_id FROM Employee"
    cursor.execute(check)
    for row in cursor.fetchall():
        if id in row:
            found = True
            query = "SELECT * FROM Employee WHERE emp_id={}".format(
                id,
            )
            cursor.execute(query)
            for row in cursor.fetchall():
                print(row)
            print(
                "\tRecord shown successfully in the order(Employee ID,Name,Address,Branch Number,Phone Number.Exiting request."
            )
            break
    if found == False:
        print("\tSaid employee does not exist.Exiting request.")


# if else statement for running various functions of the banking system
choice = "Y"
while choice == "Y":
    ans = input(
        (
            """What Queries do you want to run?
                      For dealing with Customer records > Enter C
                      For dealing with Account records > Enter A
                      For dealing with Transactions > Enter T
                      For dealing with Employee records > Enter E. 
                           Input - """
        )
    )
    if ans == "C":
        q = int(
            input(
                """         For creating customer record > Enter 1
         For editing customer record > Enter 2
         For viewing customer record > Enter 3
         For viewing accounts related to a customer > Enter 4
         For deleting customer record > Enter 5
                    Input - """
            )
        )
        if q == 1:
            create_customer()
        elif q == 2:
            edit_customer()
        elif q == 3:
            view_customer()
        elif q == 4:
            view_customer_acc()
        elif q == 5:
            delete_customer()
        else:
            print("Wrong choice.")
        choice = input("\nDo you want to run more queries? Enter Y/N - ")
    elif ans == "A":
        q = int(
            input(
                """         For creating bank account > Enter 1
         For editing bank account > Enter 2
         For viewing bank account > Enter 3
         For deleting bank account > Enter 4
                    Input - """
            )
        )
        if q == 1:
            create_acc()
        elif q == 2:
            edit_acc()
        elif q == 3:
            view_account()
        elif q == 4:
            delete_acc()
        else:
            print("Wrong choice.")
        choice = input("\nDo you want to run more queries? Enter Y/N - ")
    elif ans == "T":
        q = int(
            input(
                """         For depositing funds > Enter 1
         For withdrawing funds > Enter 2
         For transferring funds to another account > Enter 3
         For viewing transactions related to account > Enter 4
                    Input - """
            )
        )
        if q == 1:
            deposit()
        elif q == 2:
            withdraw()
        elif q == 3:
            fund_transfer()
        elif q == 4:
            view_transactions()
        else:
            print("Wrong choice")
        choice = input("\nDo you want to run more queries? Enter Y/N - ")
    elif ans == "E":
        q = int(
            input(
                """         For creating employee record > Enter 1
         For editing employee record > Enter 2
         For viewing employee record > Enter 3
         For deleting employee record > Enter 4
                    Input - """
            )
        )
        if q == 1:
            create_emp()
        elif q == 2:
            edit_emp()
        elif q == 3:
            view_emp()
        elif q == 4:
            delete_emp()
        else:
            print("Wrong choice.")
        choice = input("\nDo you want to run more queries? Enter Y/N - ")
