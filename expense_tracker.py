import csv
import os
from datetime import datetime

# Constants
EXPENSES_FILE = "expenses.csv"
CATEGORIES = ["Food", "Transport", "Housing", "Entertainment", "Utilities", "Other"]

# Create CSV file with headers if not exists
def initialize_file():
    if not os.path.exists(EXPENSES_FILE):
        with open(EXPENSES_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["Date", "Amount", "Category", "Description"])
            writer.writeheader()

# Add new expense
def add_expense():
    print("\n➕ Add New Expense")
    date = input(f"Date (YYYY-MM-DD) [Default: {datetime.today().strftime('%Y-%m-%d')}]): ") or datetime.today().strftime("%Y-%m-%d")
    
    while True:
        try:
            amount = float(input("Amount (₹): "))
            break
        except ValueError:
            print("❗ Please enter a valid number")

    print("\n".join([f"{i+1}. {cat}" for i, cat in enumerate(CATEGORIES)]))
    while True:
        try:
            cat_choice = int(input("Choose category (1-6): "))
            category = CATEGORIES[cat_choice-1]
            break
        except (ValueError, IndexError):
            print("❗ Please enter a valid category number")

    description = input("Description (optional): ").strip()

    with open(EXPENSES_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["Date", "Amount", "Category", "Description"])
        writer.writerow({
            "Date": date,
            "Amount": amount,
            "Category": category,
            "Description": description
        })
    print("✅ Expense added successfully!")

# View all expenses
def view_expenses():
    print("\n📋 All Expenses")
    try:
        with open(EXPENSES_FILE, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            expenses = list(reader)
            
        if not expenses:
            print("No expenses recorded yet!")
            return
            
        total = 0
        for i, expense in enumerate(expenses, 1):
            print(f"{i}. {expense['Date']} | ₹{expense['Amount']} | {expense['Category']} | {expense['Description']}")
            total += float(expense['Amount'])
            
        print(f"\n💵 Total Expenditure: ₹{total:.2f}")
        
    except FileNotFoundError:
        print("No expenses recorded yet!")

# View expenses by category
def view_by_category():
    print("\n🔍 View by Category")
    print("\n".join([f"{i+1}. {cat}" for i, cat in enumerate(CATEGORIES)]))
    
    while True:
        try:
            choice = int(input("Choose category (1-6): "))
            category = CATEGORIES[choice-1]
            break
        except (ValueError, IndexError):
            print("❗ Please enter a valid category number")
    
    with open(EXPENSES_FILE, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        expenses = [row for row in reader if row["Category"] == category]
        
    if not expenses:
        print(f"No expenses found in {category} category")
        return
        
    total = 0
    for i, expense in enumerate(expenses, 1):
        print(f"{i}. {expense['Date']} | ₹{expense['Amount']} | {expense['Description']}")
        total += float(expense['Amount'])
    
    print(f"\n💵 Total in {category}: ₹{total:.2f}")

# Generate summary report
def generate_summary():
    print("\n📊 Spending Summary")
    try:
        with open(EXPENSES_FILE, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            expenses = list(reader)
            
        if not expenses:
            print("No expenses to summarize!")
            return
            
        summary = {}
        for expense in expenses:
            category = expense["Category"]
            amount = float(expense["Amount"])
            summary[category] = summary.get(category, 0) + amount
            
        print("💰 Category-wise Expenditure:")
        for category, total in summary.items():
            print(f"  {category}: ₹{total:.2f}")
            
        print(f"\n💸 Grand Total: ₹{sum(summary.values()):.2f}")
        
    except FileNotFoundError:
        print("No expenses recorded yet!")

# Main menu
def main():
    initialize_file()
    
    while True:
        print("\n💼 Expense Tracker")
        print("1. Add New Expense")
        print("2. View All Expenses")
        print("3. View Expenses by Category")
        print("4. Generate Summary")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ")
        
        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            view_by_category()
        elif choice == "4":
            generate_summary()
        elif choice == "5":
            print("\n👋 Goodbye! Keep tracking your expenses!")
            break
        else:
            print("❗ Invalid choice! Please enter 1-5")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Goodbye! Keep tracking your expenses!")
