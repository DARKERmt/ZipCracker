import zipfile
import os
import time

def crack_zip_visual(zip_file, wordlist):
    with open(wordlist, 'r', encoding='latin-1') as f:
        passwords = f.readlines()

    with zipfile.ZipFile(zip_file, 'r') as zfile:
        for password in passwords:
            print("trying password =>", password)
            time.sleep(0.01)
            os.system("cls")
            password = password.strip()  # Remove newline characters
            try:
                zfile.extractall(pwd=password.encode())
                print(f"Password found: {password}")
                return password
            except Exception:
                pass

    print("Password not found in the wordlist.")
    return None


def crack_zip_fast(zip_file, wordlist):
    with open(wordlist, 'r', encoding='latin-1') as f:
        passwords = f.readlines()

    with zipfile.ZipFile(zip_file, 'r') as zfile:
        for password in passwords:
            password = password.strip()  # Remove newline characters
            try:
                zfile.extractall(pwd=password.encode())
                print(f"Password found: {password}")
                return password
            except Exception:
                pass

    print("Password not found in the wordlist.")
    return None

if __name__ == "__main__":
    file_path = input("Enter your file path => ")
    zip_file_path = file_path.replace('"',"")
    wordlist = input("Enter your word list path => ")
    wordlist_path = wordlist.replace('"',"")
    print("which mode you want to try this")
    print("[+] 1 for visual mode (slow)\n[+] 2 for fast mode")
    choose = input("=>")
    if int(choose)==1 :
        print("visual mode cracking started.......!")
        crack_zip_visual(zip_file_path, wordlist_path)
    elif int(choose)==2 :
        print("fast cracking mode started.......!")
        crack_zip_fast(zip_file_path, wordlist_path)
    else:
        print("please enter a valid input")
        exit()
