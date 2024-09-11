import unittest
import os
from faker import Faker
from expense_models import ExpenseTracker

class TestExpenseList(unittest.TestCase):
    
    def createRandomExpense(self):
        return {
            'description': self.fake.word(),
            'amount': self.fake.random_int(),
            'category': self.fake.word()
        }
        
    def addRandomExpense(self):
        new_expense = self.createRandomExpense()
        self.total += new_expense['amount']
        self.expense_list.add_expense(new_expense['description'], new_expense['amount'], new_expense['category'])
        return new_expense
    
    def setUp(self):
        self.fake = Faker()
        self.expense_list = ExpenseTracker(file_name='test_expenses.json')
        self.total = 0
        
    def test_add_expense(self):
        expense_1 = self.addRandomExpense()
        
        # Check if the expense was added correctly
        self.assertEqual(self.expense_list.expenses[-1].id, 1)
        self.assertEqual(self.expense_list.expenses[-1].amount, expense_1['amount'])
        self.assertEqual(self.expense_list.expenses[-1].description, expense_1['description'])
        self.assertEqual(self.expense_list.expenses[-1].category, expense_1['category'])
        
    def test_update_expense(self):
        self.addRandomExpense()
        self.expense_list.update_expense(1, 'Gasto 2', 200, 'Comida')
        
        # Check if the expense was updated correctly
        self.assertEqual(self.expense_list.expenses[-1].description, 'Gasto 2')
        self.assertEqual(self.expense_list.expenses[-1].amount, 200)
        self.assertEqual(self.expense_list.expenses[-1].category, 'Comida')

    def test_delete_expense(self):
        self.addRandomExpense()
        self.addRandomExpense()
        self.expense_list.delete_expense(1)
        # Check if only one expense was deleted
        self.assertEqual(len(self.expense_list.expenses), 1)
        # Check if the correct expense was deleted
        self.assertEqual(self.expense_list.expenses[0].id, 2)

    def test_list_expenses(self):
        self.addRandomExpense()
        self.addRandomExpense()
        responses = self.expense_list.get_expenses()
        self.assertEqual(len(responses), 2)
        
    def test_summary_expenses(self):
        self.addRandomExpense()
        self.addRandomExpense()
        summary = self.expense_list.get_summary()
        self.assertEqual(summary, self.total)
    
    def tearDown(self):
        print('Tearing down...')
        self.expense_list.list_command()
        os.remove('test_expenses.json')
    

if __name__ == '__main__':
    unittest.main()