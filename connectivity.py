import mysql.connector as sql
obj=sql.connect(host="localhost",user="akash",passwd="akash")
print(obj.is_connected())
cursor=obj.cursor()
def create_database():
    cursor.execute("Create database ExamPractice")
    obj.commit()
def select():
    cursor.execute("Use ExamPractice")
    obj.commit()
def create_table():
    i=int(input("How many tables do you want to create?"))
    for index in range(i):
        name=input("Enter the name of the table that you want to create. ")
        pri=input("Enter the name of the primary key column of the table.")
        cursor.execute("create table {}({} int primary key)".format(name,pri))
        obj.commit()
        no=int(input("How many more columns do you want to create?"))
        l=[]
        for index in range(0,no):
            col=input("Enter the name of the column. ")
            l.append(col)
        for index in range(0,len(l)):
            query="Alter table {} add {} int".format(name,l[index])
            cursor.execute(query)
            obj.commit()
def show_tables():
    cursor.execute("desc Number")
    for read in cursor.fetchall():
        print(read)
select()

create_table()
show_tables()