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

def budgeting_menu():
    print("Budgeting feature:")
    print("1. View budgets")
    print("2. Set up new budget")
    print("3. Manage budgets")
    choice = input("Enter your choice: ")