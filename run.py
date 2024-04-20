import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime, timedelta
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

# ANSI escape code colors
PURPLE = "\033[95m"         # Main Title color
LIGHT_BLUE = "\033[94m"     # Welcome paragraph color
RED = "\033[91m"            # Error message color
GREEN = "\033[92m"          # Input color
RESET = "\033[0m"           # Reset to default color

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
        date = datetime.strptime(date_str, "%d/%m/%Y")
        today = datetime.now()
        one_year_ago = today - timedelta(days=365)
        one_year_from_now = today + timedelta(days=365)
        return one_year_ago <= date <= one_year_from_now
    except ValueError:
        return False


def main_menu():
    print(PURPLE + """
 #######
 #        #    #  #####   ######  #    #   ####   ######
 #         #  #   #    #  #       ##   #  #       #
 #####      ##    #    #  #####   # #  #   ####   #####
 #          ##    #####   #       #  # #       #  #
 #         #  #   #       #       #   ##  #    #  #
 #######  #    #  #       ######  #    #   ####   ######
\n
 #######
    #     #####     ##     ####   #    #  ######  #####
    #     #    #   #  #   #    #  #   #   #       #    #
    #     #    #  #    #  #       ####    #####   #    #
    #     #####   ######  #       #  #    #       #####
    #     #   #   #    #  #    #  #   #   #       #   #
    #     #    #  #    #   ####   #    #  ######  #    #
    """ + RESET)
    print(LIGHT_BLUE + "Welcome to your personal Expense Tracker! "
          "Please select an option below:\n" + RESET)
    print("1. Expenses menu")
    print("2. Budgeting menu")
    print("3. Exit application")
    return input(GREEN + "\nEnter your choice:\n" + RESET)


def expense_menu():
    print(PURPLE + "\nExpenses Menu:\n" + RESET)
    print("1. Add a new expense")
    print("2. View all expenses")
    print("3. View expenses by category")
    print("4. Return to main menu")
    return input(GREEN + "\nEnter your choice:\n" + RESET)


def add_expense():
    """
    Add a new expense
    """
    while True:
        expense = input(GREEN + f"\nAdd a name for the expense "
                        f"for example 'Rent' (up to {MAX_EXPENSE_LENGTH}"
                        " characters):\n" + RESET)
        if len(expense) == 0:
            print(RED + "Invalid expense "
                  "description must be more than 0 characters.\n"
                  + RESET)
        elif len(expense) > MAX_EXPENSE_LENGTH:
            print(RED + f"Expense name "
                  f"exceeds maximum length of {MAX_EXPENSE_LENGTH} "
                  "characters Please try again:\n" + RESET)
        else:
            break

    amount = input(GREEN + "\nEnter the expense amount "
                   "(Has to be to two decimal places):" + RESET)
    while not is_valid_number(amount):
        amount = input(RED + "\nInvalid input, the number needs to "
                       "have exactly two decimal places.\n" + RESET)
    amount = float(amount)

    date = input(GREEN + "\nEnter the expense date (DD/MM/YYYY):\n" + RESET)
    while not is_valid_date(date):
        date = input(RED + "\nInvalid date format "
                     "or date is too far in the past/future. "
                     "Please use DD/MM/YYYY format and ensure it's "
                     "within one year from today:\n" + RESET)

    category = select_category()

    expenses = SHEET.worksheet('expenses')
    expenses.append_row([expense, amount, date, category])
    print(GREEN + "\nExpense added successfully!\n" + RESET)

    update_budget(category, amount)


def select_category():
    """
    Select the category from list of options
    """
    print("\nSelect a category:")
    listed_categories = ['Groceries',
                         'Utilities',
                         'Transportation',
                         'Entertainment',
                         'Healthcare',
                         'Others']
    for i, category in enumerate(listed_categories, start=1):
        print(f"{i}. {category}")

    while True:
        try:
            choice = int(input(GREEN + "\nEnter the number corresponding "
                               "to the category:\n" + RESET))
            if 1 <= choice <= len(listed_categories):
                return listed_categories[choice - 1]
            else:
                print(RED + "Invalid choice, "
                      "please enter a number corresponding to the category."
                      + RESET)
        except ValueError:
            print(RED +
                  "Invalid choice, please enter a number between 1 and 6."
                  + RESET)


