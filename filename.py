import json

# Base Employee class (Encapsulation)
class Employee:
    def __init__(self, emp_id, name, salary, department):
        self.emp_id = emp_id
        self.name = name
        self.salary = salary
        self.department = department

    def display(self):
        print(f"ID: {self.emp_id}, Name: {self.name}, Salary: ₹{self.salary:,.2f}, Department: {self.department}")

    def to_dict(self):
        return {
            "emp_id": self.emp_id,
            "name": self.name,
            "salary": self.salary,
            "department": self.department,
            "role": self.__class__.__name__
        }


# Derived classes (Inheritance & Polymorphism)
class Manager(Employee):
    def display(self):
        print(f"[Manager] ID: {self.emp_id}, Name: {self.name}, Salary: ₹{self.salary:,.2f}, Department: {self.department}")


class Developer(Employee):
    def display(self):
        print(f"[Developer] ID: {self.emp_id}, Name: {self.name}, Salary: ₹{self.salary:,.2f}, Department: {self.department}")


# Employee System
class EmployeeSystem:
    def __init__(self):
        self.employees = []
        self.load_from_file()

    def add_employee(self, emp):
        if any(e.emp_id == emp.emp_id for e in self.employees):
            print("❌ Employee with this ID already exists!")
            return
        self.employees.append(emp)
        self.save_to_file()
        print("✅ Employee added successfully!")

    def remove_employee(self, emp_id):
        before_count = len(self.employees)
        self.employees = [emp for emp in self.employees if emp.emp_id != emp_id]
        self.save_to_file()
        if len(self.employees) < before_count:
            print("✅ Employee removed successfully!")
        else:
            print("❌ Employee not found!")

    def update_employee(self, emp_id, salary=None, department=None):
        for emp in self.employees:
            if emp.emp_id == emp_id:
                if salary:
                    emp.salary = salary
                if department:
                    emp.department = department
                self.save_to_file()
                print("✅ Employee updated successfully!")
                return
        print("❌ Employee not found!")

    def promote_employee(self, emp_id, increment):
        for emp in self.employees:
            if emp.emp_id == emp_id:
                emp.salary += increment
                self.save_to_file()
                print(f"✅ Employee promoted! New salary: ₹{emp.salary:,.2f}")
                return
        print("❌ Employee not found!")

    def search_employee(self, emp_id=None, name=None):
        for emp in self.employees:
            if emp_id and emp.emp_id == emp_id:
                emp.display()
                return
            if name and emp.name.lower() == name.lower():
                emp.display()
                return
        print("❌ Employee not found!")

    def display_all(self):
        if not self.employees:
            print("⚠ No employees found!")
            return
        print("\n--- Employee List ---")
        for emp in self.employees:
            emp.display()

    def sort_employees(self, key="salary", reverse=False):
        self.employees.sort(key=lambda x: getattr(x, key), reverse=reverse)
        print("✅ Employees sorted successfully!")
        self.display_all()

    # File Handling
    def save_to_file(self):
        with open("employees.json", "w") as f:
            json.dump([emp.to_dict() for emp in self.employees], f, indent=4)

    def load_from_file(self):
        try:
            with open("employees.json", "r") as f:
                data = json.load(f)
                for emp_data in data:
                    role = emp_data.pop("role", "Employee")
                    if role == "Manager":
                        self.employees.append(Manager(**emp_data))
                    elif role == "Developer":
                        self.employees.append(Developer(**emp_data))
                    else:
                        self.employees.append(Employee(**emp_data))
        except FileNotFoundError:
            pass  # No file on first run

    # Menu-driven system
    def run(self):
        while True:
            print("\n--- Employee Management System ---")
            print("1. Add Employee")
            print("2. Remove Employee")
            print("3. Update Employee")
            print("4. Promote Employee")
            print("5. Search Employee")
            print("6. Display All Employees")
            print("7. Sort Employees")
            print("8. Exit")

            choice = input("Enter choice: ")

            if choice == "1":
                emp_id = input("Enter Employee ID: ")
                name = input("Enter Name: ")
                salary = float(input("Enter Salary: "))
                dept = input("Enter Department (Management/Development/Other): ")
                if dept.lower() == "management":
                    emp = Manager(emp_id, name, salary, dept)
                elif dept.lower() == "development":
                    emp = Developer(emp_id, name, salary, dept)
                else:
                    emp = Employee(emp_id, name, salary, dept)
                self.add_employee(emp)

            elif choice == "2":
                emp_id = input("Enter Employee ID to remove: ")
                self.remove_employee(emp_id)

            elif choice == "3":
                emp_id = input("Enter Employee ID to update: ")
                salary = input("Enter new Salary (leave blank to skip): ")
                department = input("Enter new Department (leave blank to skip): ")
                self.update_employee(emp_id, float(salary) if salary else None, department if department else None)

            elif choice == "4":
                emp_id = input("Enter Employee ID to promote: ")
                increment = float(input("Enter increment amount: "))
                self.promote_employee(emp_id, increment)

            elif choice == "5":
                emp_id = input("Enter Employee ID to search (leave blank if using name): ")
                name = input("Enter Employee Name to search (leave blank if using ID): ")
                self.search_employee(emp_id if emp_id else None, name if name else None)

            elif choice == "6":
                self.display_all()

            elif choice == "7":
                key = input("Sort by (salary/name): ").lower()
                reverse = input("Sort in descending order? (y/n): ").lower() == "y"
                self.sort_employees(key, reverse)

            elif choice == "8":
                print("Exiting system... Goodbye!")
                break

            else:
                print("❌ Invalid choice! Please try again.")


# ------------------------------
# Main Program
# ------------------------------
if __name__ == "__main__":
    system = EmployeeSystem()
    system.run()
