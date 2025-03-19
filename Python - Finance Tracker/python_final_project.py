# Import necessary libraries
import json
from datetime import datetime


# Define the FinanceTracker class
class FinanceTracker:
    # Constructor to initialize entries and budgets
    def __init__(self):
        self.entries = []   # List to store financial entries
        self.budgets = {}   # Dictionary to store budget limits for expense categories

    # Method to record a new financial entry
    def record_new_entry(self):
        # Input validation for entry type (income/expense)
        while True:
            entry_type = input("Enter your entry type (income/expense): ").lower()
            if entry_type in ["income", "expense"]:
                break
            else:
                print("Invalid entry type. Please enter 'income' or 'expense'.")

        # Input validation for amount
        amount = validate_float_input("Enter amount: ")

        # Input validation for category
        while True:
            category = input("Enter category: ")
            if category.isalpha():
                break
            else:
                print("Invalid category. Enter string input for your input.")

        # Input validation for date
        date_str = input("Enter date (YYYY-MM-DD): ")
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return

        # Check if the entry is an expense and exceeds the budget limit
        if entry_type == 'expense':
            if category in self.budgets:
                budget_limit = self.budgets[category]
                if amount > budget_limit:
                    print(f"Error: This expense exceeds the monthly budget for {category}.")
                    return

        # Create a dictionary for the entry and add it to the entries list
        entry = {
            'type': entry_type,
            'amount': amount,
            'category': category,
            'date': date.strftime("%Y-%m-%d")
        }
        self.entries.append(entry)
        print("Entry recorded successfully!")

    # Method to view all recorded entries
    def view_all_entries(self):
        if not self.entries:
            print("No entries recorded yet.")
            return

        for index, entry in enumerate(self.entries, start=1):
            print(f"{index}. Type: {entry['type']}, Amount: Rs.{entry['amount']}, "
                  f"Category: {entry['category']}, Date: {entry['date']}")

    # Method to calculate and display total income, total expenses, and net income
    def calculate_totals(self):
        total_income = sum(entry['amount'] for entry in self.entries if entry['type'] == 'income')
        total_expenses = sum(entry['amount'] for entry in self.entries if entry['type'] == 'expense')
        net_income = total_income - total_expenses

        print(f"Total Income: Rs.{total_income}")
        print(f"Total Expenses: Rs.{total_expenses}")
        print(f"Net Income: Rs.{net_income}")

    # Method to view a summary of entries for a specific month and year
    def view_summary_by_month(self):
        month_year_str = input("Enter the month and year (MM-YYYY): ")

        try:
            month, year = map(int, month_year_str.split('-'))
            date_range_start = datetime(year, month, 1)
            date_range_end = datetime(year, month % 12 + 1, 1) if month < 12 else datetime(year + 1, 1, 1)
        except ValueError:
            print("Invalid month and year format. Please enter a valid MM-YYYY.")
            return

        entries_in_month = [entry for entry in self.entries if
                            date_range_start <= datetime.strptime(entry['date'], "%Y-%m-%d") < date_range_end]

        if not entries_in_month:
            print(f"No entries found for {month_year_str}.")
            return

        for entry in entries_in_month:
            print(f"Type: {entry['type']}, Amount: Rs.{entry['amount']}, "
                  f"Category: {entry['category']}, Date: {entry['date']}")

    # Method to save entries and budgets to a file
    def save_to_file(self):
        filename = input("Enter the filename to save: ")
        try:
            with open(filename, 'w') as file:
                json.dump({'entries': self.entries, 'budgets': self.budgets}, file)
            print(f"Data saved to {filename}.")
        except Exception as e:
            print(f"Error: Unable to save data to {filename} : {e}")

    # Method to load entries and budgets from a file
    def load_from_file(self):
        filename = input("Enter the filename to load: ")
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                if 'entries' in data and 'budgets' in data:
                    self.entries = data['entries']
                    self.budgets = data['budgets']
                    print("Previous Entries:")
                    self.view_all_entries()
                    print("\nPrevious Budgets:")
                    self.view_budgets()
                else:
                    print("Invalid file format. Could not load entries and budgets.")
        except FileNotFoundError:
            print(f"The file {filename} not found.")

    # Method to set a budget for a specific expense category
    def set_budget(self):
        while True:
            category = input("Enter category to set budget: ")
            if category.isalpha():
                break
            else:
                print("Invalid category. Enter string input for your input.")
        budget_amount = validate_float_input("Enter monthly budget amount: ")
        self.budgets[category] = budget_amount
        print(f"Budget set successfully for {category}.")

    # Method to view all set budgets
    def view_budgets(self):
        if not self.budgets:
            print("No budgets set yet.")
        else:
            for category, budget_amount in self.budgets.items():
                print(f"Category: {category}, Monthly Budget: Rs.{budget_amount}")

    # Method to find and display the highest expense
    def highest_expense(self):
        if not self.entries:
            print("No entries recorded yet.")
            return

        highest_expense_entry = None
        highest_expense_amount = 0

        for entry in self.entries:
            if entry['type'] == 'expense' and entry['amount'] > highest_expense_amount:
                highest_expense_entry = entry
                highest_expense_amount = entry['amount']

        if highest_expense_entry:
            print(f"Highest Expense: Type: {highest_expense_entry['type']}, "
                  f"Amount: Rs.{highest_expense_entry['amount']}, "
                  f"Category: {highest_expense_entry['category']}, "
                  f"Date: {highest_expense_entry['date']}")
        else:
            print("No expenses found.")

    # Method to calculate and display the average income per month
    def average_income_per_month(self):
        total_income = sum(entry['amount'] for entry in self.entries if entry['type'] == 'income')
        months_with_income = len(set(entry['date'][:7] for entry in self.entries if entry['type'] == 'income'))

        if months_with_income == 0:
            print("No income recorded yet.")
            return

        average_income = total_income / months_with_income
        print(f"Average Income per Month: Rs.{average_income}")


# Function to validate float input
def validate_float_input(amount):
    while True:
        try:
            amount = float(input(amount))
            return amount
        except ValueError:
            print("Invalid input. Please enter a valid amount.")


# Create an instance of the FinanceTracker class
tracker = FinanceTracker()

print("WELCOME TO PYTHON FINANCE TRACKER SYSTEM!")
# Main loop for the finance tracker menu
while True:
    print("\nFinance Tracker Options: ")
    print("1. Record a new entry")
    print("2. View all entries")
    print("3. Calculate totals")
    print("4. View summary by month")
    print("5. Save to file")
    print("6. Load from file")
    print("7. Set Budget")
    print("8. View Budgets")
    print("9. Highest Expense")
    print("10. Average Income per Month")
    print("11. Exit")

    # Get user choice
    choice = input("Enter your choice (1-11): ")

    # Perform actions based on user choice
    if choice == '1':
        tracker.record_new_entry()
    elif choice == '2':
        tracker.view_all_entries()
    elif choice == '3':
        tracker.calculate_totals()
    elif choice == '4':
        tracker.view_summary_by_month()
    elif choice == '5':
        tracker.save_to_file()
    elif choice == '6':
        tracker.load_from_file()
    elif choice == '7':
        tracker.set_budget()
    elif choice == '8':
        tracker.view_budgets()
    elif choice == '9':
        tracker.highest_expense()
    elif choice == '10':
        tracker.average_income_per_month()
    elif choice == '11':
        print("THANK YOU FOR USING THIS SYSTEM!")
        break
    else:
        print("Invalid choice. Please enter a number between 1 and 11.")