def view_expenses():
    """
    View all expenses
    """
    expenses_data = SHEET.worksheet('expenses').get_all_records()
    if not expenses_data:
        print("\nNo expenses found.\n")
    else:
        expenses_list = [list(expense.values()) for expense in expenses_data]
        headers = ["Expense", "Amount (£)", "Date", "Category"]
        table = tabulate(expenses_list, headers=headers, tablefmt="grid", floatfmt=".2f")
        print("\nList of expenses:")
        print(table)
    input("\nPress any key to return to the Expenses menu...\n")


def view_expenses_by_category():
    """
    View expenses filtered by category
    """
    category = select_category()
    expenses_data = SHEET.worksheet('expenses').get_all_records()
    category = category.lower()  # Convert the selected category to lowercase
    filtered_expenses = [expense for expense in expenses_data
                         if expense.get('category', '').lower() == category]
    if not filtered_expenses:
        print("No expenses found for this category.")
    else:
        expenses_list = []
        for expense in filtered_expenses:
            expenses_list.append(list(expense.values()))

        headers = ["Expense", "Amount (£)", "Date", "Category"]
        print(tabulate(expenses_list, headers=headers, tablefmt="grid", floatfmt=".2f"))
    input("\nPress any key to return to the Expenses menu...\n")


def budgeting_menu():
    print(PURPLE + "\nBudgeting Menu:\n" + RESET)
    print("1. Set up new budget/ Edit existing budget")
    print("2. View budgets")
    print("3. Return to main menu")
    return input(GREEN + "\nEnter your choice:\n" + RESET)


def view_budgets():
    """
    View all budgets
    """
    budgets_worksheet = SHEET.worksheet('budgets')
    budgets_data = budgets_worksheet.get_all_records()

    if not budgets_data:
        print(RED + "No budgets found.\n" + RESET)
    else:
        budgets_list = [list(budget.values()) for budget in budgets_data]
        headers = ["Category",
                   "Budget\nAmount (£)",
                   "Current\nExpenses (£)",
                   "Remaining\nBudget (£)"]
        print("\nList of budgets:")
        print(tabulate(budgets_list, headers=headers, tablefmt="grid", floatfmt=".2f"))

    input("\nPress any key to return to the Budgets menu...\n")


def update_budget(category, expense_amount):
    """
    Update the budget for the given category
    """
    budgets_worksheet = SHEET.worksheet('budgets')
    budgets_data = budgets_worksheet.get_all_records()
    category = category.lower()
    for budgets in budgets_data:
        if budgets['budget category'].lower() == category:
            total_expenses = budgets['current expenses'] + expense_amount
            remaining_budget = budgets['budget amount'] - total_expenses
            cell_row = budgets_data.index(budgets) + 2
            budgets_worksheet.update_cell(cell_row, 3, total_expenses)
            budgets_worksheet.update_cell(cell_row, 4, remaining_budget)
            break


def update_budget_amount(category, new_budget_amount):
    """
    Update the total expenses for the given category
    and recalculate the remaining budget.
    """
    budgets_worksheet = SHEET.worksheet('budgets')
    budgets_data = budgets_worksheet.get_all_records()
    category = category.lower()
    for budget_row in budgets_data:
        if budget_row['budget category'].lower() == category:
            expenses_data = SHEET.worksheet('expenses').get_all_records()
            total_expenses = 0
            for expense in expenses_data:
                if expense.get('category', '').lower() == category.lower():
                    total_expenses += expense['amount']

            cell_row = budgets_data.index(budget_row) + 2
            budgets_worksheet.update_cell(cell_row, 2, new_budget_amount)
            budgets_worksheet.update_cell(cell_row, 3, total_expenses)
            remaining_budget = new_budget_amount - total_expenses
            budgets_worksheet.update_cell(cell_row, 4, remaining_budget)
            print(GREEN + "Budget amount updated successfully!" + RESET)
            break


