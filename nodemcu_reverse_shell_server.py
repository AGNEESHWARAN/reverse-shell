import network
import socket

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid="esp8266",password="123456789")

print(ap.ifconfig())


s = socket.socket()


s.bind(("",9999))

s.listen(5)
conn, add = s.accept()
while True:
    
    
    cmd = input(">> ")
    
    conn.send(str.encode(cmd))
    client_response = str(conn.recv(20480),"utf-8")
    print(client_response)
    print("")
    
