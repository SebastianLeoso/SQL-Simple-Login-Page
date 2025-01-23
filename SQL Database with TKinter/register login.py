import tkinter as tk
from tkinter import messagebox
import sqlite3

def create_user(username, password):
    conn = sqlite3.connect('user_credentials.db')
    cursor = conn.cursor()

    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))

    conn.commit()
    conn.close()

    messagebox.showinfo('Success', 'Bruger oprettet!')

def register_window():
    register_window = tk.Toplevel(root)
    register_window.title('Opret Bruger')

    tk.Label(register_window, text='Brugernavn:').grid(row=0, column=0, padx=10, pady=10)
    register_username_entry = tk.Entry(register_window)
    register_username_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(register_window, text='Adgangskode:').grid(row=1, column=0, padx=10, pady=10)
    register_password_entry = tk.Entry(register_window, show='*')  
    register_password_entry.grid(row=1, column=1, padx=10, pady=10)

    def on_register():
        username = register_username_entry.get()
        password = register_password_entry.get()

        if username and password:
            create_user(username, password)
            register_window.destroy()  
        else:
            messagebox.showwarning('Fejl', 'Venligst skriv både brugernavn og adgangskode')

    register_button = tk.Button(register_window, text='Opret', command=on_register)
    register_button.grid(row=2, column=0, columnspan=2, pady=10)

def login_user(username, password):
    conn = sqlite3.connect('user_credentials.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()

    conn.close()

    return user

def login_window():
    login_window = tk.Toplevel(root)
    login_window.title('User Login')

    tk.Label(login_window, text='Brugernavn:').grid(row=0, column=0, padx=10, pady=10)
    login_username_entry = tk.Entry(login_window)
    login_username_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(login_window, text='Adgangskode:').grid(row=1, column=0, padx=10, pady=10)
    login_password_entry = tk.Entry(login_window, show='*')  
    login_password_entry.grid(row=1, column=1, padx=10, pady=10)

    def on_login():
        username = login_username_entry.get()
        password = login_password_entry.get()

        if username and password:
            user = login_user(username, password)
            if user:
                messagebox.showinfo('Success', 'Logget ind')
            else:
                messagebox.showwarning('Fejl', 'Forkert brugernavn eller adgangskode')
        else:
            messagebox.showwarning('Fejl', 'Venligst skriv både brugernavn eller adgangskode')

    login_button = tk.Button(login_window, text='Login', command=on_login)
    login_button.grid(row=2, column=0, columnspan=2, pady=10)

conn = sqlite3.connect('user_credentials.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')

conn.commit()
conn.close()

root = tk.Tk()
root.title('User Credentials Manager')

register_button = tk.Button(root, text='Opret', command=register_window)
register_button.grid(row=0, column=0, padx=10, pady=10)

login_button = tk.Button(root, text='Login', command=login_window)
login_button.grid(row=0, column=1, padx=10, pady=10)

root.mainloop()