def setup_budget():
    """
    Add new budget for the given category and check if a budget
    already exists for the specified category
    """
    print(GREEN +
          "Select the category for the budget you would like to add/ update:"
          + RESET)
    category = select_category()
    budgets_worksheet = SHEET.worksheet('budgets')
    budgets_data = budgets_worksheet.get_all_records()
    for budget_row in budgets_data:
        if budget_row['budget category'].lower() == category.lower():
            print(RED +
                  f"\nA budget already exists for the category '{category}'."
                  + RESET)
            update_option = input(GREEN +
                                  "\nDo you want to update the existing "
                                  "budget? (yes/no):\n" + RESET).lower()
            if update_option == 'yes':
                new_budget_amount = input(GREEN +
                                          "\nEnter the new budget amount: £"
                                          + RESET)
                while not is_valid_number(new_budget_amount):
                    new_budget_amount = input(RED +
                                              "\nInvalid input, "
                                              "the number needs to "
                                              "have exactly two "
                                              "decimal places.\n"
                                              + RESET)
                new_budget_amount = float(new_budget_amount)
                update_budget_amount(category, new_budget_amount)
                return
            else:
                print("Returning to the main menu...")
                return

    # If no existing budget found, proceed to set up a new budget
    budget_amount = input(GREEN +
                          f"\nEnter the budget amount for '{category}'"
                          "(Has to be to two decimal places): £\n"
                          + RESET)
    while not is_valid_number(budget_amount):
        budget_amount = input(
            RED + "\nInvalid input, "
            "please enter a valid number with exactly two decimal places:\n"
            + RESET)
    budget_amount = float(budget_amount)

    total_expenses = calculate_total_expenses(category)
    remaining_budget = budget_amount - total_expenses

    budgets_worksheet.append_row(
        [category, budget_amount, total_expenses, remaining_budget]
        )
    print(GREEN + "\nBudget set up successfully!" + RESET)


def calculate_total_expenses(category):
    """
    Calculate total expenses for the given category.
    """
    expenses_data = SHEET.worksheet('expenses').get_all_records()
    total_expenses = 0
    category = category.lower()
    for expense in expenses_data:
        if expense.get('category', '').lower() == category:
            total_expenses += expense.get('amount', 0)
            total_expenses = round(total_expenses, 2)
    return total_expenses


def main():
    while True:
        choice = main_menu()
        if choice == '1':
            while True:
                expense_choice = expense_menu()  # Capture the return value
                if expense_choice == '1':
                    add_expense()
                elif expense_choice == '2':
                    view_expenses()
                elif expense_choice == '3':
                    view_expenses_by_category()
                elif expense_choice == '4':
                    break  # Break out of the inner loop to return to main menu
                else:
                    print(RED +
                          "\nInvalid choice, please choose a "
                          "number between 1 and 4.\n"
                          + RESET)
        elif choice == '2':
            while True:
                budgeting_choice = budgeting_menu()  # Capture the return value
                if budgeting_choice == '1':
                    setup_budget()
                elif budgeting_choice == '2':
                    view_budgets()
                elif budgeting_choice == '3':
                    break  # Break out of the inner loop to return to main menu
                else:
                    print(RED +
                          "\nInvalid choice, please choose a "
                          "number between 1 and 3.\n"
                          + RESET)
        elif choice == '3':
            print("\nExiting Expense Tracker...")
            break
        else:
            print(RED +
                  "\nInvalid choice, please choose a "
                  "number between 1 and 3.\n"
                  + RESET)


if __name__ == "__main__":
    main()
