# Customer Information Management System 




This repository contains a simple, desktop-based application for managing customer contact information using Python and the built-in SQLite database.

The system is split into two main components: a front-end GUI for customer entry and a back-end GUI for administrative data viewing.

## Repository Contents

| File | Description | Purpose | 
 | ----- | ----- | ----- | 
| `customerApp.py` | **Customer Entry GUI** | The main application where users (customers or staff) input new customer details. | 
| `databaseView.py` | **Data Viewer GUI** | An administrative tool to connect to the database and display all stored customer records in a graphical table. | 
| `customers.db` | **SQLite Database** | The database file that persistently stores all customer data. | 
| `README.md` | **Documentation** | This file. | 

## Features

* **Customer Entry:** Easy-to-use graphical interface (GUI) for inputting new customer details.

* **Persistent Storage:** Data is saved locally using a lightweight SQLite database (`customers.db`).

* **Data Visibility:** A separate administrative tool to view, review, and refresh all captured customer data in real-time.

## Prerequisites

To run this application, you will need:

* Python 3.x

* The `sqlite3` module (included in the standard Python library)

* The `tkinter` module (usually included with standard Python installations)

## Getting Started

Follow these steps to set up and run the application on your local machine.

### 1. Clone the Repository

```
git clone [YOUR_REPOSITORY_URL_HERE]
cd [your-repo-name]

```

*(Note: Replace `[YOUR_REPOSITORY_URL_HERE]` and `[your-repo-name]` with your actual GitHub details.)*

### 2. Run the Customer Entry App

To allow a customer to input their data and populate the database:

```
python customerApp.py

```

This will launch the main input GUI. Every time a record is successfully submitted, it is written to the `customers.db` file.

### 3. Run the Database Viewer App

To view all the collected customer data (for administrative purposes):

```
python databaseView.py

```

This will launch the data viewer GUI, displaying the contents of the `customers.db` file in a clean, scrollable table. You can use the **Refresh** button inside the viewer to see new records added by the `customerApp.py` in real-time.

## Database Structure

The `customers.db` file contains a single table (likely named `customer_data` or similar) which stores the following customer fields:

* `id` (Primary Key, Auto-incremented)

* `[Insert other fields here, e.g., name, email, phone, etc.]`

* `...`

*Created with the help of Gemini.*
"""
    
    file_path = "README.md"
    
    try:
        # Open the file in write mode ('w'). This will create the file if it doesn't exist 
        # or overwrite it if it does.
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print(f"Successfully created '{file_path}' in the current directory.")
        print("You can now add it to your Git repository.")

    except IOError as e:
        print(f"Error writing to file {file_path}: {e}")

if __name__ == "__main__":
    create_readme_file()
