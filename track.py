import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime


class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("💰 Expense Tracker")
        self.root.geometry("750x650")
        self.root.resizable(False, False)
        self.root.configure(bg='#1a1a2e')

        self.data_file = "expenses.json"
        self.expenses = []
        self.load_data()

        self.setup_ui()
        self.update_list()
        self.update_stats()

    def load_data(self):
        """Ma'lumotlarni yuklash"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    self.expenses = json.load(f)
            except:
                self.expenses = []

    def save_data(self):
        """Ma'lumotlarni saqlash"""
        with open(self.data_file, 'w') as f:
            json.dump(self.expenses, f, indent=2, ensure_ascii=False)

    def setup_ui(self):
        # Sarlavha
        title = tk.Label(
            self.root,
            text="💰 PERSONAL EXPENSE TRACKER",
            font=("Arial", 22, "bold"),
            bg='#1a1a2e',
            fg='#f2c14e'
        )
        title.pack(pady=10)

        # Kiritish paneli
        input_frame = tk.LabelFrame(
            self.root,
            text="➕ YANGI XARAJAT",
            font=("Arial", 12, "bold"),
            bg='#1a1a2e',
            fg='#f2c14e'
        )
        input_frame.pack(pady=10, padx=20, fill='x')

        # 1-qator: Summa va Kategoriya
        row1 = tk.Frame(input_frame, bg='#1a1a2e')
        row1.pack(fill='x', pady=5)

        tk.Label(
            row1,
            text="💵 Summa:",
            font=("Arial", 11),
            bg='#1a1a2e',
            fg='#aaa'
        ).pack(side='left', padx=(10, 5))

        self.amount_entry = tk.Entry(
            row1,
            font=("Arial", 12),
            width=15,
            bg='#2a2a4e',
            fg='white',
            relief='flat',
            insertbackground='white'
        )
        self.amount_entry.pack(side='left', padx=(0, 20))
        self.amount_entry.bind('<Return>', lambda e: self.add_expense())
        self.amount_entry.focus()

        tk.Label(
            row1,
            text="📂 Kategoriya:",
            font=("Arial", 11),
            bg='#1a1a2e',
            fg='#aaa'
        ).pack(side='left', padx=(0, 5))

        self.category_var = tk.StringVar(value="Ovqat")
        categories = ["Ovqat", "Transport", "Kiyim", "Uy-joy", "Sog'liq",
                      "O'qish", "Ko'ngilochar", "Internet", "Kommunal", "Boshqa"]
        self.category_combo = ttk.Combobox(
            row1,
            textvariable=self.category_var,
            values=categories,
            font=("Arial", 11),
            state='readonly',
            width=12
        )
        self.category_combo.pack(side='left', padx=(0, 10))

        # 2-qator: Tavsif
        row2 = tk.Frame(input_frame, bg='#1a1a2e')
        row2.pack(fill='x', pady=5)

        tk.Label(
            row2,
            text="📝 Tavsif:",
            font=("Arial", 11),
            bg='#1a1a2e',
            fg='#aaa'
        ).pack(side='left', padx=(10, 5))

        self.desc_entry = tk.Entry(
            row2,
            font=("Arial", 12),
            width=40,
            bg='#2a2a4e',
            fg='white',
            relief='flat',
            insertbackground='white'
        )
        self.desc_entry.pack(side='left', padx=(0, 10), fill='x', expand=True)
        self.desc_entry.bind('<Return>', lambda e: self.add_expense())

        # 3-qator: Tugma
        self.add_btn = tk.Button(
            input_frame,
            text="➕ XARAJAT QO'SHISH",
            font=("Arial", 12, "bold"),
            bg='#2ed573',
            fg='white',
            padx=30,
            pady=8,
            relief='flat',
            cursor='hand2',
            command=self.add_expense
        )
        self.add_btn.pack(pady=10)

        # Statistika paneli
        stats_frame = tk.LabelFrame(
            self.root,
            text="📊 STATISTIKA",
            font=("Arial", 12, "bold"),
            bg='#1a1a2e',
            fg='#f2c14e'
        )
        stats_frame.pack(pady=10, padx=20, fill='x')

        self.stats_label = tk.Label(
            stats_frame,
            text="",
            font=("Arial", 11),
            bg='#1a1a2e',
            fg='white',
            justify='left'
        )
        self.stats_label.pack(padx=15, pady=10, anchor='w')

        # Ro'yxat paneli
        list_frame = tk.LabelFrame(
            self.root,
            text="📋 XARAJATLAR RO'YXATI",
            font=("Arial", 12, "bold"),
            bg='#1a1a2e',
            fg='#f2c14e'
        )
        list_frame.pack(pady=10, padx=20, fill='both', expand=True)

        # Scrollbar
        scrollbar = tk.Scrollbar(list_frame, bg='#1a1a2e')
        scrollbar.pack(side='right', fill='y')

        self.listbox = tk.Listbox(
            list_frame,
            font=("Consolas", 10),
            bg='#2a2a4e',
            fg='white',
            selectmode='single',
            yscrollcommand=scrollbar.set,
            relief='flat',
            height=10
        )
        self.listbox.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        self.listbox.bind('<Double-Button-1>', self.delete_expense)
        scrollbar.config(command=self.listbox.yview)

        # Holat
        self.status_label = tk.Label(
            self.root,
            text="💡 Xarajat qo'shing va kunlik xarajatlaringizni kuzating",
            font=("Arial", 10),
            bg='#1a1a2e',
            fg='#888'
        )
        self.status_label.pack(pady=5)

    def add_expense(self):
        """Xarajat qo'shish"""
        try:
            amount = float(self.amount_entry.get().replace(',', '.'))
            if amount <= 0:
                messagebox.showwarning("⚠️", "Summa musbat bo'lishi kerak!")
                return
        except ValueError:
            messagebox.showerror("❌", "Noto'g'ri summa! Iltimos, son kiriting.")
            return

        category = self.category_var.get()
        description = self.desc_entry.get().strip() or "Tavsif yo'q"

        expense = {
            'amount': amount,
            'category': category,
            'description': description,
            'date': datetime.now().strftime('%d.%m.%Y %H:%M')
        }

        self.expenses.append(expense)
        self.save_data()

        self.amount_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.amount_entry.focus()

        self.update_list()
        self.update_stats()
        self.status_label.config(text=f"✅ Xarajat qo'shildi: {amount:.2f} so'm")

    def delete_expense(self, event):
        """Xarajatni o'chirish"""
        index = self.listbox.curselection()
        if not index:
            return

        if messagebox.askyesno("⚠️", "Bu xarajatni o'chirmoqchimisiz?"):
            del self.expenses[index[0]]
            self.save_data()
            self.update_list()
            self.update_stats()
            self.status_label.config(text="🗑️ Xarajat o'chirildi")

    def update_list(self):
        """Ro'yxatni yangilash"""
        self.listbox.delete(0, tk.END)

        # Eng oxirgi qo'shilgan birinchi bo'lib ko'rinishi uchun
        for exp in reversed(self.expenses):
            text = f"{exp['date']} | {exp['category']:12} | {exp['amount']:10.2f} | {exp['description']}"
            self.listbox.insert(tk.END, text)

    def update_stats(self):
        """Statistikani yangilash"""
        if not self.expenses:
            self.stats_label.config(text="📊 Hali xarajatlar yo'q")
            return

        total = sum(e['amount'] for e in self.expenses)
        count = len(self.expenses)
        avg = total / count if count > 0 else 0

        # Kategoriya bo'yicha
        categories = {}
        for e in self.expenses:
            cat = e['category']
            categories[cat] = categories.get(cat, 0) + e['amount']

        # Eng ko'p xarajat
        max_cat = max(categories.items(), key=lambda x: x[1]) if categories else ('', 0)

        stats = f"💰 Jami xarajat: {total:,.2f} so'm\n"
        stats += f"📊 Xarajatlar soni: {count} ta\n"
        stats += f"📈 O'rtacha: {avg:,.2f} so'm\n"
        stats += f"🏷️ Eng ko'p: {max_cat[0]} ({max_cat[1]:,.2f} so'm)\n"
        stats += "━" * 35 + "\n"

        # Kategoriyalar
        for cat, amount in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            percent = (amount / total) * 100 if total > 0 else 0
            stats += f"  • {cat}: {amount:,.2f} ({percent:.1f}%)\n"

        self.stats_label.config(text=stats)


def main():
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()


if __name__ == "__main__":
    main()