import sqlite3
from employee import Employee

def createTable(cur): 

    #Create a table using SQL use triple quotes for multi line strings
    with connection:
        cur.execute("""CREATE TABLE if not exists employees (
                        first text,
                        last text,
                        pay integer
                    ) """)

def addEmployee(emp):

    try: 
        with connection: 
            cur.execute("INSERT INTO employees VALUES (:first,:last,:pay)", {'first':emp.first,'last':emp.last,'pay':emp.pay})
            print('Employee added successfully')
            return 
    except: 
        print('Error adding Employee to Database')
        return

def getEmployees(lastname, firstname="None"):
    try: 
        if firstname == "None":
            cur.execute("SELECT * FROM employees WHERE last=:last", {'last':lastname})
            return cur.fetchall()

        elif firstname != "None":
            cur.execute("SELECT * FROM employees WHERE last=:last, first=:first", {'last':lastname, 'first':firstname})
            return cur.fetchall()

    except: 
        print('Error Retrieving Employee')
    pass

def update_pay(emp,pay):
    with connection:
        try:
            cur.execute("""UPDATE employees SET pay = :pay
                            WHERE first = :first and last = :last""",
                        {'first':emp.first, 'last':emp.last,'pay':pay})

        except:
            print('Error Updating Pay')

def removeEmployee(emp):
    with connection:
        try: 
            cur.execute("DELETE from employees WHERE first=:first AND last = :last", {'first':emp.first, 'last':emp.last})
        except:
            print('Error removing employee')

def main(): 

    #Make connection to database. You can do it in memory using ':memory:', or connect to a db file. 
    global connection
    connection = sqlite3.connect(':memory:')

    #Create a cursor to start running SQL commands 
    global cur
    cur = connection.cursor()

    #Create table if it does not exist
    createTable(cur)

    #cur.execute("INSERT INTO employees VALUES ('Corey','Schafer',50000)")
    #addCh = addEmployee('Mary','Schafer', 75000, cur)
    emp_1 = Employee('John', 'Doe', 80000)
    addEmployee(emp_1)
    emp_2 = Employee('Jane', 'Doe', 90000)
    addEmployee(emp_2)

    emps = getEmployees('Doe')
    print(emps)

    update_pay(emp_2, 95000)
    removeEmployee(emp_1)
    emps = getEmployees('Doe')
    print(emps)

    connection.commit()

    connection.close()

main()