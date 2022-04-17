import socket
import time
import os
import sys
import json

with open('config.json', 'r') as f:
    configs = json.loads(f.read())

def dlpkg(s):
    pkg = input("What package do you want to copy?\n")

    s.sendall(pkg.encode())
    start = time.time()
    fsize = 0
    if not os.path.exists(pkg):
        os.mkdir(pkg)
    while True:
        currentFile = s.recv(4096).decode("utf-8", 'ignore')
        print(currentFile)
        with open(f"{pkg}/{currentFile}", 'wb') as f:
            while True:
                received = s.recv(4096)
                fsize += 4
                if received.decode("utf-8", "ignore")[-8:] == "!!DONE!!":
                    print(f"{pkg}/{currentFile} transferred")
                    break
                elif received.decode("utf-8", "ignore")[-15:] == "!!PKGNOTFOUND!!":
                    print("That package doesn't exist. Please try again.")
                    os.remove(pkg)
                    quit()
                elif received.decode("utf-8", "ignore")[-16:] == "!!FILENOTFOUND!!":
                    print('e')
                    notFound = s.recv(4096).decode()
                    print(f"File {notFound} not found")
                    quit()
                elif received.decode("utf-8", "ignore")[-11:] == "!!PKGDONE!!":
                    print("Elapsed time:", round(time.time() - start, 2), "s")
                    if fsize > 1024:
                        print("Total package size:", round(fsize / 1024, 2), "MB")
                    else:
                        print("Total package size,", fsize, "KB")
                    quit()
                f.write(received)

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
    pkgs = json.loads(s.recv(4096).decode())
    for pk in pkgs:
        print(f"{pk[0]}: {pk[1]} files")

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

