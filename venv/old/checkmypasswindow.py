#Checks passwords for breaches using pwnedpasswords API
#Run in terminal with password(s) as inputs with spaces between args
#Ex. python checkmypass.py password1 password2 1234567

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

# def main(args):
#     for password in args:
#         count = pwned_api_check(password)
#         if count:
#             print(f'{password} was found {count} times! You should change your password!')
#         else:
#             print(f'{password} was not found. You can still use this password!')
#     return 'Done!'

def main_pass(password):
        count = pwned_api_check(password)
        if count:
            print(f'{password} was found {count} times! You should change your password!')
        else:
            print(f'{password} was not found. You can still use this password!')

if __name__ == '__main__':
    main_pass(input('Was your password pwned? Input password here: '))