import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet
import os

# Generate a key for encryption and decryption (this should be kept safe)
def generate_key():
    return Fernet.generate_key()

# Load encryption key from file or generate a new one
def load_key():
    if os.path.exists("secret.key"):
        with open("secret.key", "rb") as key_file:
            return key_file.read()
    else:
        key = generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)
        return key

# Encrypt a password
def encrypt_password(password):
    key = load_key()
    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(password.encode())
    return encrypted_password

# Decrypt a password
def decrypt_password(encrypted_password):
    key = load_key()
    fernet = Fernet(key)
    decrypted_password = fernet.decrypt(encrypted_password).decode()
    return decrypted_password

# File to store passwords
PASSWORD_FILE = "passwords.txt"

# Save a password to the file
def save_password():
    website = website_entry.get().strip()
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if not website or not username or not password:
        messagebox.showerror("Error", "All fields are required.")
        return

    encrypted_password = encrypt_password(password)

    with open(PASSWORD_FILE, "a") as file:
        file.write(f"{website},{username},{encrypted_password.decode()}\n")

    website_entry.delete(0, tk.END)
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    messagebox.showinfo("Success", "Password saved successfully!")

# View saved passwords
def view_passwords():
    if not os.path.exists(PASSWORD_FILE):
        messagebox.showinfo("No Data", "No passwords saved yet.")
        return

    with open(PASSWORD_FILE, "r") as file:
        passwords = file.readlines()

    passwords_display.delete(1.0, tk.END)
    for line in passwords:
        website, username, encrypted_password = line.strip().split(",")
        decrypted_password = decrypt_password(encrypted_password.encode())
        passwords_display.insert(tk.END, f"Website: {website}\nUsername: {username}\nPassword: {decrypted_password}\n\n")

# Delete a password
def delete_password():
    website_to_delete = website_entry.get().strip()

    if not os.path.exists(PASSWORD_FILE):
        messagebox.showinfo("No Data", "No passwords saved yet.")
        return

    updated_passwords = []
    found = False

    with open(PASSWORD_FILE, "r") as file:
        for line in file:
            website, username, encrypted_password = line.strip().split(",")
            if website != website_to_delete:
                updated_passwords.append(line)
            else:
                found = True

    if not found:
        messagebox.showerror("Error", "Website not found.")
        return

    with open(PASSWORD_FILE, "w") as file:
        file.writelines(updated_passwords)

    messagebox.showinfo("Success", f"Password for '{website_to_delete}' deleted.")
    view_passwords()

    # Clear the website entry field after deletion
    website_entry.delete(0, tk.END)

# Create main window
root = tk.Tk()
root.title("Password Manager")

# Input fields
website_label = tk.Label(root, text="Website:")
website_label.grid(row=0, column=0, padx=10, pady=5)
website_entry = tk.Entry(root, width=30)
website_entry.grid(row=0, column=1, padx=10, pady=5)

username_label = tk.Label(root, text="Username:")
username_label.grid(row=1, column=0, padx=10, pady=5)
username_entry = tk.Entry(root, width=30)
username_entry.grid(row=1, column=1, padx=10, pady=5)

password_label = tk.Label(root, text="Password:")
password_label.grid(row=2, column=0, padx=10, pady=5)
password_entry = tk.Entry(root, width=30)
password_entry.grid(row=2, column=1, padx=10, pady=5)

# Buttons
save_button = tk.Button(root, text="Save Password", command=save_password)
save_button.grid(row=3, column=0, columnspan=2, pady=10)

view_button = tk.Button(root, text="View Passwords", command=view_passwords)
view_button.grid(row=4, column=0, columnspan=2, pady=10)

delete_button = tk.Button(root, text="Delete Password", command=delete_password)
delete_button.grid(row=5, column=0, columnspan=2, pady=10)

# Display for saved passwords
passwords_display = tk.Text(root, width=50, height=10)
passwords_display.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

# Start the application
root.mainloop()
