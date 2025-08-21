import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date


conn = mysql.connector.connect(
    host="localhost",
    user="root",  # apna MySQL username
    password="tpq2ikk",  # apna MySQL password
    database="library_db"
)
cursor = conn.cursor()



def add_book():
    title = book_title_entry.get()
    author = book_author_entry.get()
    qty = book_qty_entry.get()

    if title and author and qty:
        cursor.execute("INSERT INTO books (title, author, qty) VALUES (%s, %s, %s)",
                       (title, author, qty))
        conn.commit()
        messagebox.showinfo("Success", "Book added successfully!")
        load_books()
    else:
        messagebox.showwarning("Input Error", "Please fill all fields")

def load_books():
    for i in book_table.get_children():
        book_table.delete(i)
    cursor.execute("SELECT * FROM books")
    for row in cursor.fetchall():
        book_table.insert("", tk.END, values=row)

def delete_book():
    selected = book_table.selection()
    if selected:
        book_id = book_table.item(selected[0])['values'][0]
        cursor.execute("DELETE FROM books WHERE id=%s", (book_id,))
        conn.commit()
        messagebox.showinfo("Deleted", "Book deleted successfully!")
        load_books()
    else:
        messagebox.showwarning("Selection Error", "Please select a book to delete")

# ======== MEMBER FUNCTIONS ========

def add_member():
    name = member_name_entry.get()
    email = member_email_entry.get()
    phone = member_phone_entry.get()

    if name:
        cursor.execute("INSERT INTO members (name, email, phone) VALUES (%s, %s, %s)",
                       (name, email, phone))
        conn.commit()
        messagebox.showinfo("Success", "Member added successfully!")
        load_members()
    else:
        messagebox.showwarning("Input Error", "Please enter member name")

def load_members():
    for i in member_table.get_children():
        member_table.delete(i)
    cursor.execute("SELECT * FROM members")
    for row in cursor.fetchall():
        member_table.insert("", tk.END, values=row)

def delete_member():
    selected = member_table.selection()
    if selected:
        member_id = member_table.item(selected[0])['values'][0]
        cursor.execute("DELETE FROM members WHERE id=%s", (member_id,))
        conn.commit()
        messagebox.showinfo("Deleted", "Member deleted successfully!")
        load_members()
    else:
        messagebox.showwarning("Selection Error", "Please select a member to delete")


def issue_book():
    book_id = issue_book_id_entry.get()
    member_id = issue_member_id_entry.get()
    today = date.today()

    cursor.execute("SELECT qty FROM books WHERE id=%s", (book_id,))
    book = cursor.fetchone()
    if not book:
        messagebox.showerror("Error", "Book not found!")
        return
    if book[0] <= 0:
        messagebox.showerror("Error", "Book not available!")
        return

    cursor.execute("INSERT INTO transactions (book_id, member_id, issue_date) VALUES (%s, %s, %s)",
                   (book_id, member_id, today))
    cursor.execute("UPDATE books SET qty = qty - 1 WHERE id=%s", (book_id,))
    conn.commit()
    messagebox.showinfo("Issued", "Book issued successfully!")
    load_transactions()
    load_books()

def return_book():
    trans_id = return_trans_id_entry.get()
    today = date.today()

    cursor.execute("SELECT book_id FROM transactions WHERE id=%s AND return_date IS NULL", (trans_id,))
    trans = cursor.fetchone()
    if not trans:
        messagebox.showerror("Error", "Invalid Transaction ID or already returned!")
        return

    cursor.execute("UPDATE transactions SET return_date=%s WHERE id=%s", (today, trans_id))
    cursor.execute("UPDATE books SET qty = qty + 1 WHERE id=%s", (trans[0],))
    conn.commit()
    messagebox.showinfo("Returned", "Book returned successfully!")
    load_transactions()
    load_books()

def load_transactions():
    for i in trans_table.get_children():
        trans_table.delete(i)
    cursor.execute("""
        SELECT t.id, b.title, m.name, t.issue_date, t.return_date
        FROM transactions t
        JOIN books b ON t.book_id = b.id
        JOIN members m ON t.member_id = m.id
    """)
    for row in cursor.fetchall():
        trans_table.insert("", tk.END, values=row)

# ======== GUI SETUP ========

