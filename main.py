import tkinter as tk
from tkinter import ttk, messagebox
import csv, os
from datetime import datetime
from collections import defaultdict

FILE = "expenses.csv"
CATEGORIES = ["Food", "Transport", "Entertainment", "Utilities", "Others"]

# Create CSV with headers if not present
if not os.path.exists(FILE):
    with open(FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Amount", "Category", "Description"])

# Save one expense
def save_expense(date, amount, category, description):
    with open(FILE, "a", newline="") as f:
        csv.writer(f).writerow([date, amount, category, description])

# Read all expenses
def read_expenses():
    with open(FILE, "r") as f:
        return list(csv.DictReader(f))

# Analyze data
def analyze():
    data = read_expenses()
    total = 0
    by_category = defaultdict(float)
    this_month = datetime.now().strftime("%Y-%m")

    for row in data:
        if row["Date"].startswith(this_month):
            try:
                amt = float(row["Amount"])
                total += amt
                by_category[row["Category"]] += amt
            except:
                continue
    return total, by_category

# Main app class
class ExpenseApp:
    def __init__(self, root):
        self.root = root
        root.title("Expense Tracker")
        root.geometry("500x500")
        root.configure(bg="#f4f4f4")

        ttk.Label(root, text="Expense Tracker", font=("Helvetica", 20)).pack(pady=15)

        form = ttk.Frame(root)
        form.pack(pady=10)

        ttk.Label(form, text="Amount").grid(row=0, column=0, padx=5, pady=5)
        self.amount = ttk.Entry(form)
        self.amount.grid(row=0, column=1, padx=5)

        ttk.Label(form, text="Category").grid(row=1, column=0, padx=5, pady=5)
        self.category = ttk.Combobox(form, values=CATEGORIES, state="readonly")
        self.category.grid(row=1, column=1, padx=5)
        self.category.set(CATEGORIES[0])

        ttk.Label(form, text="Description").grid(row=2, column=0, padx=5, pady=5)
        self.desc = ttk.Entry(form)
        self.desc.grid(row=2, column=1, padx=5)

        ttk.Button(root, text="Add Expense", command=self.add_expense).pack(pady=10)
        ttk.Button(root, text="Show Summary", command=self.show_summary).pack(pady=5)

    def add_expense(self):
        try:
            amt = float(self.amount.get())
            cat = self.category.get()
            desc = self.desc.get()
            date = datetime.now().strftime("%Y-%m-%d")

            save_expense(date, amt, cat, desc)
            messagebox.showinfo("Success", "Expense recorded!")

            self.amount.delete(0, tk.END)
            self.desc.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Enter a valid amount!")

    def show_summary(self):
        total, by_cat = analyze()
        msg = f"Monthly Total: ₹{total:.2f}\n\n"
        for cat, amt in by_cat.items():
            msg += f"{cat}: ₹{amt:.2f}\n"
        messagebox.showinfo("Summary", msg)

# Start app
if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("TLabel", background="#f4f4f4", font=("Helvetica", 11))
    style.configure("TButton", font=("Helvetica", 10), padding=6)
    app = ExpenseApp(root)
    root.mainloop()
