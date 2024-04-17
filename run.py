import gspread
from google.oauth2.service_account import Credentials

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

def main_menu():
    print("Welcome to your personal Expense Tracker")
    print("1. Expenses")
    print("2. Budgeting")
    print("3. Exit")
    return input("Enter your choice: ")

def expense_menu():
    print("Expenses")
    print("1. Add a new expense")
    print("2. View all expenses")
    print("3. View expenses by category")
    print("4. Return to main menu")
    return input("Enter your choice: ")

def add_expense():
    print("Expense set up successfully!")

def view_expenses():
    print("Viewing expenses...")

def view_expenses_by_category():
    print("Viewing expenses...")

def budgeting_menu():
    print("Budgeting feature:")
    print("1. View budgets")
    print("2. Set up new budget")
    print("3. Manage budgets")
    return input("Enter your choice: ")

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
                print("Invalid choice. Please try again.")
        elif choice == '2':
            budgeting_choice = budgeting_menu()  # Capture the return value
            if budgeting_choice == '1':
                view_budgets()
            elif budgeting_choice == '2':
                setup_budget()
            elif budgeting_choice == '3':
                manage_budgets()
            else:
                print("Invalid choice. Please try again.")
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
            
if __name__ == "__main__":
    main()