from setuptools import setup, find_packages

setup(
    name='expense-tracker',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'expense-tracker=expense_tracker.expense_tracker:main',
        ],
    },
    install_requires=[
        # List your dependencies here
    ],
)