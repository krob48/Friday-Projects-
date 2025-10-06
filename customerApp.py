"""
Tkinter + SQLite Customer Info Submission App (Meets Project Spec)
------------------------------------------------------------------
A single-file Python app that:
- Creates an SQLite database (`customers.db`) with a `customers` table
- Collects: Name, Birthday, Email, Phone, Address, Preferred Contact Method (dropdown)
- "Submit" button saves to DB **and clears the form**
- Optional table (Treeview) shows submitted entries for confirmation
- Simple validation for required fields, email and date format (YYYY-MM-DD)

Run:
    python customer_app.py

Stdlib only: sqlite3, tkinter. Python 3.8+
"""

import re
import sqlite3
from tkinter import Tk, StringVar, END, messagebox
from tkinter import ttk

DB_FILE = "customers.db"

# ----------------------------
# Database helpers
# ----------------------------

def get_conn():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                birthday TEXT,                -- store as ISO string YYYY-MM-DD
                email TEXT,
                phone TEXT,
                address TEXT,
                preferred_contact TEXT CHECK(preferred_contact in ('Email','Phone','Mail')),
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def insert_customer(name, birthday, email, phone, address, preferred_contact):
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO customers(name, birthday, email, phone, address, preferred_contact)
            VALUES(?,?,?,?,?,?)
            """,
            (name, birthday, email, phone, address, preferred_contact),
        )


def fetch_customers():
    with get_conn() as conn:
        cur = conn.execute(
            "SELECT id, name, birthday, email, phone, address, preferred_contact, created_at FROM customers ORDER BY id DESC"
        )
        return [dict(row) for row in cur.fetchall()]


# ----------------------------
# Validation
# ----------------------------
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PHONE_RE = re.compile(r"^[0-9+()\-\s]{7,}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")  # YYYY-MM-DD


def validate_fields(name, birthday, email, phone, preferred_contact):
    if not name.strip():
        return False, "Name is required."
    if birthday and not DATE_RE.match(birthday.strip()):
        return False, "Birthday must be YYYY-MM-DD (e.g., 2001-09-30)."
    if email and not EMAIL_RE.match(email.strip()):
        return False, "Email format looks invalid."
    if phone and not PHONE_RE.match(phone.strip()):
        return False, "Phone should contain digits and ()-+ only (min 7 chars)."
    if preferred_contact not in ("Email", "Phone", "Mail"):
        return False, "Choose a preferred contact method."
    return True, "OK"


# ----------------------------
# GUI Application
# ----------------------------
class CustomerApp:
    def __init__(self, root: Tk):
        self.root = root
        self.root.title("Customer Information (SQLite + Tkinter)")
        self.root.geometry("860x520")

        # Variables
        self.name = StringVar()
        self.birthday = StringVar()
        self.email = StringVar()
        self.phone = StringVar()
        self.address = StringVar()
        self.preferred_contact = StringVar(value="Email")

        self._build_ui()
        self.refresh_table()

    def _build_ui(self):
        container = ttk.Frame(self.root, padding=12)
        container.pack(fill="both", expand=True)

        form = ttk.LabelFrame(container, text="Enter Your Information", padding=12)
        form.pack(fill="x")

        # Row 1
        ttk.Label(form, text="Name *").grid(row=0, column=0, sticky="w", padx=(0,8), pady=6)
        ttk.Entry(form, textvariable=self.name, width=32).grid(row=0, column=1, sticky="w")

        ttk.Label(form, text="Birthday (YYYY-MM-DD)").grid(row=0, column=2, sticky="w", padx=(24,8))
        ttk.Entry(form, textvariable=self.birthday, width=18).grid(row=0, column=3, sticky="w")

        # Row 2
        ttk.Label(form, text="Email").grid(row=1, column=0, sticky="w", padx=(0,8), pady=6)
        ttk.Entry(form, textvariable=self.email, width=32).grid(row=1, column=1, sticky="w")

        ttk.Label(form, text="Phone").grid(row=1, column=2, sticky="w", padx=(24,8))
        ttk.Entry(form, textvariable=self.phone, width=18).grid(row=1, column=3, sticky="w")

        # Row 3
        ttk.Label(form, text="Address").grid(row=2, column=0, sticky="w", padx=(0,8), pady=6)
        ttk.Entry(form, textvariable=self.address, width=68).grid(row=2, column=1, columnspan=3, sticky="we")

        # Row 4 - Preferred contact dropdown
        ttk.Label(form, text="Preferred Contact *").grid(row=3, column=0, sticky="w", padx=(0,8), pady=6)
        contact_combo = ttk.Combobox(form, textvariable=self.preferred_contact, state="readonly", width=16)
        contact_combo["values"] = ("Email", "Phone", "Mail")
        contact_combo.grid(row=3, column=1, sticky="w")

        # Buttons
        btns = ttk.Frame(container)
        btns.pack(fill="x", pady=(10, 12))
        ttk.Button(btns, text="Submit", command=self.submit).pack(side="left")
        ttk.Button(btns, text="Clear", command=self.clear_form).pack(side="left", padx=8)

        # Table (optional visualization of saved entries)
        table_frame = ttk.LabelFrame(container, text="Recently Submitted", padding=8)
        table_frame.pack(fill="both", expand=True)

        columns = ("id", "name", "birthday", "email", "phone", "address", "preferred_contact", "created_at")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        headers = [
            ("id", "ID", 50),
            ("name", "Name", 160),
            ("birthday", "Birthday", 100),
            ("email", "Email", 170),
            ("phone", "Phone", 120),
            ("address", "Address", 220),
            ("preferred_contact", "Preferred", 100),
            ("created_at", "Created", 140),
        ]
        for col, text, width in headers:
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width, anchor="w")

        yscroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        xscroll = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        yscroll.grid(row=0, column=1, sticky="ns")
        xscroll.grid(row=1, column=0, sticky="ew")
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        # Nice theme tweaks
        style = ttk.Style(self.root)
        try:
            style.theme_use("clam")
        except Exception:
            pass
        style.configure("Treeview", rowheight=24)

    # ---------- Actions ----------
    def clear_form(self):
        self.name.set("")
        self.birthday.set("")
        self.email.set("")
        self.phone.set("")
        self.address.set("")
        self.preferred_contact.set("Email")

    def refresh_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for r in fetch_customers():
            self.tree.insert(
                "",
                END,
                values=(
                    r["id"], r["name"], r.get("birthday",""), r.get("email",""),
                    r.get("phone",""), r.get("address",""), r.get("preferred_contact",""), r.get("created_at",""),
                ),
            )

    def submit(self):
        name = self.name.get().strip()
        birthday = self.birthday.get().strip()
        email = self.email.get().strip()
        phone = self.phone.get().strip()
        address = self.address.get().strip()
        preferred = self.preferred_contact.get().strip()

        ok, msg = validate_fields(name, birthday, email, phone, preferred)
        if not ok:
            messagebox.showerror("Validation", msg)
            return

        try:
            insert_customer(name, birthday or None, email or None, phone or None, address or None, preferred)
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {e}")
            return

        self.refresh_table()
        self.clear_form()
        messagebox.showinfo("Success", "Your information was submitted.")


# ----------------------------
# Main entry
# ----------------------------

def main():
    init_db()
    root = Tk()
    app = CustomerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
