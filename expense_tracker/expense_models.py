import json
import datetime
from tabulate import tabulate

class Expense():
    """ Class to represent an expense """
    def get_current_date(self):
        """ Get the current date in the format YYYY-MM-DD """
        return datetime.datetime.now().strftime('%Y-%m-%d')

    def __init__(self, id, description, amount, category):
        self.id = id
        self.description = description
        self.amount = amount
        self.date = self.get_current_date()
        self.category = category

class ExpenseTracker():
    """ Class to represent a list of expenses with its budget """
    def __init__(self, file_name='expenses.json'):
        self.file_name = file_name
        self.expenses = []
        self.budget = 0
        self.load_data()

    def save_data(self):
        """ Save the expenses and budget to a JSON file """
        with open(self.file_name, 'w') as f:
            json.dump({
                'expenses': [expense.__dict__ for expense in self.expenses],
                'budget': self.budget
            }, f)

    def load_data(self):
        """ Load the expenses and budget from a JSON file """
        try:
            with open(self.file_name) as f:
                data = json.load(f)
                self.expenses = [Expense(
                    expense['id'],
                    expense['description'],
                    expense['amount'],
                    expense['category'],
                ) for expense in data['expenses']]
                self.budget = data['budget']
        except FileNotFoundError:
            return

    def get_last_id(self):
        """ Get the last ID of the expenses """
        if len(self.expenses) == 0:
            return 1
        return self.expenses[-1].id + 1


    def add_expense(self, description, amount, category):
        """ Add a new expense to the list """
        new_expense = Expense(self.get_last_id(), description, amount, category)
        self.expenses.append(new_expense)
        self.save_data()
        return new_expense

    def add_command(self, description, amount, category):
        """ Call add expense and print the result """
        new_expense = self.add_expense(description, amount, category)
        print(f'Expense added successfully (ID: {new_expense.id})')
        if self.budget != 0:
            if self.is_over_budget():
                print(f'You are ${abs(self.get_remaining())} over budget!')
            elif self.get_remaining() < 100:
                print(f'You have ${self.get_remaining()} remaining in your budget')
            elif self.get_remaining() == 0:
                print('You have no budget remaining')

    def update_expense(self, id, description, amount, category):
        """ Update an existing expense """
        for expense in self.expenses:
            if expense.id == id:
                if description is not None:
                    expense.description = description
                if amount is not None:
                    expense.amount = amount
                if category is not None:
                    expense.category = category
                self.save_data()
                return expense
        return None

    def update_command(self, id, description, amount, category):
        """ Call update expense and print the result """
        new_expense = self.update_expense(id, description, amount, category)
        if new_expense is not None:
            print(f'Expense updated successfully (ID: {id})')
        else:
            print(f'Expense not found (ID: {id})')

    def delete_expense(self, id):
        """ Delete an expense """
        for expense in self.expenses:
            if expense.id == id:
                self.expenses.remove(expense)
                self.save_data()
                return expense
        return None

    def delete_command(self, id):
        """ Call delete expense and print the result """
        deleted_expense = self.delete_expense(id)
        if deleted_expense is not None:
            print(f'Expense deleted successfully (ID: {id})')
        else:
            print(f'Expense not found (ID: {id})')

    def get_expenses(self, month=None, category=None):
        """ Get a list of expenses """
        expenses_list = []
        for expense in self.expenses:
            if (month is None or int(expense.date.split('-')[1]) == month) and \
                (category is None or expense.category == category):
                expenses_list.append(expense)

        return expenses_list

    def list_command(self, month=None, category=None):
        """ Call list expenses and print the result """
        headers = ['ID', 'Date', 'Description', 'Amount', 'Category']
        expenses = self.get_expenses(month, category)
        tabulated_expenses = [[
            expense.id,
            expense.date,
            expense.description,
            f'${expense.amount:,.2f}',
            expense.category
        ] for expense in expenses]
        print(tabulate(tabulated_expenses, headers))

    def get_summary(self, month=None, category=None):
        """ Get the total amount of expenses """
        expenses = self.get_expenses(month, category)
        total = 0
        for expense in expenses:
            total += expense.amount
        return total

    def summary_command(self, month=None, category=None):
        """ Call summary expenses """
        total = self.get_summary(month, category)
        print(f'Total expenses: ${total}')
        
    def set_budget(self, budget):
        """ Set the budget """
        self.budget = budget
        self.save_data()
        
    def budget_command(self, budget):
        """ Call set budget and print the result """
        self.set_budget(budget)
        print(f'Monthly Budget set to ${budget}')
        
    def export_command(self):
        """ Export the expenses to a CSV file """
        with open('expenses.csv', 'w') as f:
            f.write('ID,Date,Description,Amount,Category\n')
            for expense in self.expenses:
                f.write(f'{expense.id},{expense.date},{expense.description},{expense.amount},{expense.category}\n')
        print('Expenses exported to expenses.csv')

    def get_current_month(self):
        """ Get the current month """
        return int(datetime.datetime.now().strftime('%m'))

    def get_remaining(self):
        """ Get the remaining budget """
        return self.budget - self.get_summary(self.get_current_month())

    def is_over_budget(self):
        """ Check if the expenses are over budget """
        return self.get_summary(self.get_current_month()) > self.budget
