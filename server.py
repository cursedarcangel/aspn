import socket
import os
import json

with open('.pkgs', 'r') as f:
    port = json.loads(f.read())["port"]

def dlpkg(pkg, conn):
    if os.path.exists(pkg):
        size = os.path.getsize(pkg)
        with open(pkg, "rb") as f:
            while True:
                bytesRead = f.read(4096)
                if not bytesRead:
                    break
                conn.sendall(bytesRead)
        conn.sendall(b"!!DONE!!")
        return
    else:
        conn.sendall(b"!!FILENOTFOUND!!")
        return

def mkpkg(info):
    pkginfo = json.loads(info)
    with open('.pkgs', 'r+') as f:
        data = json.loads(f.read())
        data['pkgs'][pkginfo[0]] = pkginfo[1]
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print(port)
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
