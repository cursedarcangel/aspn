import socket
import os
import json

with open('.pkgs', 'r') as f:
    port = json.loads(f.read())["port"]

def dlfil(fil, conn):
    if os.path.exists(fil):
        conn.sendall(os.path.basename(fil).encode())
        with open(fil, "rb") as f:
            while True:
                bytesRead = f.read(4096)
                if not bytesRead:
                    break
                conn.sendall(bytesRead)
        conn.sendall(b"!!DONE!!")
        return True
    else:
        conn.sendall(b"!!FILENOTFOUND!!")
        conn.sendall(os.path.basename(fil).encode())
        print(fil)
        return False

def dlpkg(pkg, conn):
    files = []
    with open('.pkgs', 'r') as f:
        pkgs = json.loads(f.read())['pkgs']
 
    for k, v in pkgs.items():
        if pkg.casefold() == k.casefold():
            files = v
            break
        else:
            conn.sendall(b"!!PKGNOTFOUND!!")
    
    for f in files:
        if os.path.isdir(f):
            print('is a dir')
            pass
        else:
            print(f)
            if dlfil(f, conn):
                continue
                print(f"{f} transferred")
            else:
                continue
    conn.sendall(b"!!PKGDONE!!")

def mkpkg(info):
    pkginfo = json.loads(info)
    with open('.pkgs', 'r+') as f:
        data = json.loads(f.read())
        data['pkgs'][pkginfo[0]] = pkginfo[1]
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('0.0.0.0', port))
    print('Server started')
    while True:
        s.listen()
        conn, addr = s.accept()
        with conn:
            while True:
                rq = conn.recv(1024).decode()
                if not rq:
                    break
                elif rq[-9:] == '!!mkpkg!!':
                    mkpkg(conn.recv(4096).decode())
                elif rq[-9:] == '!!dlpkg!!':
                    dlpkg(conn.recv(4096).decode(), conn)
