import sqlite3
import re
from tkinter import *
from tkinter import messagebox

# Database Initialization
connection = sqlite3.connect("snippet_database.db")
cursor = connection.cursor()

# Create the snippets table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS snippets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        code TEXT NOT NULL,
        description TEXT,
        tags TEXT
    )
''')
connection.commit()

# Function to extract keywords from code
def extract_keywords(code):
    keywords = set()
    tags_keywords = {
        'database': ['sql', 'mongodb', 'postgresql', 'database'],
        'sorting': ['sort', 'order', 'filter'],
        'web': ['html', 'css', 'javascript', 'web', 'frontend', 'backend'],
        # Add more tags and keywords here
    }
    
    for tag, keywords_list in tags_keywords.items():
        for keyword in keywords_list:
            if re.search(r'\b' + re.escape(keyword) + r'\b', code, re.IGNORECASE):
                keywords.add(tag)
    return keywords

# Function to add a new snippet
def add_snippet():
    name = name_entry.get()
    code = code_text.get("1.0", "end-1c")
    description = description_entry.get()
    tags = extract_keywords(code)
    
    cursor.execute('''
        INSERT INTO snippets (name, code, description, tags)
        VALUES (?, ?, ?, ?)
    ''', (name, code, description, ", ".join(tags)))
    
    connection.commit()
    messagebox.showinfo("Success", "Snippet added successfully!")

# Function to search snippets by tag
def search_by_tag():
    tag = search_tag_entry.get()
    cursor.execute('SELECT name, description FROM snippets WHERE tags LIKE ?', ('%' + tag + '%',))
    results = cursor.fetchall()
    
    search_result_text.config(state=NORMAL)
    search_result_text.delete("1.0", "end")
    for result in results:
        search_result_text.insert(END, f"Name: {result[0]}\nDescription: {result[1]}\n\n")
    search_result_text.config(state=DISABLED)

# Create the GUI
root = Tk()
root.title("Code Snippet Organizer")

# Labels
name_label = Label(root, text="Snippet Name:")
code_label = Label(root, text="Code:")
description_label = Label(root, text="Description:")
search_tag_label = Label(root, text="Search by Tag:")

# Entry fields
name_entry = Entry(root)
code_text = Text(root, height=10, width=50)
description_entry = Entry(root)
search_tag_entry = Entry(root)

# Buttons
add_button = Button(root, text="Add Snippet", command=add_snippet)
search_button = Button(root, text="Search by Tag", command=search_by_tag)

# Display the search results
search_result_text = Text(root, height=10, width=50, state=DISABLED)

# Arrange the GUI components using grid layout
name_label.grid(row=0, column=0, sticky=E)
name_entry.grid(row=0, column=1, columnspan=3, padx=10, pady=10)
code_label.grid(row=1, column=0, sticky=E)
code_text.grid(row=1, column=1, columnspan=3, padx=10, pady=10)
description_label.grid(row=2, column=0, sticky=E)
description_entry.grid(row=2, column=1, columnspan=3, padx=10, pady=10)
add_button.grid(row=3, column=0, columnspan=2, pady=10)
search_tag_label.grid(row=3, column=2, sticky=E)
search_tag_entry.grid(row=3, column=3, padx=10)
search_button.grid(row=4, column=2, columnspan=2, pady=10)
search_result_text.grid(row=5, column=0, columnspan=4, padx=10, pady=10)

# Start the GUI event loop
root.mainloop()

# Close the database connection on application exit
connection.close()
