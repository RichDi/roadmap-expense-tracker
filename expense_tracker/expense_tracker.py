import argparse
from .expense_models import ExpenseTracker

def main():

    parser = argparse.ArgumentParser(description='Expense Tracker')
    subparsers = parser.add_subparsers(dest='command', help='Sub-command help')

    # Add command
    parser_add = subparsers.add_parser('add', help='Add a new expense')
    parser_add.add_argument('--description', type=str, required=True, help='Description of the expense')
    parser_add.add_argument('--amount', type=float, required=True, help='Amount of the expense')
    parser_add.add_argument('--category', type=str, required=True, help='Category of the expense')

    # Update command
    parser_update = subparsers.add_parser('update', help='Update an existing expense')
    parser_update.add_argument('--id', type=int, required=True, help='ID of the expense to update')
    parser_update.add_argument('--description', type=str, help='New description of the expense')
    parser_update.add_argument('--amount', type=float, help='New amount of the expense')

    # Delete command
    parser_delete = subparsers.add_parser('delete', help='Delete an expense')
    parser_delete.add_argument('--id', type=int, required=True, help='ID of the expense to delete')

    # List command
    parser_list = subparsers.add_parser('list', help='List all expenses')
    parser_list.add_argument('--month', type=int, help='Month to filter the expenses')
    parser_list.add_argument('--category', type=str, help='Category to filter the expenses')

    # Summary command
    parser_summary = subparsers.add_parser('summary', help='Show summary of expenses')
    parser_summary.add_argument('--month', type=int, help='Month to show the summary for')
    parser_summary.add_argument('--category', type=str, help='Category to show the summary for')

    # Budget command
    parser_budget = subparsers.add_parser('budget', help='Set a budget')
    parser_budget.add_argument('--amount', type=float, required=True, help='Budget amount')
    
    # Export command
    parser_export = subparsers.add_parser('export', help='Export expenses to CSV')

    args = parser.parse_args()

    expense_list = ExpenseTracker('expenses.json')

    if args.command == 'add':
        expense_list.add_command(args.description, args.amount, args.category)
    elif args.command == 'update':
        expense_list.update_command(args.id, args.description, args.amount, args.category)
    elif args.command == 'delete':
        expense_list.delete_command(args.id)
    elif args.command == 'list':
        expense_list.list_command(args.month, args.category)
    elif args.command == 'summary':
        expense_list.summary_command(args.month)
    elif args.command == 'budget':
        expense_list.budget_command(args.amount)
    elif args.command == 'export':
        expense_list.export_command()

if __name__ == '__main__':
    main()
