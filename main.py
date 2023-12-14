import tkinter as tk
from tkinter import messagebox, simpledialog
import mysql.connector

class Employee:
    def __init__(self, emp_id, emp_name, emp_salary):
        self.emp_id = emp_id
        self.emp_name = emp_name
        self.emp_salary = emp_salary

class CRUDApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Management System")

        # MySQL database connection
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='UnionSoftware7127'
        )
        self.cursor = self.conn.cursor()

        # Create the database if not exists
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS employee_management")
        self.conn.commit()

        # Switch to the employee_management database
        self.cursor.execute("USE employee_management")
        self.conn.commit()

        # Create the employees table if not exists
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                emp_id INT AUTO_INCREMENT PRIMARY KEY,
                emp_name VARCHAR(50) NOT NULL,
                emp_salary INT NOT NULL
            )
        """)
        self.conn.commit()

        self.employees = []

        self.label = tk.Label(root, text="Employee Management System", font=("Helvetica", 16))
        self.label.pack(pady=10)

        self.display_employees_button = tk.Button(root, text="Display Employees", command=self.display_employees)
        self.display_employees_button.pack(pady=5)

        self.add_employee_button = tk.Button(root, text="Add Employee", command=self.add_employee)
        self.add_employee_button.pack(pady=5)

        self.update_employee_button = tk.Button(root, text="Update Employee", command=self.update_employee)
        self.update_employee_button.pack(pady=5)

        self.delete_employee_button = tk.Button(root, text="Delete Employee", command=self.delete_employee)
        self.delete_employee_button.pack(pady=5)

        self.exit_button = tk.Button(root, text="Exit", command=self.exit_program)
        self.exit_button.pack(pady=5)

    def display_employees(self):
        self.cursor.execute("SELECT * FROM employees")
        employees_data = self.cursor.fetchall()

        self.employees = []
        for emp_data in employees_data:
            employee = Employee(*emp_data)
            self.employees.append(employee)

        if not self.employees:
            messagebox.showinfo("Employee Information", "No employees found.")
            return

        employee_info = "\nEmployees:\n"
        for employee in self.employees:
            employee_info += f"ID: {employee.emp_id}, Name: {employee.emp_name}, Salary: {employee.emp_salary}\n"
        messagebox.showinfo("Employee Information", employee_info)

    def add_employee(self):
        emp_name = simpledialog.askstring("Add Employee", "Enter the employee name:")
        emp_salary = simpledialog.askinteger("Add Employee", "Enter the employee salary:")

        # Insert the new employee into the database
        self.cursor.execute("""
            INSERT INTO employees (emp_name, emp_salary)
            VALUES (%s, %s)
        """, (emp_name, emp_salary))
        self.conn.commit()

        messagebox.showinfo("Employee Added", "New employee added successfully!")

    def update_employee(self):
        self.display_employees()

        emp_id = simpledialog.askinteger("Update Employee", "Enter the ID of the employee you want to update:")
        new_salary = simpledialog.askinteger("Update Employee", "Enter the new salary:")

        # Check if the employee exists
        self.cursor.execute("SELECT * FROM employees WHERE emp_id = %s", (emp_id,))
        emp_data = self.cursor.fetchone()
        if not emp_data:
            messagebox.showerror("Error", "Employee not found.")
            return

        # Update the employee's salary in the database
        self.cursor.execute("UPDATE employees SET emp_salary = %s WHERE emp_id = %s", (new_salary, emp_id))
        self.conn.commit()

        messagebox.showinfo("Employee Updated", "Employee information updated successfully!")

    def delete_employee(self):
        self.display_employees()

        emp_id = simpledialog.askinteger("Delete Employee", "Enter the ID of the employee you want to delete:")

        # Check if the employee exists
        self.cursor.execute("SELECT * FROM employees WHERE emp_id = %s", (emp_id,))
        emp_data = self.cursor.fetchone()
        if not emp_data:
            messagebox.showerror("Error", "Employee not found.")
            return

        # Delete the employee from the database
        self.cursor.execute("DELETE FROM employees WHERE emp_id = %s", (emp_id,))
        self.conn.commit()

        messagebox.showinfo("Employee Deleted", "Employee deleted successfully!")

    def exit_program(self):
        self.conn.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    crud_app = CRUDApp(root)
    root.mainloop()
