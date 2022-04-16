import socket
import time
import os
import sys
import json

with open('config.json', 'r') as f:
    configs = json.loads(f.read())

def dlpkg(s):
    pkg = input("What package do you want to copy?\n")
    output = input("Where should it be output to?\n")

    s.sendall(pkg.encode())
    start = time.time()
    fsize = 0
    with open(output, 'wb') as f:
        while True:
            received = s.recv(4096)
            fsize += 4
            if received.decode("utf-8", "ignore")[-8:] == "!!DONE!!":
                break
            elif received.decode("utf-8", "ignore")[-16:] == "!!FILENOTFOUND!!":
                print("That package doesn't exist. Please try again.")
                os.remove(output)
                quit()
            f.write(received)
        print("Elapsed time:", round(time.time() - start, 2), "s")
        if fsize > 1024:
            print("Total package size:", round(fsize / 1024, 2), "MB")
        else:
            print("Total package size,", fsize, "KB")

def mkpkg(s):
    pkgname = input("What is the package name?\n")
    dirs = []
    print("What folders/files are included?")
    while True:
        inpt = input()
        if inpt == '':
            break
        dirs.append(inpt)

    s.sendall(json.dumps((pkgname, dirs)).encode())

def lspkg(s):
    pass

if len(sys.argv) < 2:
    print("Please input a mode")
elif sys.argv[1] == 'dl':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((configs["server_address"], configs["port"]))
        s.sendall('!!dlpkg!!'.encode())
        dlpkg(s)
elif sys.argv[1] == 'help':
    print("HELP PLS")
elif sys.argv[1] == 'make':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((configs["server_address"], configs["port"]))
        s.sendall('!!mkpkg!!'.encode())
        mkpkg(s)
elif sys.argv[1] == 'list':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((configs["server_address"], configs["port"]))
        s.sendall('!!lspkg!!'.encode())
        lspkg(s)