root = tk.Tk()
root.title("𝓛𝓲𝓫𝓻𝓪𝓻𝔂 𝓜𝓪𝓷𝓪𝓰𝓮𝓶𝓮𝓷𝓽 𝓢𝔂𝓼𝓽𝓮𝓶 𝓫𝔂 𝓜𝓾𝓱𝓪𝓶𝓶𝓪𝓭 𝓤𝓼𝓶𝓪𝓷")

root.iconbitmap(r"C:\Users\Administrator\Downloads\icons8-library-50.ico")
root.geometry("950x600")
root.configure(bg="blue")

tab_control = ttk.Notebook(root)

# Books Tab
books_tab = ttk.Frame(tab_control)
tab_control.add(books_tab, text="Books")

tk.Label(books_tab, text="Title").grid(row=0, column=0)
book_title_entry = tk.Entry(books_tab)
book_title_entry.grid(row=0, column=1)

tk.Label(books_tab, text="Author").grid(row=0, column=2)
book_author_entry = tk.Entry(books_tab)
book_author_entry.grid(row=0, column=3)

tk.Label(books_tab, text="Qty").grid(row=0, column=4)
book_qty_entry = tk.Entry(books_tab)
book_qty_entry.grid(row=0, column=5)

tk.Button(books_tab, text="Add Book", command=add_book).grid(row=0, column=6, padx=5)
tk.Button(books_tab, text="Delete Book", command=delete_book).grid(row=0, column=7, padx=5)

book_table = ttk.Treeview(books_tab, columns=("ID", "Title", "Author", "Qty"), show="headings")
for col in ("ID", "Title", "Author", "Qty"):
    book_table.heading(col, text=col)
book_table.grid(row=1, column=0, columnspan=8, pady=10)
load_books()

# Members Tab
members_tab = ttk.Frame(tab_control)
tab_control.add(members_tab, text="Members")

tk.Label(members_tab, text="Name").grid(row=0, column=0)
member_name_entry = tk.Entry(members_tab)
member_name_entry.grid(row=0, column=1)

tk.Label(members_tab, text="Email").grid(row=0, column=2)
member_email_entry = tk.Entry(members_tab)
member_email_entry.grid(row=0, column=3)

tk.Label(members_tab, text="Phone").grid(row=0, column=4)
member_phone_entry = tk.Entry(members_tab)
member_phone_entry.grid(row=0, column=5)

tk.Button(members_tab, text="Add Member", command=add_member).grid(row=0, column=6, padx=5)
tk.Button(members_tab, text="Delete Member", command=delete_member).grid(row=0, column=7, padx=5)

member_table = ttk.Treeview(members_tab, columns=("ID", "Name", "Email", "Phone"), show="headings")
for col in ("ID", "Name", "Email", "Phone"):
    member_table.heading(col, text=col)
member_table.grid(row=1, column=0, columnspan=8, pady=10)
load_members()

# Transactions Tab
trans_tab = ttk.Frame(tab_control)
tab_control.add(trans_tab, text="Transactions")

tk.Label(trans_tab, text="Book ID").grid(row=0, column=0)
issue_book_id_entry = tk.Entry(trans_tab)
issue_book_id_entry.grid(row=0, column=1)

tk.Label(trans_tab, text="Member ID").grid(row=0, column=2)
issue_member_id_entry = tk.Entry(trans_tab)
issue_member_id_entry.grid(row=0, column=3)

tk.Button(trans_tab, text="Issue Book", command=issue_book).grid(row=0, column=4, padx=5)

tk.Label(trans_tab, text="Transaction ID").grid(row=1, column=0)
return_trans_id_entry = tk.Entry(trans_tab)
return_trans_id_entry.grid(row=1, column=1)

tk.Button(trans_tab, text="Return Book", command=return_book).grid(row=1, column=2, padx=5)

trans_table = ttk.Treeview(trans_tab, columns=("ID", "Book", "Member", "Issue Date", "Return Date"), show="headings")
for col in ("ID", "Book", "Member", "Issue Date", "Return Date"):
    trans_table.heading(col, text=col)
trans_table.grid(row=2, column=0, columnspan=5, pady=10)
load_transactions()

tab_control.pack(expand=1, fill="both")

root.mainloop()
