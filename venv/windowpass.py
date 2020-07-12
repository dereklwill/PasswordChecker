import tkinter as tk
import requests
import hashlib
import sys

url = 'https://api.pwnedpasswords.com/range/' + 'CBFDA'
res = requests.get(url)

def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check the API and try again.')
    return res

def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0

def pwned_api_check(password):
    sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1_password[:5], sha1_password[5:]
    response = request_api_data(first5_char)
    return get_password_leaks_count(response, tail)

root = tk.Tk()
root.title('Password Breach Checker')

canvas1 = tk.Canvas(root, width=600, height=320, relief='raised')
canvas1.pack()

label1 = tk.Label(root, text='Has your password been breached?')
label1.config(font=('helvetica', 17))
canvas1.create_window(300, 25, window=label1)

label2 = tk.Label(root, text='Type your password here')
label2.config(font=('helvetica', 12))
canvas1.create_window(300, 80, window=label2)

label5 = tk.Label(root, text='(Password not stored and only checked as hash)')
label5.config(font=('helvetica', 8))
canvas1.create_window(300, 100, window=label5)

label6 = tk.Label(root, text='*Powered by haveibeenpwned API')
label6.config(font=('helvetica', 10))
canvas1.create_window(300, 300, window=label6)

entry1 = tk.Entry(root)
canvas1.create_window(300, 130, window=entry1)

def func(event):
    x1 = entry1.get()
    count = pwned_api_check(x1)
    label6 = tk.Label(root, text='                                                                                   ',
                      font=('helvetica', 16))
    canvas1.create_window(300, 250, window=label6)
    label3 = tk.Label(root, text=f'{x1} was found {count} times!', font=('helvetica', 13))
    canvas1.create_window(300, 250, window=label3)
root.bind('<Return>', func)

def end_program():
    root.destroy()

def main_pass():
    x1 = entry1.get()
    count = pwned_api_check(x1)
    label6 = tk.Label(root, text='                                                                                   ', font=('helvetica', 16))
    canvas1.create_window(300, 250, window=label6)
    label3 = tk.Label(root, text=f'{x1} was found {count} times!', font=('helvetica', 13))
    canvas1.create_window(300, 250, window=label3)

button1 = tk.Button(text='Have you been pwned?', command=main_pass, bg='orange', fg='black', font=('helvetica', 11, 'bold'))
button2 = tk.Button(text='Quit', command=end_program, bg='orange', fg='black', font=('helvetica', 10, 'bold'))
canvas1.create_window(300, 180, window=button1)
canvas1.create_window(300, 220, window=button2)

root.mainloop()