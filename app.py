import zipfile
import os
import concurrent.futures
import tkinter as tk
from tkinter import filedialog
import threading

def crack_zip(zip_file, password, result_text):
    password = password.strip()  # Remove newline characters
    try:
        with zipfile.ZipFile(zip_file, 'r') as zfile:
            zfile.extractall(pwd=password.encode())
            result_text.insert(tk.END, f"Password found: {password}\n")
            return password
    except Exception:
        return None

def crack_zip_fast(zip_file, wordlist, result_text):
    with open(wordlist, 'r', encoding='latin-1') as f:
        passwords = f.readlines()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_password = {executor.submit(crack_zip, zip_file, password, result_text): password for password in passwords}
        for future in concurrent.futures.as_completed(future_to_password):
            if future.result():
                return future.result()

    result_text.insert(tk.END, "Password not found in the wordlist.\n")
    return None

def select_file(entry):
    file_path = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, file_path)

def start_cracking():
    zip_file_path = zip_entry.get()
    wordlist_path = wordlist_entry.get()
    
    result_text.delete(1.0, tk.END)  # Clear previous result
    
    if not os.path.isfile(zip_file_path) or not os.path.isfile(wordlist_path):
        result_text.insert(tk.END, "Please provide valid file paths.")
        return
    
    result_text.insert(tk.END, "Cracking mode started...\n")
    
    threading.Thread(target=crack_zip_fast, args=(zip_file_path, wordlist_path, result_text)).start()

# Create the Tkinter window
root = tk.Tk()
root.title("ZIP Cracker")

# File Path inputs
zip_label = tk.Label(root, text="ZIP File:")
zip_label.pack()
zip_entry = tk.Entry(root, width=50)
zip_entry.pack()
zip_button = tk.Button(root, text="Select File", command=lambda: select_file(zip_entry))
zip_button.pack()

wordlist_label = tk.Label(root, text="Wordlist File:")
wordlist_label.pack()
wordlist_entry = tk.Entry(root, width=50)
wordlist_entry.pack()
wordlist_button = tk.Button(root, text="Select File", command=lambda: select_file(wordlist_entry))
wordlist_button.pack()

# Result display area
result_label = tk.Label(root, text="Cracking Results:")
result_label.pack()
result_text = tk.Text(root, width=50, height=10)
result_text.pack()

# Start cracking button
start_button = tk.Button(root, text="Start Cracking", command=start_cracking)
start_button.pack()

root.mainloop()
