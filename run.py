import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from tabulate import tabulate

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('expense_tracker_PP3')

expenses = SHEET.worksheet('expenses')

# Define maximum lengths for expense name and category
MAX_EXPENSE_LENGTH = 25
MAX_CATEGORY_LENGTH = 15

def is_valid_number(number_str):
    """
    Check if the input number is valid (two decimal places)
    """
    try:
        number = float(number_str)
        return round(number, 2) == number and '.' in number_str
    except ValueError:
        return False

def is_valid_date(date_str):
    """
    Check if the input date is valid (DD/MM/YYYY format)
    """
    try:
        datetime.strptime(date_str, "%d/%m/%Y")
        return True
    except ValueError:
        return False

def main_menu():
    print("Welcome to your personal Expense Tracker. Please select an option below: \n")
    print("1. Expenses")
    print("2. Budgeting")
    print("3. Exit")
    return input("\nEnter your choice: ")

def expense_menu():
    print("Expenses\n")
    print("1. Add a new expense")
    print("2. View all expenses")
    print("3. View expenses by category")
    print("4. Return to main menu")
    return input("\nEnter your choice: ")

def add_expense():
    """
    Add a new expense
    """
    expense = input(f"\nAdd a name for the expense. For example 'Rent' (up to {MAX_EXPENSE_LENGTH} characters): ")
    while len(expense) == 0:
        print("Invalid expense description. Must be more than 0 characters.\n")
        expense = input(f"Enter the expense (up to {MAX_EXPENSE_LENGTH} characters): ")

    while len(expense) > MAX_EXPENSE_LENGTH:
        expense = input(f"Expense name exceeds maximum length of {MAX_EXPENSE_LENGTH} characters. Please try again: ")
        
    amount = input("\nEnter the expense amount (Has to be to two decimal places): ")
    while not is_valid_number(amount):
        amount = input("Invalid input. Please enter a valid number with exactly two decimal places for amount: ")
    amount = float(amount)
    
    date = input("\nEnter the expense date (DD/MM/YYYY): ")
    while not is_valid_date(date):
        date = input("Invalid date format. Please use DD/MM/YYYY format: ")
    
    category = select_category()
    
    expenses = SHEET.worksheet('expenses')
    expenses.append_row([expense, amount, date, category])
    print("\nExpense added successfully!\n")


def select_category():
    """
    Select the category from list of options
    """
    print("\nSelect a category:")
    predefined_categories = ['Groceries', 'Utilities', 'Transportation', 'Entertainment', 'Healthcare', 'Others']
    for i, category in enumerate(predefined_categories, start=1):
        print(f"{i}. {category}")
    
    while True:
        try:
            choice = int(input("\nEnter the number corresponding to the category: "))
            if 1 <= choice <= len(predefined_categories):
                return predefined_categories[choice - 1]
            else:
                print("Invalid choice. Please enter a number corresponding to the category.")
        except ValueError:
            print("Invalid choice. Please enter a number.")

def view_expenses():
    """
    View all expenses
    """
    expenses_data = SHEET.worksheet('expenses').get_all_records()
    if not expenses_data:
        print("No expenses found.\n")
    else:
        expenses_list = [list(expense.values()) for expense in expenses_data]
        headers = ["Expense", "Amount (£)", "Date", "Category"]
        table = tabulate(expenses_list, headers=headers, tablefmt="grid")
        print("\nList of expenses:")
        print(table)
    input("\nPress Enter to return to the main menu...\n")

def view_expenses_by_category():
    """
    View expenses filtered by category
    """
    category = select_category()
    expenses_data = SHEET.worksheet('expenses').get_all_records()
    category = category.lower()  # Convert the selected category to lowercase
    filtered_expenses = [expense for expense in expenses_data if expense.get('category', '').lower() == category]
    if not filtered_expenses:
        print("No expenses found for this category.")
    else:
        expenses_list = [list(expense.values()) for expense in filtered_expenses]
        headers = ["Expense", "Amount (£)", "Date", "Category"]
        print(tabulate(expenses_list, headers=headers, tablefmt="grid"))
    input("\nPress Enter to return to the main menu...\n")

def budgeting_menu():
    print("Budgeting:\n")
    print("1. View budgets")
    print("2. Set up new budget")
    print("3. Manage budgets")
    print("4. Return to main menu")
    return input("\nEnter your choice: ")

def view_budgets():
    print("Viewing budgets...")

def setup_budget():
    print("Budget set up successfully!")

def manage_budgets():
    print("Managing budgets...")

def main():
    while True:
        choice = main_menu()
        if choice == '1':
            expense_choice = expense_menu()  # Capture the return value
            if expense_choice == '1':
                add_expense()
            elif expense_choice == '2':
                view_expenses()
            elif expense_choice == '3':
                view_expenses_by_category()
            elif expense_choice == '4':
                continue
            else:
                print("\nInvalid choice. Please try again.\n")
        elif choice == '2':
            budgeting_choice = budgeting_menu()  # Capture the return value
            if budgeting_choice == '1':
                view_budgets()
            elif budgeting_choice == '2':
                setup_budget()
            elif budgeting_choice == '3':
                manage_budgets()
            elif budgeting_choice == '4':
                continue
            else:
                print("\nInvalid choice. Please try again.\n")
        elif choice == '3':
            print("\nExiting...")
            break
        else:
            print("\nInvalid choice. Please try again.\n")

if __name__ == "__main__":
    main()