import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os

DATABASE_FILE = "customers.db"
APP_TITLE = "Customer Database Viewer"

class DBViewerApp:
    """A Tkinter application to view customer data from an SQLite database."""
    def __init__(self, master):
        self.master = master
        master.title(APP_TITLE)
        master.geometry("800x500")
        
        # Configure grid for resizing
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)

        # Frame for the Treeview (Table) and Scrollbars
        self.tree_frame = ttk.Frame(master, padding="10")
        self.tree_frame.grid(row=0, column=0, sticky="nsew")
        self.tree_frame.grid_columnconfigure(0, weight=1)
        self.tree_frame.grid_rowconfigure(0, weight=1)

        # Create Treeview (the table widget)
        self.tree = ttk.Treeview(self.tree_frame, show='headings')
        self.tree.grid(row=0, column=0, sticky="nsew")

        # Add scrollbars to the Treeview
        self.vsb = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.vsb.grid(row=0, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=self.vsb.set)
        
        self.hsb = ttk.Scrollbar(self.tree_frame, orient="horizontal", command=self.tree.xview)
        self.hsb.grid(row=1, column=0, sticky='ew')
        self.tree.configure(xscrollcommand=self.hsb.set)

        # Frame for controls (Button and Status)
        self.control_frame = ttk.Frame(master, padding="10 10 10 0")
        self.control_frame.grid(row=1, column=0, sticky="ew")
        
        # Load Data Button
        self.load_button = ttk.Button(self.control_frame, text="Refresh Customer Data", command=self.load_data)
        self.load_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Status Label
        self.status_label = ttk.Label(self.control_frame, text="Status: Ready", anchor="w")
        self.status_label.pack(side=tk.LEFT, fill='x', expand=True, padx=10)
        
        # Initial data load
        self.load_data()

    def _get_db_data(self):
        """
        Connects to the database, finds the main table, and fetches all data.
        Returns: tuple (column_names, rows) or None on error.
        """
        if not os.path.exists(DATABASE_FILE):
            self.status_label.config(text=f"Status: Error - Database file '{DATABASE_FILE}' not found.", foreground='red')
            return None, None

        try:
            with sqlite3.connect(DATABASE_FILE) as conn:
                cursor = conn.cursor()

                # 1. Find the name of the first user-defined table
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' LIMIT 1")
                result = cursor.fetchone()
                
                if not result:
                    self.status_label.config(text="Status: Error - No customer tables found in the database.", foreground='red')
                    return None, None
                    
                table_name = result[0]
                
                # 2. Get the column names
                cursor.execute(f"PRAGMA table_info({table_name});")
                column_names = [col[1] for col in cursor.fetchall()]
                
                # 3. Get the data
                cursor.execute(f"SELECT * FROM {table_name}")
                rows = cursor.fetchall()
                
                self.status_label.config(text=f"Status: Successfully loaded data from table '{table_name}'.", foreground='green')
                return column_names, rows

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An SQLite error occurred: {e}")
            self.status_label.config(text=f"Status: SQLite Error - {e}", foreground='red')
            return None, None
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
            self.status_label.config(text=f"Status: Unexpected Error - {e}", foreground='red')
            return None, None


    def load_data(self):
        """Fetches data and updates the Treeview display."""
        
        # Clear existing data in Treeview
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = ()
        
        column_names, rows = self._get_db_data()
        
        if column_names and rows is not None:
            # 1. Configure the Treeview columns
            self.tree["columns"] = column_names
            
            for col_name in column_names:
                # Setup column properties (stretch=True makes columns fill the width)
                self.tree.column(col_name, anchor=tk.CENTER, width=100, stretch=tk.TRUE)
                # Set the column heading text
                self.tree.heading(col_name, text=col_name)

            # 2. Insert the fetched rows
            for row in rows:
                self.tree.insert("", tk.END, values=row)

if __name__ == "__main__":
    # Create the main window
    root = tk.Tk()
    # Apply a cleaner theme
    style = ttk.Style()
    style.theme_use('clam')
    
    # Initialize and run the application
    app = DBViewerApp(root)
    root.mainloop()