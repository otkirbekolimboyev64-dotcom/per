import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import PyPDF2
import os
import threading


class PDFMerger:
    def __init__(self, root):
        self.root = root
        self.root.title("📄 PDF Merger")
        self.root.geometry("650x550")
        self.root.resizable(False, False)
        self.root.configure(bg='#1a1a2e')

        self.pdf_files = []
        self.setup_ui()

    def setup_ui(self):
        # Sarlavha
        title = tk.Label(
            self.root,
            text="📄 PDF MERGER",
            font=("Arial", 24, "bold"),
            bg='#1a1a2e',
            fg='#f2c14e'
        )
        title.pack(pady=15)

        subtitle = tk.Label(
            self.root,
            text="Bir nechta PDF fayllarni birlashtirish",
            font=("Arial", 11),
            bg='#1a1a2e',
            fg='#888'
        )
        subtitle.pack(pady=(0, 15))

        # Tugmalar paneli
        btn_frame = tk.Frame(self.root, bg='#1a1a2e')
        btn_frame.pack(pady=10, padx=20, fill='x')

        self.add_btn = tk.Button(
            btn_frame,
            text="📂 PDF QO'SHISH",
            font=("Arial", 11, "bold"),
            bg='#2ed573',
            fg='white',
            padx=20,
            pady=8,
            relief='flat',
            cursor='hand2',
            command=self.add_pdfs
        )
        self.add_btn.pack(side='left', padx=5)

        self.remove_btn = tk.Button(
            btn_frame,
            text="🗑️ O'CHIRISH",
            font=("Arial", 11, "bold"),
            bg='#ff6b6b',
            fg='white',
            padx=20,
            pady=8,
            relief='flat',
            cursor='hand2',
            state='disabled',
            command=self.remove_selected
        )
        self.remove_btn.pack(side='left', padx=5)

        self.clear_btn = tk.Button(
            btn_frame,
            text="🔄 TOZALASH",
            font=("Arial", 11, "bold"),
            bg='#333',
            fg='white',
            padx=20,
            pady=8,
            relief='flat',
            cursor='hand2',
            command=self.clear_all
        )
        self.clear_btn.pack(side='left', padx=5)

        self.move_up_btn = tk.Button(
            btn_frame,
            text="⬆️ TEPAGA",
            font=("Arial", 11, "bold"),
            bg='#4a6fa5',
            fg='white',
            padx=15,
            pady=8,
            relief='flat',
            cursor='hand2',
            state='disabled',
            command=self.move_up
        )
        self.move_up_btn.pack(side='left', padx=5)

        self.move_down_btn = tk.Button(
            btn_frame,
            text="⬇️ PASTGA",
            font=("Arial", 11, "bold"),
            bg='#4a6fa5',
            fg='white',
            padx=15,
            pady=8,
            relief='flat',
            cursor='hand2',
            state='disabled',
            command=self.move_down
        )
        self.move_down_btn.pack(side='left', padx=5)

        # Ro'yxat
        list_frame = tk.LabelFrame(
            self.root,
            text="📋 PDF FAYLLAR RO'YXATI",
            font=("Arial", 12, "bold"),
            bg='#1a1a2e',
            fg='#f2c14e'
        )
        list_frame.pack(pady=10, padx=20, fill='both', expand=True)

        scrollbar = tk.Scrollbar(list_frame, bg='#1a1a2e')
        scrollbar.pack(side='right', fill='y')

        self.listbox = tk.Listbox(
            list_frame,
            font=("Consolas", 11),
            bg='#2a2a4e',
            fg='white',
            selectmode='single',
            yscrollcommand=scrollbar.set,
            relief='flat',
            height=10
        )
        self.listbox.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        self.listbox.bind('<<ListboxSelect>>', self.on_select)
        scrollbar.config(command=self.listbox.yview)

        # Fayl soni
        self.count_label = tk.Label(
            self.root,
            text="📄 0 ta PDF fayl",
            font=("Arial", 11),
            bg='#1a1a2e',
            fg='#888'
        )
        self.count_label.pack(pady=(5, 0))

        # Merge tugmasi
        self.merge_btn = tk.Button(
            self.root,
            text="🔗 PDF LARNI BIRLASHTIRISH",
            font=("Arial", 14, "bold"),
            bg='#f2c14e',
            fg='#1a1a2e',
            padx=30,
            pady=12,
            relief='flat',
            cursor='hand2',
            state='disabled',
            command=self.merge_pdfs
        )
        self.merge_btn.pack(pady=15)

        # Progress
        self.progress = ttk.Progressbar(
            self.root,
            length=500,
            mode='determinate'
        )
        self.progress.pack(pady=5)

        # Holat
        self.status_label = tk.Label(
            self.root,
            text="💡 PDF fayllarni qo'shing va tartibini o'zgartiring",
            font=("Arial", 10),
            bg='#1a1a2e',
            fg='#888'
        )
        self.status_label.pack(pady=5)

    def add_pdfs(self):
        """PDF fayllarni qo'shish"""
        files = filedialog.askopenfilenames(
            title="PDF fayllarni tanlang",
            filetypes=[("PDF fayllar", "*.pdf"), ("Barcha fayllar", "*.*")]
        )

        added = 0
        for file in files:
            if file not in self.pdf_files:
                self.pdf_files.append(file)
                self.listbox.insert(tk.END, os.path.basename(file))
                added += 1

        if added > 0:
            self.update_buttons()
            self.update_count()
            self.status_label.config(text=f"✅ {added} ta PDF fayl qo'shildi")
        else:
            self.status_label.config(text="ℹ️ Yangi PDF fayllar tanlanmadi")

    def remove_selected(self):
        """Tanlangan PDF ni o'chirish"""
        index = self.listbox.curselection()
        if not index:
            return

        filename = os.path.basename(self.pdf_files[index[0]])
        if messagebox.askyesno("⚠️", f"'{filename}' ni o'chirmoqchimisiz?"):
            del self.pdf_files[index[0]]
            self.listbox.delete(index[0])
            self.update_buttons()
            self.update_count()
            self.status_label.config(text=f"🗑️ '{filename}' o'chirildi")

    def clear_all(self):
        """Barcha PDF larni tozalash"""
        if not self.pdf_files:
            return

        if messagebox.askyesno("⚠️", "Barcha PDF fayllarni tozalamoqchimisiz?"):
            self.pdf_files = []
            self.listbox.delete(0, tk.END)
            self.update_buttons()
            self.update_count()
            self.status_label.config(text="🔄 Barcha PDF fayllar tozalandi")

    def move_up(self):
        """Tanlangan faylni tepaga ko'chirish"""
        index = self.listbox.curselection()
        if not index or index[0] == 0:
            return

        i = index[0]
        self.pdf_files[i], self.pdf_files[i - 1] = self.pdf_files[i - 1], self.pdf_files[i]

        # Ro'yxatni yangilash
        self.listbox.delete(i)
        self.listbox.insert(i - 1, os.path.basename(self.pdf_files[i - 1]))
        self.listbox.selection_set(i - 1)
        self.update_buttons()
        self.status_label.config(text="⬆️ Fayl tepaga ko'chirildi")

    def move_down(self):
        """Tanlangan faylni pastga ko'chirish"""
        index = self.listbox.curselection()
        if not index or index[0] == len(self.pdf_files) - 1:
            return

        i = index[0]
        self.pdf_files[i], self.pdf_files[i + 1] = self.pdf_files[i + 1], self.pdf_files[i]

        # Ro'yxatni yangilash
        self.listbox.delete(i)
        self.listbox.insert(i + 1, os.path.basename(self.pdf_files[i + 1]))
        self.listbox.selection_set(i + 1)
        self.update_buttons()
        self.status_label.config(text="⬇️ Fayl pastga ko'chirildi")

    def on_select(self, event):
        """Ro'yxatdan tanlanganda"""
        self.update_buttons()

    def update_buttons(self):
        """Tugmalarni yangilash"""
        selected = len(self.listbox.curselection()) > 0
        count = len(self.pdf_files)

        self.remove_btn.config(state='normal' if selected else 'disabled')
        self.move_up_btn.config(state='normal' if selected and self.listbox.curselection()[0] > 0 else 'disabled')
        self.move_down_btn.config(
            state='normal' if selected and self.listbox.curselection()[0] < count - 1 else 'disabled')
        self.merge_btn.config(state='normal' if count >= 2 else 'disabled')

    def update_count(self):
        """Fayl sonini yangilash"""
        count = len(self.pdf_files)
        self.count_label.config(text=f"📄 {count} ta PDF fayl")
        self.merge_btn.config(
            text=f"🔗 {count} TA PDF NI BIRLASHTIRISH" if count >= 2 else "🔗 PDF LARNI BIRLASHTIRISH (2+ KERAK)"
        )

    def merge_pdfs(self):
        """PDF larni birlashtirish"""
        if len(self.pdf_files) < 2:
            messagebox.showwarning("⚠️", "Kamida 2 ta PDF fayl kerak!")
            return

        # Saqlash joyi
        output_file = filedialog.asksaveasfilename(
            title="Birlashtirilgan PDF ni saqlash",
            defaultextension=".pdf",
            filetypes=[("PDF fayllar", "*.pdf")]
        )

        if not output_file:
            return

        # Yuklanishni ko'rsatish
        self.merge_btn.config(state='disabled')
        self.progress['value'] = 0
        self.status_label.config(text="⏳ PDF larni birlashtirish...")
        self.root.update()

        def merge_thread():
            try:
                merger = PyPDF2.PdfMerger()
                total = len(self.pdf_files)

                for i, pdf in enumerate(self.pdf_files):
                    merger.append(pdf)
                    progress = ((i + 1) / total) * 100
                    self.progress['value'] = progress
                    self.status_label.config(text=f"⏳ Yuklanmoqda: {i + 1}/{total}")
                    self.root.update()

                merger.write(output_file)
                merger.close()

                self.progress['value'] = 100
                self.status_label.config(text=f"✅ Birlashtirildi: {os.path.basename(output_file)}")
                self.root.after(0, lambda: messagebox.showinfo("✅", f"PDF birlashtirildi!\n{output_file}"))

            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("❌", f"Xatolik: {str(e)}"))
                self.status_label.config(text=f"❌ Xatolik: {str(e)[:50]}")

            finally:
                self.progress['value'] = 0
                self.merge_btn.config(state='normal')

        threading.Thread(target=merge_thread, daemon=True).start()


def main():
    root = tk.Tk()
    app = PDFMerger(root)
    root.mainloop()


if __name__ == "__main__":
    main()