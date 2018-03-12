import socket 
import _thread
def gra(gracz1,gracz2):
    print("gra rozpoczeta")
    gracz1.send((1).to_bytes(8,byteorder='big'))
    gracz2.send((2).to_bytes(8,byteorder='big'))
    while True:
        idb = gracz1.recv(1024)
        if not idb:
            break
        gracz2.send(idb)
        idb = gracz2.recv(1024)
        idb = gracz2.recv(1024)
        if not idb:
            break
        gracz1.send(idb)
        idb = gracz1.recv(1024)
    gracz1.close()
    gracz2.close()

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
host = socket.gethostname()
port = 12346               
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))  
s.listen(5)
while True:
    gracz1, addr = s.accept()
    print ("Gracz 1 polaczony")
    gracz2, addr = s.accept() 
    print ("Gracz 2 polaczony")
    _thread.start_new_thread(gra,(gracz1,gracz2))
